from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from internal.database.books import get_all_borrowed_books, get_book_by_id, update_book
from internal.database.users import get_user_by_id, update_user
from internal.models.user import BookPenalty
from config.config import get_config


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
            user.penalties.append(BookPenalty(book_id=book.id, amount=get_config("penalty_amount")))

        if not user.overdue_books:
            user.overdue_books = []

        if book.id not in user.overdue_books:
            user.overdue_books.append(book.id)

        book = await get_book_by_id(book.id)
        if not book.has_penalty:
            book.has_penalty = bool
        book.has_penalty = True

        await update_user(user)
        await update_book(book)


def start_cron_jobs():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_penalties, 'cron', hour=0, minute=0)
    scheduler.start()
