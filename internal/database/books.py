from internal.database.database import books_collection
from internal.database.users import users_collection
from internal.models.book import Book
from typing import Optional, List


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


async def get_all_borrowed_books() -> List[Book]:
    books_cursor = books_collection.find({"borrowed": True})
    books = [Book(**doc) async for doc in books_cursor]
    return books


async def update_book(book: Book) -> bool:
    book_data = book.model_dump(by_alias=True)
    result = await books_collection.update_one(
        {"_id": book.id}, {"$set": book_data}
    )
    return result.modified_count > 0


async def get_borrowed_books_count() -> int:
    return await books_collection.count_documents({"borrowed": True})


async def get_penalty_books_count() -> int:
    return await books_collection.count_documents({"has_penalty": True})


async def get_books_count() -> int:
    return await books_collection.estimated_document_count()


async def delete_book(book_id: str) -> bool:
    result = await books_collection.delete_one({"_id": book_id})
    return result.deleted_count > 0


async def delete_book_by_id(book_id: str) -> bool:
    result = await books_collection.delete_one({"_id": book_id})
    return result.deleted_count > 0


async def remove_book_from_notify_lists(book_id: str):
    await users_collection.update_many(
        {"notify_me_list": book_id},
        {"$pull": {"notify_me_list": book_id}}
    )


async def clear_books_from_user(user_id: str, book_ids: List[str]) -> None:
    if not book_ids:
        return

    await users_collection.update_one(
        {"_id": user_id},
        {
            "$pull": {
                "borrowed_books": {"$in": book_ids},
                "overdue_books":  {"$in": book_ids},
                "penalties":     {"book_id": {"$in": book_ids}}
            }
        }
    )
