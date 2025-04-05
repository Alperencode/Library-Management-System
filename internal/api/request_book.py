from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.request import BookRequest
from internal.models.user import User
from internal.utils.utils import get_current_user
from internal.database.users import update_user, get_user_by_id
from internal.types.types import SUCCESS, FAIL
from internal.types.responses import (
    SuccessResponse,
    FailResponse,
    BookRequestListResponse
)
from datetime import datetime
router = APIRouter()


@router.post("/request-book", response_model=SuccessResponse)
async def request_book(data: BookRequest = Body(...), user: User = Depends(get_current_user)):
    if not user.requested_books:
        user.requested_books = []

    data.requested_at = datetime.now()
    user = await get_user_by_id(user.id)
    for existing in user.requested_books:
        if existing.id and existing.id == data.id:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(FailResponse(
                    code=FAIL,
                    message="You have already requested this book."
                ))
            )

    user.requested_books.append(data)
    updated = await update_user(user)
    if not updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Failed to update user data"
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message=f"Book request for '{data.title}' submitted successfully"
    )


@router.get("/request-book", response_model=BookRequestListResponse)
async def get_requested_books(user: User = Depends(get_current_user)):
    if not user.requested_books:
        return BookRequestListResponse(
            code=SUCCESS,
            message="No requested books found",
            books=[]
        )

    book_requests = [
        BookRequest(
            id=request.id,
            title=request.title,
            authors=request.authors,
            isbn=request.isbn,
            publisher=request.publisher,
            cover_image=request.cover_image,
            status=request.status,
            requested_at=request.requested_at,
        ) for request in user.requested_books
    ]

    return BookRequestListResponse(
        code=SUCCESS,
        message="Requested books retrieved successfully",
        books=book_requests
    )


@router.get("/requests/{request_id}", response_model=BookRequest)
async def get_requested_book(request_id: str, user: User = Depends(get_current_user)):
    if not user.requested_books:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="No requested books found"
            ))
        )

    for request in user.requested_books:
        if request.id == request_id:
            return request

    return JSONResponse(
        status_code=404,
        content=jsonable_encoder(FailResponse(
            code=FAIL,
            message="Requested book not found"
        ))
    )


@router.delete("/requests/{request_id}", response_model=SuccessResponse)
async def delete_requested_book(request_id: str, user: User = Depends(get_current_user)):
    if not user.requested_books:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="No requested books found"
            ))
        )

    filtered = [req for req in user.requested_books if req.id != request_id]
    if len(filtered) == len(user.requested_books):
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Requested book not found"
            ))
        )

    user.requested_books = filtered
    updated = await update_user(user)
    if not updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Failed to update user data"
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="Requested book removed successfully"
    )
