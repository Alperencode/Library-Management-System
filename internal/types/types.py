from pydantic import EmailStr, Field
from fastapi import Request
from internal.models.user import User

SUCCESS = "Success"
FAIL = "Fail"


class LoginRequest(Request):
    email: EmailStr
    password: str
    remember_me: bool = False


class RegisterRequest(Request):
    email: EmailStr
    name: str
    password: str


class RefreshTokenRequest(Request):
    user: User = Field(None, examples=[{
            "username": "test",
            "email": "test@example.com",
            "password": "test123",
            "role": "user"
        }]
    )


class UserRequest(Request):
    user: User = Field(None, examples=[{
            "username": "test",
            "email": "test@example.com",
            "password": "test123",
            "role": "user"
        }]
    )
