from pydantic import EmailStr, Field, BaseModel
from internal.models.user import User

SUCCESS = "Success"
FAIL = "Fail"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


class RefreshTokenRequest(BaseModel):
    user: User = Field(None, examples=[{
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "username": "test",
            "email": "test@example.com",
            "role": "user",
            "refresh_token": ""
        }]
    )


class UserRequest(BaseModel):
    user: User = Field(None, examples=[{
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "username": "test",
            "email": "test@example.com",
            "role": "user",
            "refresh_token": ""
        }]
    )
