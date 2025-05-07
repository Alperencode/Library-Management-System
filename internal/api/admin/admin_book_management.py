from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.database.books import get_book_by_isbn, get_book_by_id, delete_book_by_id, remove_book_from_notify_lists
from internal.database.users import get_all_users, update_user
from internal.utils.utils import get_current_admin
from internal.types.types import SUCCESS, FAIL
from internal.database.books import create_book, update_book
from internal.models.book import Book, BookCreate, BookEdit
from internal.types.responses import SuccessResponse, FailResponse, BookResponse

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


@router.post("/book", response_model=SuccessResponse)
async def add_book(book_data: BookCreate, admin=Depends(get_current_admin)):
    if not book_data.authors or len(book_data.authors) == 0:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(code=FAIL, message="At least one author is required"))
        )

    if not book_data.categories or not any(c.category.strip() for c in book_data.categories):
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(code=FAIL, message="At least one valid category is required"))
        )

    if book_data.isbn:
        existing = await get_book_by_isbn(book_data.isbn)
        if existing:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(FailResponse(code=FAIL, message="A book with the same ISBN already exists"))
            )

    book = Book(**book_data.model_dump())
    created = await create_book(book)

    if not created:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to create book"))
        )

    return SuccessResponse(code=SUCCESS, message=f"Book '{book.title}' added successfully")


@router.patch("/book/{book_id}", response_model=SuccessResponse)
async def patch_book(book_id: str, book_data: BookEdit, admin=Depends(get_current_admin)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    updates = book_data.model_dump(exclude_unset=True)

    # Check ISBN duplication if provided
    if "isbn" in updates and updates["isbn"] != book.isbn:
        existing = await get_book_by_isbn(updates["isbn"])
        if existing:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(FailResponse(code=FAIL, message="ISBN already exists"))
            )

    for key, value in updates.items():
        setattr(book, key, value)

    saved = await update_book(book)
    if not saved:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to update book"))
        )

    return SuccessResponse(code=SUCCESS, message=f"Book '{book.title}' updated successfully")


@router.delete("/book/{book_id}", response_model=SuccessResponse)
async def delete_book(book_id: str = Path(...), admin=Depends(get_current_admin)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    # Remove book references from all users
    users = await get_all_users()
    for user in users:
        modified = False

        if book_id in (user.borrowed_books or []):
            user.borrowed_books.remove(book_id)
            modified = True

        if book_id in (user.overdue_books or []):
            user.overdue_books.remove(book_id)
            modified = True

        if book_id in (user.borrowed_history or []):
            user.borrowed_history.remove(book_id)
            modified = True

        if user.penalties:
            new_penalties = [p for p in user.penalties if p.book_id != book_id]
            if len(new_penalties) != len(user.penalties):
                user.penalties = new_penalties
                modified = True

        if book_id in (user.notify_me_list or []):
            user.notify_me_list.remove(book_id)
            modified = True

        if modified:
            await update_user(user)

    # Remove book from book collection
    deleted = await delete_book_by_id(book_id)
    if not deleted:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Failed to delete book"))
        )

    # Clean up notify lists for safety
    await remove_book_from_notify_lists(book_id)

    return SuccessResponse(
        code=SUCCESS,
        message=f"Book '{book.title}' has been deleted and references cleared."
    )
