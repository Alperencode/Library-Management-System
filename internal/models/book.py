from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime


class BookCategory(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None


class BookPenalty(BaseModel):
    book_id: str
    amount: float


class Book(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: str
    authors: List[str]
    categories: List[BookCategory]
    language: Optional[str] = None
    page_count: Optional[int] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    borrowed: bool = False
    borrow_count: int = 0
    return_date: Optional[datetime] = None
    added_at: datetime = Field(default_factory=datetime.now)
    borrowed_at: datetime = Field(default_factory=datetime.now)
    currently_borrowed_by: Optional[str] = None
    last_borrowed_by: Optional[str] = None
    notify_me_list: List[str] = []
    has_extended: bool = False
    has_penalty: bool = False

    def __setattr__(self, name, value):
        if name == "id" and hasattr(self, "id"):
            raise AttributeError(
                "The 'id' field is immutable and cannot be changed after creation."
            )
        super().__setattr__(name, value)


class BookPreview(BaseModel):
    id: str
    title: str
    authors: List[str]
    categories: List[BookCategory]
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    borrowed: bool = False
    isbn: Optional[str] = None
    borrowed_at: Optional[datetime] = None
    return_date: Optional[datetime] = None
    has_penalty: bool = False
    currently_borrowed_by: Optional[str] = None


class BorrowedBookPreview(BaseModel):
    id: str
    title: str
    authors: List[str]
    publisher: Optional[str]
    cover_image: Optional[str]
    borrowed: bool
    isbn: Optional[str]
    borrowed_at: datetime
    return_date: datetime
    currently_borrowed_by: Optional[str]


class BookCreate(BaseModel):
    title: str
    authors: List[str]
    categories: List[BookCategory]
    language: Optional[str] = None
    page_count: Optional[int] = None
    isbn: str
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None


class BookEdit(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    categories: Optional[List[BookCategory]] = None
    language: Optional[str] = None
    page_count: Optional[int] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
