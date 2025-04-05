from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
from .request import BookRequest
import bcrypt


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    username: str
    email: str
    password: str
    role: str
    borrowed_books: Optional[List[str]] = []
    borrowed_history: Optional[List[str]] = []
    overdue_books: Optional[List[str]] = []
    requested_books: Optional[list[BookRequest]] = None
    notify_me_list: Optional[List[str]] = []
    penalty_amount: Optional[str] = []

    def check_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.password.encode())

    def __setattr__(self, name, value):
        if name == "id" and hasattr(self, "id"):
            raise AttributeError("The 'id' field is immutable and cannot be changed after creation.")
        super().__setattr__(name, value)


class PublicUser(BaseModel):
    id: str
    username: str
    email: str
    role: str
    borrowed_books: Optional[List[str]] = []
    borrowed_history: Optional[List[str]] = []
    overdue_books: Optional[List[str]] = []
    requested_books: Optional[list[BookRequest]] = None
    notify_me_list: Optional[List[str]] = []
    penalty_amount: Optional[str] = []
