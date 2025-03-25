from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime


class Book(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: str
    authors: List[str]
    categories: List[str]
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
    updated_at: datetime = Field(default_factory=datetime.now)
    available_copies: int = 1
    total_copies: int = 1
    last_borrowed_by: Optional[str] = None

    def __setattr__(self, name, value):
        if name == "id" and hasattr(self, "id"):
            raise AttributeError(
                "The 'id' field is immutable and cannot be changed after creation."
            )
        super().__setattr__(name, value)


class ExternalBookPreview(BaseModel):
    id: str
    title: str
    authors: List[str]
    categories: List[str]
