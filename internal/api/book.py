from rapidfuzz import fuzz
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.book import BookPreview
from internal.database.books import get_all_books, get_book_by_id
from internal.types.types import SUCCESS, FAIL
from internal.types.responses import (
    FailResponse,
    BookListResponse,
    BookResponse,
    GroupedCategoryListResponse,
    GroupedCategory,
    BookPreviewListResponse
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


@router.get("/books/search/categories", response_model=GroupedCategoryListResponse)
async def list_categories():
    books = await get_all_books()
    category_map: dict[str, set[str]] = {}

    for book in books:
        for cat in book.categories or []:
            if not cat.category:
                continue
            category = cat.category.strip()
            subcategory = cat.subcategory.strip() if cat.subcategory else None

            if category not in category_map:
                category_map[category] = set()
            if subcategory:
                category_map[category].add(subcategory)

    grouped = [
        GroupedCategory(category=cat, subcategories=sorted(subs))
        for cat, subs in sorted(category_map.items())
    ]

    return GroupedCategoryListResponse(
        code=SUCCESS,
        message="Categories grouped successfully",
        categories=grouped
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


@router.get("/books/{book_id}/related", response_model=BookPreviewListResponse)
async def related_books(book_id: str):
    original = await get_book_by_id(book_id)
    if not original:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Book not found")
            )
        )

    original_categories = {c.category.lower() for c in original.categories if c.category}
    original_isbn = original.isbn
    all_books = await get_all_books()
    related = []

    for book in all_books:
        if book.id == original.id or (original_isbn and book.isbn == original_isbn):
            continue

        for cat in book.categories or []:
            if cat.category and cat.category.lower() in original_categories:
                related.append(book)
                break

    if not related:
        threshold = 60
        for book in all_books:
            if book.id == original.id or (original_isbn and book.isbn == original_isbn):
                continue

            score = 0
            for oc in original.categories:
                for bc in book.categories or []:
                    oc_full = f"{oc.category} / {oc.subcategory}" if oc.subcategory else oc.category
                    bc_full = f"{bc.category} / {bc.subcategory}" if bc.subcategory else bc.category
                    score = max(score, fuzz.partial_ratio(oc_full.lower(), bc_full.lower()))

            if score >= threshold:
                related.append(book)

    sorted_related = sorted(related, key=lambda x: (x.borrow_count, x.added_at), reverse=True)

    previews = [
        BookPreview(
            id=book.id,
            title=book.title,
            authors=book.authors,
            categories=book.categories,
            publisher=book.publisher,
            cover_image=book.cover_image,
            borrowed=book.borrowed,
            isbn=book.isbn
        )
        for book in sorted_related
    ]

    return BookPreviewListResponse(
        code=SUCCESS,
        message="Related books retrieved successfully",
        books=previews
    )
