from pydantic import EmailStr, Field, BaseModel
from internal.models.user import User

SUCCESS = "Success"
FAIL = "Fail"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserRequest(BaseModel):
    email: EmailStr
    username: str = Field(None, examples=["example"])
    password: str = Field(None, examples=["example123"])


class RefreshTokenRequest(BaseModel):
    user: User = Field(None, examples=[{
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "username": "test",
            "email": "test@example.com",
            "role": "user",
        }]
    )
