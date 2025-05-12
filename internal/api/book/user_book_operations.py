from datetime import datetime, timedelta, time
from fastapi import APIRouter, Depends, Query, Response
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.utils.utils import get_current_user, get_scanned_book
from internal.utils.email import send_email_to_subscribers
from internal.database.books import get_book_by_id, update_book
from internal.database.users import update_user, get_user_by_id
from internal.types.types import SUCCESS, FAIL
from internal.models.user import User
from internal.models.book import BookPreview
from internal.types.responses import (
    FailResponse,
    SuccessResponse,
    PaginatedBookPreviewListResponse
)


router = APIRouter()


@router.get("/borrowed", response_model=PaginatedBookPreviewListResponse)
async def get_borrowed_books(
    user: User = Depends(get_current_user),
    q: Optional[str] = Query(None, min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100)
):
    return await get_previews(user.borrowed_books or [], q, page, limit)


@router.get("/borrowed/history", response_model=PaginatedBookPreviewListResponse)
async def get_borrowed_history(
    user: User = Depends(get_current_user),
    q: Optional[str] = Query(None, min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100)
):
    return await get_previews(user.borrowed_history or [], q, page, limit)


@router.get("/notify-me", response_model=PaginatedBookPreviewListResponse)
async def get_notify_me_list(
    user: User = Depends(get_current_user),
    q: Optional[str] = Query(None, min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100)
):
    return await get_previews(user.notify_me_list or [], q, page, limit)


@router.get("/borrowed/overdue-books", response_model=PaginatedBookPreviewListResponse)
async def get_overdue_books(
    user: User = Depends(get_current_user),
    q: Optional[str] = Query(None, min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100)
):
    return await get_previews(user.overdue_books or [], q, page, limit)


@router.post("/borrow/{book_id}", response_model=SuccessResponse)
async def borrow_book(
    book_id: str,
    user: User = Depends(get_current_user),
    scanned_book=Depends(get_scanned_book)
):
    if scanned_book.id != book_id:
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Scanned book ID does not match")
            )
        )

    book = scanned_book

    if book.currently_borrowed_by is not None:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book is already borrowed")
            )
        )

    book.borrow_count += 1
    book.return_date = datetime.combine((datetime.now() + timedelta(weeks=1)).date(), time(23, 59))
    book.currently_borrowed_by = user.id
    book.borrowed = True
    book.borrowed_at = datetime.now()

    updated = await update_book(book)
    if not updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to update book data.")
            )
        )

    if not user.borrowed_books:
        user.borrowed_books = []
    if book.id not in user.borrowed_books:
        user.borrowed_books.append(book.id)

    user_updated = await update_user(user)
    if not user_updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to update user data.")
            )
        )

    return SuccessResponse(
        code=SUCCESS, message=f"Book '{book.title}' borrowed successfully."
    )


@router.post("/notify-me/{book_id}", response_model=SuccessResponse)
async def notify_me(book_id: str, user: User = Depends(get_current_user)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found")
            )
        )

    if not book.borrowed:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book is already available")
            )
        )

    if user.id == book.currently_borrowed_by:
        return SuccessResponse(
            code=SUCCESS, message="You can't subscribe to book which is borrowed by you"
        )

    if user.id in book.notify_me_list:
        return SuccessResponse(
            code=SUCCESS, message="You have already subscribed."
        )

    book.notify_me_list.append(user.id)
    user.notify_me_list.append(book.id)

    user_updated = await update_user(user)
    book_updated = await update_book(book)
    if not book_updated or not user_updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to update book or user data.")
            )
        )

    return SuccessResponse(
        code=SUCCESS, message=f"Subscribed to notifications for '{book.title}'."
    )


