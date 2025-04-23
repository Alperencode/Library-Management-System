from datetime import datetime, timedelta, time
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.utils.utils import get_current_user, send_email_to_subscribers, get_scanned_book
from internal.database.books import get_book_by_id, update_book
from internal.database.users import update_user, get_user_by_id
from internal.types.types import SUCCESS, FAIL
from internal.models.user import User
from internal.models.book import BookPreview
from internal.types.responses import (
    FailResponse,
    BookPreviewListResponse,
    SuccessResponse
)


router = APIRouter()


@router.get("/borrowed", response_model=BookPreviewListResponse)
async def get_borrowed_books(user: User = Depends(get_current_user)):
    if not user.borrowed_books:
        return BookPreviewListResponse(
            code=SUCCESS, message="No borrowed books found", books=[]
        )

    previews = []
    for book_id in user.borrowed_books:
        book = await get_book_by_id(book_id)
        if not book:
            continue

        previews.append(
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
            )
        )

    return BookPreviewListResponse(
        code=SUCCESS,
        message="Borrowed books retrieved successfully",
        books=previews
    )


@router.get("/borrowed/history", response_model=BookPreviewListResponse)
async def get_borrowed_history(user: User = Depends(get_current_user)):
    if not user.borrowed_history:
        return BookPreviewListResponse(
            code=SUCCESS, message="No borrowed history found", books=[]
        )

    previews = []

    for book_id in user.borrowed_history:
        book = await get_book_by_id(book_id)
        if not book:
            continue

        previews.append(
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
            )
        )

    return BookPreviewListResponse(
        code=SUCCESS,
        message="Borrowed history retrieved successfully",
        books=previews
    )


@router.get("/notify-me", response_model=BookPreviewListResponse)
async def get_notify_me_list(user: User = Depends(get_current_user)):
    if not user.notify_me_list:
        return BookPreviewListResponse(
            code=SUCCESS, message="No books found to notify", books=[]
        )

    previews = []
    for book_id in user.notify_me_list:
        book = await get_book_by_id(book_id)
        if not book:
            continue

        previews.append(
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
            )
        )

    return BookPreviewListResponse(
        code=SUCCESS,
        message="Notify me list retrieved successfully",
        books=previews
    )


@router.get("/borrowed/overdue-books", response_model=BookPreviewListResponse)
async def get_overdue_books(user: User = Depends(get_current_user)):
    if not user.overdue_books:
        return BookPreviewListResponse(
            code=SUCCESS, message="No overdue books found", books=[]
        )

    previews = []
    for book_id in user.overdue_books:
        book = await get_book_by_id(book_id)
        if not book:
            continue

        previews.append(
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
            )
        )

    return BookPreviewListResponse(
        code=SUCCESS,
        message="Overdue books retrieved successfully",
        books=previews
    )


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

    if book.available_copies < 1:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="No copies available")
            )
        )

    book.borrow_count += 1
    book.return_date = datetime.combine((datetime.now() + timedelta(weeks=1)).date(), time(23, 59))
    book.currently_borrowed_by = user.id
    book.available_copies -= 1
    if book.available_copies < 1:
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

    book.available_copies += 1
    if book.available_copies >= book.total_copies:
        book.borrowed = False
    book.currently_borrowed_by = None
    book.last_borrowed_by = user.id
    book.return_date = None

    if book.available_copies > 0 and book.notify_me_list:
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
