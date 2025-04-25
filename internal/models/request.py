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


class RequesterInfo(BaseModel):
    id: str
    username: str
    email: str


class RequestDetails(BaseModel):
    id: str
    title: Optional[str]
    authors: Optional[List[str]]
    isbn: Optional[str]
    publisher: Optional[str]
    cover_image: Optional[str]
    status: str
    requested_at: Optional[datetime]
    status_updated_at: Optional[datetime]


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
    requested_at: datetime
    status_updated_at: datetime