@router.post("/return/{book_id}", response_model=SuccessResponse)
async def return_book(
    book_id: str,
    user: User = Depends(get_current_user),
    scanned_book=Depends(get_scanned_book)
):
    if scanned_book.id != book_id:
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Scanned book ID does not match")
            )
        )

    book = scanned_book

    if book.currently_borrowed_by != user.id:
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Not borrowed by you.")
            )
        )

    if user.penalties:
        for penalty in user.penalties:
            if penalty.book_id == book.id and penalty.amount > 0:
                return JSONResponse(
                    status_code=403,
                    content=jsonable_encoder(
                        FailResponse(
                            code=FAIL,
                            message="You have a penalty on this book." +
                            " Please contact the library staff to return it."
                        )
                    )
                )

    book.borrowed = False
    book.currently_borrowed_by = None
    book.last_borrowed_by = user.id
    book.return_date = None

    if book.notify_me_list:
        for user_id in book.notify_me_list:
            subject = f"Book '{book.title}' is now available"
            sub_user = await get_user_by_id(user_id)
            success = await send_email_to_subscribers(sub_user, book, subject)
            if success:
                sub_user.notify_me_list.remove(book_id)
                sub_user_updated = await update_user(sub_user)
            if sub_user_updated:
                book.notify_me_list.remove(user_id)

    updated_book = await update_book(book)
    if not updated_book:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to update book data.")
            )
        )

    if user.borrowed_books and book.id in user.borrowed_books:
        user.borrowed_books.remove(book.id)
    if user.overdue_books and book.id in user.overdue_books:
        user.overdue_books.remove(book.id)
    if not user.borrowed_history:
        user.borrowed_history = []
    if book.id not in user.borrowed_history:
        user.borrowed_history.append(book.id)

    updated_user = await update_user(user)
    if not updated_user:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to update user data.")
            )
        )

    return SuccessResponse(
        code=SUCCESS, message=f"You have returned '{book.title}' successfully."
    )


@router.post("/extend-return/{book_id}", response_model=SuccessResponse)
async def extend_return(book_id: str, user: User = Depends(get_current_user)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found")
            )
        )

    if book.currently_borrowed_by != user.id:
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Not borrowed by you.")
            )
        )

    if user.penalties:
        for penalty in user.penalties:
            if penalty.book_id == book.id and penalty.amount > 0:
                return JSONResponse(
                    status_code=403,
                    content=jsonable_encoder(
                        FailResponse(
                            code=FAIL,
                            message="You have a penalty on this book." +
                            " Please contact the library staff to return it."
                        )
                    )
                )

    if book.has_extended:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Already extended once.")
            )
        )

    if not book.return_date:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="No return date found.")
            )
        )

    book.return_date = (book.return_date + timedelta(days=5)).replace(hour=23, minute=59, second=0)
    book.has_extended = True
    updated_book = await update_book(book)

    if not updated_book:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to update book data.")
            )
        )

    return SuccessResponse(
        code=SUCCESS,
        message=f"Return date extended by 5 days for '{book.title}'."
    )


@router.delete("/notify-me/{book_id}", response_model=SuccessResponse)
async def remove_notify_me(book_id: str, user: User = Depends(get_current_user)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found")
            )
        )

    if user.id in book.notify_me_list:
        book.notify_me_list.remove(user.id)

    if book_id in user.notify_me_list:
        user.notify_me_list.remove(book_id)

    book_updated = await update_book(book)
    user_updated = await update_user(user)

    if not book_updated or not user_updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL, message="Failed to update user or book data"
            ))
        )

    return SuccessResponse(
        code=SUCCESS, message="You have unsubscribed from notifications for this book"
    )


@router.post("/remove-scanned", response_model=SuccessResponse)
async def logout_user(response: Response):
    response.delete_cookie("scanned_book")
    return SuccessResponse(code=SUCCESS, message="Successfully removed the scanned_book")


def filter_books(books, q: Optional[str]):
    if not q:
        return books
    q_lower = q.lower()
    return [
        book for book in books
        if (
            q_lower in book.title.lower()
            or any(q_lower in author.lower() for author in book.authors)
            or (book.publisher and q_lower in book.publisher.lower())
        )
    ]


def paginate_books(books, page: int, limit: int):
    total = len(books)
    last_page = (total + limit - 1) // limit
    page = min(page, last_page) if last_page > 0 else 1
    start = (page - 1) * limit
    end = start + limit
    return books[start:end], total, last_page, page, end < total and page < last_page


async def get_previews(book_ids, q: Optional[str], page: int, limit: int):
    books = []
    for book_id in book_ids:
        book = await get_book_by_id(book_id)
        if book:
            books.append(book)

    filtered = filter_books(books, q)
    paginated, total, last_page, page, has_next = paginate_books(filtered, page, limit)

    previews = [
        BookPreview(
            id=book.id,
            title=book.title,
            authors=book.authors,
            categories=book.categories,
            publisher=book.publisher,
            cover_image=book.cover_image,
            borrowed=book.borrowed,
            isbn=book.isbn,
            borrowed_at=book.borrowed_at,
            return_date=book.return_date,
            currently_borrowed_by=book.currently_borrowed_by
        ) for book in paginated
    ]

    return PaginatedBookPreviewListResponse(
        code=SUCCESS,
        message="Books retrieved successfully",
        books=previews,
        total=total,
        page=page,
        last_page=last_page,
        has_next=has_next
    )
