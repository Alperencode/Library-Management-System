from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.database.books import get_all_books, get_book_by_id
from internal.types.responses import FailResponse, BookListResponse, BookResponse
from internal.types.types import SUCCESS, FAIL
from fuzzywuzzy import fuzz

router = APIRouter()


@router.get("/books", response_model=BookListResponse)
async def list_books():
    books = await get_all_books()
    return BookListResponse(
        code=SUCCESS,
        message="Books retrieved successfully",
        books=books
    )


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: str):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found")
            )
        )
    return BookResponse(
        code=SUCCESS,
        message="Book retrieved successfully",
        book=book
    )


@router.get("/books/search/", response_model=BookListResponse)
async def search_books(q: str = Query(..., min_length=1)):
    all_books = await get_all_books()
    THRESHOLD = 60
    matched = []

    for book in all_books:
        # Check fuzzy matches across multiple fields:
        title_match = fuzz.partial_ratio(q.lower(), book.title.lower())
        author_match = max(fuzz.partial_ratio(q.lower(), author.lower()) for author in book.authors or [])
        category_match = max(fuzz.partial_ratio(q.lower(), cat.lower()) for cat in book.categories or [])
        publisher_match = fuzz.partial_ratio(q.lower(), book.publisher.lower()) if book.publisher else 0

        # Fuzzy treshold
        if any(score >= THRESHOLD for score in [title_match, author_match, category_match, publisher_match]):
            matched.append(book)

    if not matched:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="No books found for query")
            )
        )

    return BookListResponse(
        code=SUCCESS,
        message="Books found successfully",
        books=matched
    )
