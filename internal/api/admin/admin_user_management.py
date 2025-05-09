from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from rapidfuzz import fuzz
from internal.utils.utils import get_current_admin
from internal.types.responses import PublicUserResponse, FailResponse, SuccessResponse
from internal.types.types import SUCCESS, FAIL, NEED_ACTION
from internal.database.users import get_all_users, get_user_by_id
from internal.models.user import User, PublicUser, UserPreview, PaginatedUserPreviewListResponse
from internal.utils.email import generate_penalty_email_html, generate_penalty_email_html_for_book, send_email_to_user
from internal.database.users import ban_user, unban_user
from internal.database.books import delete_book_by_id, remove_book_from_notify_lists, clear_books_from_user


router = APIRouter(prefix="/admin")


@router.get("/users", response_model=PaginatedUserPreviewListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    q: Optional[str] = Query(None, min_length=1),
    only_with_penalties: bool = Query(False),
    only_banned: bool = Query(False),
    admin=Depends(get_current_admin)
):
    all_users: List[User] = await get_all_users()
    q_lower = q.lower() if q else None
    filtered_users: List[User] = []

    if q_lower:
        exact_username_matches = [user for user in all_users if user.username.lower() == q_lower]

        if exact_username_matches:
            filtered_users = exact_username_matches
        else:
            exact_email_matches = [user for user in all_users if user.email.lower() == q_lower]
            if exact_email_matches:
                filtered_users = exact_email_matches
            else:
                threshold = 60
                for user in all_users:
                    username_match = fuzz.partial_ratio(q_lower, user.username.lower())
                    email_match = fuzz.partial_ratio(q_lower, user.email.lower())
                    if max(username_match, email_match) >= threshold:
                        filtered_users.append(user)
    else:
        filtered_users = all_users

    if only_with_penalties:
        filtered_users = [user for user in filtered_users if user.penalties and len(user.penalties) > 0]

    if only_banned:
        filtered_users = [user for user in filtered_users if user.banned]

    total_users = len(filtered_users)
    last_page = (total_users + limit - 1) // limit
    page = min(page, last_page) if last_page > 0 else 1
    start = (page - 1) * limit
    end = start + limit

    paginated_users = filtered_users[start:end]

    user_previews = [
        UserPreview(
            id=user.id,
            username=user.username,
            email=user.email,
            borrow_count=len(user.borrowed_books or []),
            penalty_fee=sum(p.amount for p in user.penalties or []),
            has_penalty=bool(user.penalties and len(user.penalties) > 0),
            banned=user.banned
        )
        for user in paginated_users
    ]

    return PaginatedUserPreviewListResponse(
        code=SUCCESS,
        message="Users retrieved successfully",
        users=user_previews,
        total=total_users,
        page=page,
        has_next=end < total_users and page < last_page,
        last_page=last_page
    )


@router.get("/users/{user_id}", response_model=PublicUserResponse)
async def get_user_details(user_id: str, admin=Depends(get_current_admin)):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="User not found"
            ))
        )

    return PublicUserResponse(
        code=SUCCESS,
        message="User details retrieved successfully",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            borrowed_books=user.borrowed_books,
            borrowed_history=user.borrowed_history,
            overdue_books=user.overdue_books,
            requested_books=user.requested_books,
            notify_me_list=user.notify_me_list,
            penalties=user.penalties,
            banned=user.banned
        )
    )


@router.post("/ban/{user_id}", response_model=SuccessResponse)
async def ban_user_endpoint(user_id: str, admin=Depends(get_current_admin)):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="User not found"
            ))
        )

    if user.borrowed_books and len(user.borrowed_books) > 0:
        return SuccessResponse(
            code=NEED_ACTION,
            message="User has active borrowed books. Hard-ban required."
        )

    # Safe to ban
    if not await ban_user(user_id):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Failed to ban the user"
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="User banned successfully"
    )


@router.post("/hard-ban/{user_id}", response_model=SuccessResponse)
async def hard_ban_user_endpoint(user_id: str, admin=Depends(get_current_admin)):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    book_ids = list(user.borrowed_books or [])

    # 1) delete the books themselves and clean notify lists
    for book_id in book_ids:
        await delete_book_by_id(book_id)
        await remove_book_from_notify_lists(book_id)

    # 2) mark the user as banned
    if not await ban_user(user_id):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to hard-ban the user"))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="User hard-banned; borrowed books removed from library"
    )


@router.post("/unban/{user_id}", response_model=SuccessResponse)
async def unban_user_endpoint(user_id: str, admin=Depends(get_current_admin)):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    if not user.banned:
        return SuccessResponse(code=SUCCESS, message="User is not banned")

    book_ids = list(user.borrowed_books or [])
    book_ids += list(user.overdue_books or [])
    book_ids += [p.book_id for p in (user.penalties or [])]

    await clear_books_from_user(user_id, book_ids)

    if not await unban_user(user_id):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to unban the user"))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="User unbanned successfully and book references cleared"
    )


@router.post("/notify/{user_id}", response_model=SuccessResponse)
async def notify_penalty_user(user_id: str, admin=Depends(get_current_admin)):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    if not user.penalties or len(user.penalties) == 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User has no penalties"))
        )

    html = await generate_penalty_email_html(user, user.penalties)
    subject = "Library Penalty Book Reminder"

    success = await send_email_to_user(user, html, subject)

    if not success:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to send penalty email"))
        )

    return SuccessResponse(code=SUCCESS, message="Penalty reminder email sent to user.")


@router.post("/notify/{user_id}/book/{book_id}", response_model=SuccessResponse)
async def notify_penalty_user_by_book(user_id: str, book_id: str, admin=Depends(get_current_admin)):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    matching_penalty = next((p for p in (user.penalties or []) if p.book_id == book_id), None)

    if not matching_penalty:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="No penalty found for this book"))
        )

    html = await generate_penalty_email_html_for_book(user, matching_penalty)
    subject = "Penalty Reminder for Specific Book"

    success = await send_email_to_user(user, html, subject)

    if not success:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to send penalty email"))
        )

    return SuccessResponse(code=SUCCESS, message="Penalty reminder email sent for specified book.")
