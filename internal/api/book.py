from rapidfuzz import fuzz
from fastapi import APIRouter, Query, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.database.books import get_all_books, get_book_by_id, create_book
from internal.types.types import SUCCESS, FAIL
from internal.utils.google_books import search_google_books, fetch_google_book
from internal.models.book import ExternalBookPreview
from internal.types.responses import (
    FailResponse,
    BookListResponse,
    BookResponse,
    CategoryListResponse,
    ExternalBookListResponse
)

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
    threshold = 60
    matched = []

    for book in all_books:
        # Check fuzzy matches across multiple fields:
        title_match = fuzz.partial_ratio(q.lower(), book.title.lower())
        author_match = max(fuzz.partial_ratio(q.lower(), author.lower()) for author in book.authors or [])
        category_match = max(fuzz.partial_ratio(q.lower(), cat.lower()) for cat in book.categories or [])
        publisher_match = fuzz.partial_ratio(q.lower(), book.publisher.lower()) if book.publisher else 0

        # Fuzzy treshold
        if any(score >= threshold for score in [title_match, author_match, category_match, publisher_match]):
            matched.append(book)

    if not matched:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="No books found for the query")
            )
        )

    return BookListResponse(
        code=SUCCESS,
        message="Books found successfully",
        books=matched
    )


@router.get("/books/search/categories", response_model=CategoryListResponse)
async def list_categories():
    books = await get_all_books()
    categories_set = set()
    for book in books:
        categories_set.update(book.categories or [])
    return CategoryListResponse(
        code=SUCCESS,
        message="Categories retrieved successfully",
        categories=sorted(categories_set)
    )


@router.get("/books/search/popular", response_model=BookListResponse)
async def list_popular_books():
    books = await get_all_books()
    sorted_books = sorted(books, key=lambda x: (x.borrow_count, x.added_at), reverse=True)
    return BookListResponse(
        code=SUCCESS,
        message="Popular books retrieved successfully",
        books=sorted_books
    )


@router.get("/books/{book_id}/related", response_model=BookListResponse)
async def related_books(book_id: str):
    original = await get_book_by_id(book_id)
    if not original:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found")
            )
        )

    # TO-DO: Get only category matched books in future
    books = await get_all_books()
    threshold = 60
    related = []

    for book in books:
        if book.id == original.id:
            continue

        # First, try to match category.
        category_match = any(cat in original.categories for cat in book.categories)

        # If category doesn't matches, try to fuzzy match
        if not category_match:
            fuzzy_score = max(
                fuzz.partial_ratio(cat1.lower(), cat2.lower())
                for cat1 in original.categories for cat2 in book.categories
            ) if book.categories and original.categories else 0

            if fuzzy_score >= threshold:
                related.append(book)
        else:
            related.append(book)

    sorted_related = sorted(related, key=lambda x: (x.borrow_count, x.added_at), reverse=True)
    return BookListResponse(
        code=SUCCESS,
        message="Related books retrieved successfully",
        books=sorted_related
    )


@router.get("/books/search/external", response_model=ExternalBookListResponse)
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
        ExternalBookPreview(
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


@router.post("/books/add/external", response_model=BookResponse)
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
