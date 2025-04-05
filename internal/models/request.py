from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookRequest(BaseModel):
    id: str
    title: str
    authors: list[str]
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    status: str = "Request Sent"
    requested_at: datetime = Field(default_factory=datetime.now)
