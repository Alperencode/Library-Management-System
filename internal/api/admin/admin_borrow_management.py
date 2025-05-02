from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Path, Body, Query
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.database.books import get_all_books, get_book_by_id, update_book
from internal.database.users import get_user_by_id, update_user, get_all_users
from internal.models.book import BorrowedBookPreview
from internal.utils.utils import get_current_admin
from internal.types.responses import (
    SuccessResponse,
    FailResponse,
    BorrowedBookListResponse,
    BookResponse
)
from internal.types.types import SUCCESS, FAIL
from internal.utils.email import send_email_to_subscribers
from rapidfuzz import fuzz


router = APIRouter(prefix="/admin")


@router.get("/book/{book_id}", response_model=BookResponse)
async def get_book_details(book_id: str, admin=Depends(get_current_admin)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    return BookResponse(
        code=SUCCESS,
        message="Book details retrieved successfully",
        book=book
    )


@router.get("/borrowed-books", response_model=BorrowedBookListResponse)
async def list_borrowed_books(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None),
    admin=Depends(get_current_admin)
):
    books = await get_all_books()
    users = await get_all_users()
    user_id_to_username = {user.id: user.username for user in users}

    borrowed_books: List[BorrowedBookPreview] = []

    for book in books:
        if book.borrowed and book.currently_borrowed_by:
            borrowed_books.append(
                BorrowedBookPreview(
                    id=book.id,
                    title=book.title,
                    authors=book.authors,
                    publisher=book.publisher,
                    cover_image=book.cover_image,
                    borrowed=True,
                    isbn=book.isbn,
                    borrowed_at=book.borrowed_at,
                    return_date=book.return_date,
                    currently_borrowed_by=book.currently_borrowed_by
                )
            )

    if q:
        q_lower = q.strip().lower()

        # First: check exact username match
        matched_user_ids = [
            user_id for user_id, username in user_id_to_username.items()
            if username.lower() == q_lower
        ]

        if matched_user_ids:
            borrowed_books = [
                book for book in borrowed_books
                if book.currently_borrowed_by in matched_user_ids
            ]
        else:
            filtered = []
            for book in borrowed_books:
                title = (book.title or "").lower()
                isbn = (book.isbn or "").lower()
                authors = ", ".join(book.authors or []).lower()
                publisher = (book.publisher or "").lower()

                if fuzz.partial_ratio(q_lower, title) >= 70:
                    filtered.append(book)
                elif fuzz.partial_ratio(q_lower, isbn) >= 70:
                    filtered.append(book)
                elif fuzz.partial_ratio(q_lower, authors) >= 70:
                    filtered.append(book)
                elif fuzz.partial_ratio(q_lower, publisher) >= 70:
                    filtered.append(book)

            borrowed_books = filtered

    total = len(borrowed_books)
    last_page = (total + limit - 1) // limit
    page = min(page, last_page) if last_page else 1
    start, end = (page - 1) * limit, page * limit

    return BorrowedBookListResponse(
        code=SUCCESS,
        message="Borrowed books retrieved",
        books=borrowed_books[start:end],
        total=total,
        page=page,
        has_next=end < total and page < last_page,
        last_page=last_page
    )


@router.patch("/borrowed-books/{book_id}", response_model=SuccessResponse)
async def update_borrowed_book(
    book_id: str = Path(...),
    return_date: str = Body(..., embed=True),
    admin=Depends(get_current_admin)
):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    try:
        book.return_date = datetime.strptime(return_date, "%Y-%m-%d")
    except ValueError:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Invalid return_date format. Expected YYYY-MM-DD.",
            ))
        )
    updated = await update_book(book)

    if not updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to update book"))
        )

    return SuccessResponse(code=SUCCESS, message="Book return date updated")


@router.post("/borrowed-books/return/{book_id}", response_model=SuccessResponse)
async def admin_return_book(
    book_id: str = Path(...),
    admin=Depends(get_current_admin)
):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    if not book.borrowed or not book.currently_borrowed_by:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book is not currently borrowed"))
        )

    user = await get_user_by_id(book.currently_borrowed_by)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Borrower user not found"))
        )

    # Book updates
    book.borrowed = False
    book.currently_borrowed_by = None
    book.last_borrowed_by = user.id
    book.return_date = None

    # Notify subscribers
    if book.notify_me_list:
        for user_id in book.notify_me_list:
            sub_user = await get_user_by_id(user_id)
            if sub_user:
                subject = f"Book '{book.title}' is now available"
                await send_email_to_subscribers(sub_user, book, subject)
                if book.id in sub_user.notify_me_list:
                    sub_user.notify_me_list.remove(book.id)
                    await update_user(sub_user)
        book.notify_me_list = []

    updated_book = await update_book(book)
    if not updated_book:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to update book"))
        )

    # User updates
    if user.borrowed_books and book.id in user.borrowed_books:
        user.borrowed_books.remove(book.id)
    if user.overdue_books and book.id in user.overdue_books:
        user.overdue_books.remove(book.id)
    if not user.borrowed_history:
        user.borrowed_history = []
    if book.id not in user.borrowed_history:
        user.borrowed_history.append(book.id)

    if user.penalties:
        user.penalties = [penalty for penalty in user.penalties if penalty.book_id != book.id]

    updated_user = await update_user(user)
    if not updated_user:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to update user data"))
        )

    return SuccessResponse(
        code=SUCCESS,
        message=f"Book '{book.title}' successfully returned by admin and penalties cleared."
    )


@router.post("/borrowed-books/extend/{book_id}", response_model=SuccessResponse)
async def admin_extend_borrowed_book(
    book_id: str = Path(...),
    extra_days: int = Body(..., embed=True, ge=1),
    admin=Depends(get_current_admin)
):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    if not book.return_date:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book does not have a return date"))
        )

    book.return_date += timedelta(days=extra_days)

    updated = await update_book(book)
    if not updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to extend return date"))
        )

    return SuccessResponse(
        code=SUCCESS,
        message=f"Return date extended by {extra_days} days for '{book.title}'."
    )
