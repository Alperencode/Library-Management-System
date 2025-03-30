from typing import List
from pydantic import BaseModel, Field
from internal.models.user import PublicUser
from internal.models.book import Book, BookPreview, ExternalBookPreview


class SuccessResponse(BaseModel):
    code: str = Field(None, examples=["Success"])
    message: str = Field(None, examples=["message"])


class FailResponse(BaseModel):
    code: str = Field(None, examples=["Fail"])
    message: str = Field(None, examples=["message"])


class VersionResponse(SuccessResponse):
    version: str = Field(None, examples=["v0.1.0"])


class PublicUserResponse(SuccessResponse):
    user: PublicUser = Field(None, examples=[{
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "username": "test",
            "email": "test@example.com",
            "role": "user",
        }]
    )


class TokenResponse(SuccessResponse):
    access_token: str = Field(None, examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(None, examples=["bearer"])


class BookResponse(SuccessResponse):
    book: Book = Field(...)


class BookListResponse(SuccessResponse):
    books: list[Book] = Field(default_factory=list)


class BookPreviewListResponse(SuccessResponse):
    books: List[BookPreview]


class ExternalBookListResponse(SuccessResponse):
    books: list[ExternalBookPreview] = Field(None)


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
