import requests
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus
from internal.models.book import Book, BookCategory
from datetime import datetime
from .logger import logger


GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
SEARCH_FIELDS = ["isbn", "intitle", "inauthor", "inpublisher"]


def search_google_books(query: str) -> List[Dict[str, Any]]:
    encoded_query = quote_plus(query)

    for field in SEARCH_FIELDS:
        search_term = f"{field}:{encoded_query}"
        params = {"q": search_term}
        try:
            response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to search the book | query={query} | status code {response.status_code}")
                continue

            data = response.json()
            items = data.get("items")
            if not items:
                continue

            results = []
            for item in items:
                volume_id = item.get("id")
                info = item.get("volumeInfo", {})
                title = info.get("title")
                authors = info.get("authors", [])
                categories = info.get("categories", [])
                publisher = info.get("publisher")
                image_links = info.get("imageLinks", {})
                cover_image = image_links.get("thumbnail") or image_links.get("smallThumbnail")
                isbn = _extract_isbn(info.get("industryIdentifiers", []))

                if volume_id and title:
                    results.append({
                        "id": volume_id,
                        "title": title,
                        "authors": authors,
                        "categories": categories,
                        "publisher": publisher,
                        "cover_image": cover_image,
                        "isbn": isbn
                    })
            if results:
                return results
        except requests.RequestException:
            continue

    return []


def fetch_google_book(volume_id: str) -> Optional[Book]:
    url = f"{GOOGLE_BOOKS_API_URL}/{volume_id}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        logger.error(f"Failed to get book information | id={volume_id} | status code {response.status_code}")
        return None

    data = response.json()
    info = data.get("volumeInfo")
    if not info:
        return None

    raw_categories = info.get("categories", [])
    categories = _parse_categories(raw_categories)

    return Book(
        title=info.get("title"),
        authors=info.get("authors", []),
        categories=categories,
        language=info.get("language"),
        page_count=info.get("pageCount"),
        isbn=_extract_isbn(info.get("industryIdentifiers", [])),
        publisher=info.get("publisher"),
        cover_image=_extract_cover_image(info.get("imageLinks")),
        description=info.get("description"),
        borrowed=False,
        borrow_count=0,
        return_date=None,
        added_at=datetime.now(),
        updated_at=datetime.now(),
        last_borrowed_by=None
    )


def _extract_isbn(identifiers: List[Dict[str, str]]) -> Optional[str]:
    for ident in identifiers:
        if ident.get("type") == "ISBN_13":
            return ident.get("identifier")
    for ident in identifiers:
        if ident.get("type") == "ISBN_10":
            return ident.get("identifier")
    return None


def _extract_cover_image(links: Optional[Dict[str, str]]) -> Optional[str]:
    if not links:
        return None
    return links.get("thumbnail") or links.get("smallThumbnail")


def _parse_categories(raw: List[str]) -> List[BookCategory]:
    max_categories = 3
    if not raw:
        return []

    structured: List[BookCategory] = []
    seen = set()

    for full in raw:
        if len(structured) >= max_categories:
            break
        parts = [p.strip() for p in full.split("/") if p.strip()]
        if not parts:
            continue

        category = parts[0]
        subcategory = parts[1] if len(parts) > 1 else None

        key = (category.lower(), subcategory.lower() if subcategory else None)
        if key in seen:
            continue

        seen.add(key)
        structured.append(BookCategory(
            category=category,
            subcategory=subcategory
        ))

    return structured
