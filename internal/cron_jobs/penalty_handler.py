from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from internal.database.books import get_all_borrowed_books
from internal.database.users import get_user_by_id, update_user
from internal.models.user import BookPenalty

PENALTY_AMOUNT = 10.0


async def check_penalties():
    now = datetime.now()
    borrowed_books = await get_all_borrowed_books()

    for book in borrowed_books:
        if not book.return_date or book.return_date > now:
            continue

        user = await get_user_by_id(book.currently_borrowed_by)
        if not user:
            continue

        if not user.penalties:
            user.penalties = []

        if not any(p.book_id == book.id for p in user.penalties):
            user.penalties.append(BookPenalty(book_id=book.id, amount=PENALTY_AMOUNT))

        if not user.overdue_books:
            user.overdue_books = []

        if book.id not in user.overdue_books:
            user.overdue_books.append(book.id)

        await update_user(user)


def start_cron_jobs():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_penalties, 'cron', hour=0, minute=0)
    scheduler.start()
