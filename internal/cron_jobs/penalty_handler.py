from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from internal.database.books import get_all_borrowed_books, get_book_by_id, update_book
from internal.database.users import get_user_by_id, update_user
from internal.models.user import BookPenalty
from config.config import get_config


async def check_penalties():
    now = datetime.now()
    borrowed_books = await get_all_borrowed_books()

    penalty_per_day = get_config("penalty_amount")

    for book in borrowed_books:
        if not book.return_date or book.return_date > now:
            continue

        user = await get_user_by_id(book.currently_borrowed_by)
        if not user:
            continue

        overdue_days = (now - book.return_date).days
        if overdue_days <= 0:
            continue

        total_penalty = overdue_days * penalty_per_day

        if not user.penalties:
            user.penalties = []

        existing_penalty = next((p for p in user.penalties if p.book_id == book.id), None)
        if existing_penalty:
            existing_penalty.amount = total_penalty
        else:
            user.penalties.append(BookPenalty(book_id=book.id, amount=total_penalty))

        if not user.overdue_books:
            user.overdue_books = []

        if book.id not in user.overdue_books:
            user.overdue_books.append(book.id)

        book = await get_book_by_id(book.id)
        if book and not book.has_penalty:
            book.has_penalty = True

        await update_user(user)
        await update_book(book)


def start_cron_jobs():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_penalties, 'cron', hour=0, minute=0)
    scheduler.start()
