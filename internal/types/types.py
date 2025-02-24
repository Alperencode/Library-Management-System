from pydantic import BaseModel, EmailStr

SUCCESS = "Success"
FAIL = "Fail"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
