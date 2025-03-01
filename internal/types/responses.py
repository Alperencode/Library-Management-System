from pydantic import BaseModel, Field
from internal.models.user import User


class SuccessResponse(BaseModel):
    code: str = Field(None, examples=["Success"])
    message: str = Field(None, examples=["message"])


class FailResponse(BaseModel):
    code: str = Field(None, examples=["Fail"])
    message: str = Field(None, examples=["message"])


class VersionResponse(SuccessResponse):
    version: str = Field(None, examples=["v0.1.0"])


class UserResponse(SuccessResponse):
    user: User = Field(None, examples=[{
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "username": "test",
            "email": "test@example.com",
            "password": "test123",
            "role": "user",
            "refresh_token": ""
        }]
    )
