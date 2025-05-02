from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.database.books import get_book_by_id
from internal.utils.utils import get_current_admin
from internal.types.types import SUCCESS, FAIL
from internal.types.responses import (
    FailResponse,
    BookResponse
)

router = APIRouter(prefix="/admin")


@router.get("/book/{book_id}", response_model=BookResponse)
async def get_book_details(book_id: str, admin=Depends(get_current_admin)):
    book = await get_book_by_id(book_id)
    if not book:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Book not found"))
        )

    return BookResponse(
        code=SUCCESS,
        message="Book details retrieved successfully",
        book=book
    )
