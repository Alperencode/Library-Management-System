from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from rapidfuzz import fuzz
from internal.utils.utils import get_current_admin
from internal.types.responses import AdminDashboardResponse, PublicUserResponse, FailResponse, SuccessResponse
from internal.types.types import SUCCESS, FAIL, NEED_ACTION
from internal.database.users import get_all_users, get_user_by_id
from internal.models.user import User, PublicUser, UserPreview, PaginatedUserPreviewListResponse
from internal.database.users import get_penalty_users_count, ban_user, unban_user
from internal.database.books import (
    get_borrowed_books_count, delete_book_by_id,
    get_penalty_books_count, remove_book_from_notify_lists,
    get_books_count, clear_books_from_user
)


router = APIRouter(prefix="/admin")


@router.get("/dashboard", response_model=AdminDashboardResponse)
async def get_admin_dashboard(admin=Depends(get_current_admin)):
    borrowed_books_count = await get_borrowed_books_count()
    penalty_books_count = await get_penalty_books_count()
    penalty_users_count = await get_penalty_users_count()
    total_books_count = await get_books_count()

    available_books_count = total_books_count - borrowed_books_count

    all_users = await get_all_users()
    total_users_count = len(all_users)

    return AdminDashboardResponse(
        code=SUCCESS,
        message="Dashboard statistics fetched successfully",
        borrowed_books_count=borrowed_books_count,
        penalty_books_count=penalty_books_count,
        penalty_users_count=penalty_users_count,
        total_books_count=total_books_count,
        available_books_count=available_books_count,
        total_users_count=total_users_count
    )


@router.get("/users", response_model=PaginatedUserPreviewListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    q: Optional[str] = Query(None, min_length=1),
    admin=Depends(get_current_admin)
):
    all_users: List[User] = await get_all_users()
    threshold = 60
    filtered_users: List[User] = []

    q_lower = q.lower() if q else None

    for user in all_users:
        if q_lower:
            username_match = fuzz.partial_ratio(q_lower, user.username.lower())
            email_match = fuzz.partial_ratio(q_lower, user.email.lower())
            if max(username_match, email_match) < threshold:
                continue

        filtered_users.append(user)

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
