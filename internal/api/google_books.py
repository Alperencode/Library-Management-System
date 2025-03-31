import asyncio
from fastapi import APIRouter, Query, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.database.books import create_book, get_book_by_isbn
from internal.types.types import SUCCESS, FAIL
from internal.utils.google_books import search_google_books, fetch_google_book
from internal.models.book import BookPreview
from internal.types.responses import (
    FailResponse,
    BookResponse,
    ExternalBookListResponse,
    BulkExternalBookAddResponse
)

router = APIRouter()


@router.get("/google-books/search", response_model=ExternalBookListResponse)
async def search_books_external(q: str = Query(..., min_length=1)):
    results = search_google_books(q)
    if not results:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="No books found from external source")
            )
        )

    books = [
        BookPreview(
            id=item["id"],
            title=item["title"],
            authors=item["authors"],
            categories=item["categories"],
        )
        for item in results
    ]

    return ExternalBookListResponse(
        code=SUCCESS,
        message="Books found via external search",
        books=books
    )


@router.post("/google-books/add", response_model=BookResponse)
async def add_book_from_external(volume_id: str = Body(..., embed=True)):
    book = fetch_google_book(volume_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found or incomplete from external source")
            )
        )

    created = await create_book(book)
    if not created:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Failed to insert book into database")
            )
        )

    return BookResponse(
        code=SUCCESS,
        message="Book added successfully from external source",
        book=created
    )


@router.post("/google-books/add/bulk", response_model=BulkExternalBookAddResponse)
async def bulk_add_books_from_external(
    isbns: list[str] = Body(..., embed=True)
):
    created_books = []
    failed_isbns = []

    for isbn in isbns:
        exists = await get_book_by_isbn(isbn)
        if exists:
            continue

        # Add small delay
        await asyncio.sleep(0.3)
        matches = search_google_books(isbn)
        if not matches:
            failed_isbns.append(isbn)
            continue

        volume_id = matches[0]["id"]
        book = fetch_google_book(volume_id)
        if not book:
            failed_isbns.append(isbn)
            continue

        created = await create_book(book)
        if not created:
            failed_isbns.append(isbn)
            continue

        created_books.append(
            BookPreview(
                id=created.id,
                title=created.title,
                authors=created.authors,
                categories=created.categories,
            )
        )

    return BulkExternalBookAddResponse(
        code=SUCCESS if created_books else FAIL,
        message="Books added successfully from external source"
        if created_books else "No books were added",
        success_count=len(created_books),
        failed_count=len(failed_isbns),
        failed_isbns=failed_isbns
    )
