import requests
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus
from internal.models.book import Book
from datetime import datetime


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
                if volume_id and title:
                    results.append({
                        "id": volume_id,
                        "title": title,
                        "authors": authors,
                        "categories": categories
                    })
            if results:
                return results
        except requests.RequestException:
            continue

    return []


def fetch_google_book(volume_id: str) -> Optional[Book]:
    url = f"{GOOGLE_BOOKS_API_URL}/{volume_id}"
    print(url)
    response = requests.get(url, timeout=10)
    print(response)
    if response.status_code != 200:
        return None

    data = response.json()
    info = data.get("volumeInfo")
    if not info:
        return None

    return Book(
        title=info.get("title"),
        authors=info.get("authors", []),
        categories=info.get("categories", []),
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
        available_copies=1,
        total_copies=1,
        last_borrowed_by=None
    )


def _extract_isbn(identifiers: List[Dict[str, str]]) -> Optional[str]:
    for ident in identifiers:
        if ident.get("type") in ("ISBN_13", "ISBN_10"):
            return ident.get("identifier")
    return None


def _extract_cover_image(links: Optional[Dict[str, str]]) -> Optional[str]:
    if not links:
        return None
    return links.get("thumbnail") or links.get("smallThumbnail")
