from pydantic import EmailStr, Field, BaseModel
from typing import Optional


SUCCESS = "Success"
FAIL = "Fail"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(None, examples=["example123"])
    remember_me: bool = False


class UserRequest(BaseModel):
    email: EmailStr
    username: str = Field(None, examples=["example"])
    password: str = Field(None, examples=["example123"])


class IDRequest(BaseModel):
    id: str = Field(None, examples=["67cdec2c6cd51597b698e636"])


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, examples=["example"])
    password: Optional[str] = Field(None, examples=["example123"])
