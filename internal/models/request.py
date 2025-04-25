from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RequestStatus(str, Enum):
    REQUEST_SENT = "Request Sent"
    APPROVED = "Approved"
    DENIED = "Denied"
    ADDED = "Added"
    ON_HOLD = "On Hold"


class BookRequest(BaseModel):
    id: str
    title: str
    authors: List[str]
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    cover_image: Optional[str] = None

    status: RequestStatus = RequestStatus.REQUEST_SENT
    requested_at: datetime = Field(default_factory=datetime.now)
    status_updated_at: datetime = Field(default_factory=datetime.now)


class BookRequestPreview(BaseModel):
    user_id: str
    username: str
    email: str

    id: str
    title: str
    authors: List[str]
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    status: RequestStatus = RequestStatus.REQUEST_SENT
    status_updated_at: datetime
