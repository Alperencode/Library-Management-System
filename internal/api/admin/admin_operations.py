from fastapi import APIRouter, Depends
from internal.utils.utils import get_current_admin
from internal.types.responses import AdminDashboardResponse
from internal.types.types import SUCCESS
from internal.database.books import (
    get_borrowed_books_count,
    get_penalty_books_count,
    get_books_count
)
from internal.database.users import get_penalty_users_count

router = APIRouter()


@router.get("admin/dashboard", response_model=AdminDashboardResponse)
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
