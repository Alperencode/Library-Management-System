from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from rapidfuzz import fuzz
from internal.utils.utils import get_current_admin
from internal.types.responses import AdminDashboardResponse, PublicUserResponse, FailResponse
from internal.types.types import SUCCESS, FAIL
from internal.database.users import get_all_users, get_user_by_id
from internal.models.user import User, PublicUser
from internal.models.user import UserPreview, PaginatedUserPreviewListResponse
from internal.database.users import get_penalty_users_count
from internal.database.books import (
    get_borrowed_books_count,
    get_penalty_books_count,
    get_books_count
)


router = APIRouter(prefix="/admin")


@router.get("/dashboard", response_model=AdminDashboardResponse)
async def get_admin_dashboard(admin=Depends(get_current_admin)):
    borrowed_books_count = await get_borrowed_books_count()
    penalty_books_count = await get_penalty_books_count()
    penalty_users_count = await get_penalty_users_count()
    total_books_count = await get_books_count()

    return AdminDashboardResponse(
        code=SUCCESS,
        message="Dashboard statistics fetched successfully",
        borrowed_books_count=borrowed_books_count,
        penalty_books_count=penalty_books_count,
        penalty_users_count=penalty_users_count,
        total_books_count=total_books_count
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
            has_penalty=bool(user.penalties and len(user.penalties) > 0)
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
            penalties=user.penalties
        )
    )
