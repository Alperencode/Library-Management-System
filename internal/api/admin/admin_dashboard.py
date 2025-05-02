from fastapi import APIRouter, Depends
from internal.utils.utils import get_current_admin
from internal.types.responses import AdminDashboardResponse
from internal.types.types import SUCCESS
from internal.database.users import get_all_users
from internal.database.users import get_penalty_users_count
from internal.database.books import get_borrowed_books_count, get_penalty_books_count, get_books_count

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

    total_penalty_fee = sum(
        p.amount for user in all_users for p in (user.penalties or [])
    )

    return AdminDashboardResponse(
        code=SUCCESS,
        message="Dashboard statistics fetched successfully",
        borrowed_books_count=borrowed_books_count,
        penalty_books_count=penalty_books_count,
        penalty_users_count=penalty_users_count,
        total_books_count=total_books_count,
        available_books_count=available_books_count,
        total_users_count=total_users_count,
        total_penalty_fee=total_penalty_fee
    )
