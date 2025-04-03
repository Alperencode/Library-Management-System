from internal.database.database import books_collection
from internal.models.book import Book
from typing import Optional, List
from bson import ObjectId


async def create_book(book: Book) -> Optional[Book]:
    if not book.isbn:
        return None

    # Check for an existing book with the same ISBN
    existing = await books_collection.find_one({"isbn": book.isbn})
    if existing:
        return None

    book_data = book.model_dump(by_alias=True)
    result = await books_collection.insert_one(book_data)
    if result.inserted_id:
        return book
    return None


async def get_book_by_id(book_id: str) -> Optional[Book]:
    book_data = await books_collection.find_one({"_id": book_id})
    return Book(**book_data) if book_data else None


async def get_book_by_isbn(isbn: str) -> Optional[Book]:
    book_data = await books_collection.find_one({"isbn": isbn})
    return Book(**book_data) if book_data else None


async def get_all_books() -> List[Book]:
    books_cursor = books_collection.find()
    books = [Book(**doc) async for doc in books_cursor]
    return books


async def update_book(book: Book) -> bool:
    book_data = book.model_dump(by_alias=True)
    result = await books_collection.update_one(
        {"_id": book.id}, {"$set": book_data}
    )
    return result.modified_count > 0


async def delete_book(book_id: str) -> bool:
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count > 0
