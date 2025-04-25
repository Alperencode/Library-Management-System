from pydantic import EmailStr, Field, BaseModel
from typing import Optional


SUCCESS = "Success"
FAIL = "Fail"
NEED_ACTION = "NeedAction"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(None, examples=["123"])
    remember_me: bool = False


class UserRequest(BaseModel):
    email: EmailStr
    username: str = Field(None, examples=["example"])
    password: str = Field(None, examples=["123"])


class AdminRequest(BaseModel):
    username: str
    email: str
    password: str


class AdminUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, examples=["admin"])
    password: Optional[str] = Field(None, examples=["123"])


class IDRequest(BaseModel):
    id: str = Field(None, examples=["67cdec2c6cd51597b698e636"])


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, examples=["example"])
    password: Optional[str] = Field(None, examples=["123"])


class LanguageItem(BaseModel):
    Language: str
    Key: str
