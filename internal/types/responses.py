from typing import List
from pydantic import BaseModel, Field
from internal.models.user import PublicUser
from internal.models.admin import PublicAdmin
from internal.models.book import Book, BookPreview, BorrowedBookPreview
from internal.models.request import BookRequest, BookRequestPreview, RequestDetails, RequesterInfo
from .types import LanguageItem


class SuccessResponse(BaseModel):
    code: str = Field(None, examples=["Success"])
    message: str = Field(None, examples=["message"])


class FailResponse(BaseModel):
    code: str = Field(None, examples=["Fail"])
    message: str = Field(None, examples=["message"])


class VersionResponse(SuccessResponse):
    version: str = Field(None, examples=["v0.1.0"])


class PublicUserResponse(SuccessResponse):
    user: PublicUser = Field(None)


class PublicAdminResponse(SuccessResponse):
    admin: PublicAdmin


class TokenResponse(SuccessResponse):
    access_token: str = Field(None, examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(None, examples=["bearer"])


class BookResponse(SuccessResponse):
    book: Book = Field(...)


class BookListResponse(SuccessResponse):
    books: list[Book] = Field(default_factory=list)


class BookPreviewListResponse(SuccessResponse):
    books: List[BookPreview]


class PaginatedBookPreviewListResponse(SuccessResponse):
    books: List[BookPreview]
    total: int
    page: int
    has_next: bool
    last_page: int


class BulkExternalBookAddResponse(BaseModel):
    code: str
    message: str
    success_count: int
    failed_count: int
    failed_isbns: List[str]


class CategoryListResponse(SuccessResponse):
    categories: list[str] = Field(default_factory=list)


class GroupedCategory(BaseModel):
    category: str
    subcategories: List[str]


class GroupedCategoryListResponse(SuccessResponse):
    categories: List[GroupedCategory]


class LanguageListResponse(SuccessResponse):
    languages: List[LanguageItem]


class BookRequestListResponse(SuccessResponse):
    books: List[BookRequest]


class AdminDashboardResponse(SuccessResponse):
    borrowed_books_count: int
    penalty_books_count: int
    penalty_users_count: int
    total_books_count: int
    available_books_count: int
    total_users_count: int
    total_penalty_fee: int


class BooksOverviewResponse(SuccessResponse):
    total_books: int
    total_users: int
    total_borrowed_books: int
    total_available_books: int


class BookRequestPreviewListResponse(SuccessResponse):
    requests: List[BookRequestPreview]
    total: int
    page: int
    has_next: bool
    last_page: int


class BookRequestDetailsResponse(SuccessResponse):
    request: RequestDetails
    requester_count: int
    requesters: List[RequesterInfo]


class BorrowedBookListResponse(SuccessResponse):
    books: List[BorrowedBookPreview]
    total: int
    page: int
    has_next: bool
    last_page: int
