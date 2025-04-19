from fastapi import HTTPException
from .types import FAIL


class FailResponseException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail={"code": FAIL, "message": message})
