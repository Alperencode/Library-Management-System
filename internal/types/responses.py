from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    code: str = Field(None, examples=["Success"])
    message: str = Field(None, examples=["message"])


class FailResponse(BaseModel):
    code: str = Field(None, examples=["Fail"])
    message: str = Field(None, examples=["message"])
