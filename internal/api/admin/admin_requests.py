from fastapi import APIRouter, Depends, Body, Query, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from rapidfuzz import fuzz
from internal.database.books import create_book
from internal.models.request import BookRequest, RequestStatus, BookRequestPreview
from internal.utils.utils import get_current_admin
from internal.types.types import SUCCESS, FAIL
from datetime import datetime
from internal.types.responses import (
    FailResponse,
    SuccessResponse,
    BookRequestPreviewListResponse
)
from internal.database.users import (
    get_all_users, get_user_by_id,
    update_request_status_for_all, delete_request_from_all_users,
)

router = APIRouter(prefix="/admin")


@router.get("/requested-books", response_model=BookRequestPreviewListResponse)
async def list_requested_books(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    q: Optional[str] = Query(None, min_length=1),
    admin=Depends(get_current_admin)
):
    users = await get_all_users()
    previews: List[BookRequestPreview] = []

    for u in users:
        for req in (u.requested_books or []):
            previews.append(
                BookRequestPreview(
                    user_id=u.id,
                    username=u.username,
                    email=u.email,
                    id=req.id,
                    title=req.title,
                    authors=req.authors,
                    isbn=req.isbn,
                    publisher=req.publisher,
                    cover_image=req.cover_image,
                    status=req.status,
                    requested_at=req.requested_at,
                    status_updated_at=req.status_updated_at
                )
            )

    if q:
        q_lower = q.lower()
        previews = [
            p for p in previews
            if fuzz.partial_ratio(q_lower, (p.title or "").lower()) >= 60
            or (p.isbn and q_lower in p.isbn.lower())
        ]
    else:
        previews = [p for p in previews if p.status not in ("Added", "Denied")]

    total = len(previews)
    last_page = (total + limit - 1) // limit
    page = min(page, last_page) if last_page else 1
    start, end = (page - 1) * limit, (page * limit)

    return BookRequestPreviewListResponse(
        code=SUCCESS,
        message="Requested books retrieved",
        requests=previews[start:end],
        total=total,
        page=page,
        has_next=end < total and page < last_page,
        last_page=last_page
    )


@router.patch("/requested-books/{user_id}/{request_id}", response_model=SuccessResponse)
async def update_request_status(
    user_id: str = Path(...),
    request_id: str = Path(...),
    status: str = Body(..., embed=True, min_length=1),
    admin=Depends(get_current_admin)
):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    found = False
    for req in user.requested_books or []:
        if req.id == request_id:
            try:
                new_status = RequestStatus(status)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content=jsonable_encoder(FailResponse(code=FAIL, message="Invalid status value"))
                )
            req.status = new_status
            req.status_updated_at = datetime.now()
            found = True
            break

    if not found:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    ok = await update_request_status_for_all(request_id, new_status)
    if not ok:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    return SuccessResponse(code=SUCCESS, message="Status updated")


@router.delete("/requested-books/{user_id}/{request_id}", response_model=SuccessResponse)
async def delete_request(
    user_id: str = Path(...),
    request_id: str = Path(...),
    admin=Depends(get_current_admin)
):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    orig_len = len(user.requested_books or [])
    user.requested_books = [r for r in user.requested_books or [] if r.id != request_id]

    if len(user.requested_books) == orig_len:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    if not await delete_request_from_all_users(request_id):
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    return SuccessResponse(code=SUCCESS, message="Request deleted")


@router.post("/add-book", response_model=SuccessResponse)
async def add_book_from_request(
    user_id: str = Body(...),
    request_id: str = Body(...),
    admin=Depends(get_current_admin)
):
    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="User not found"))
        )

    target: Optional[BookRequest] = None
    for r in user.requested_books or []:
        if r.id == request_id:
            target = r
            break

    if not target:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    from internal.utils.google_books import fetch_google_book
    book_obj = fetch_google_book(target.id)

    if not book_obj:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Volume not found in Google Books"))
        )

    created = await create_book(book_obj)
    if not created:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Could't add book to catalog, Book might already exist in library"
            ))
        )

    target.status = RequestStatus.ADDED
    target.status_updated_at = datetime.now()

    if not await update_request_status_for_all(request_id, RequestStatus.ADDED):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Book saved but request status not updated for everyone"
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="Book added from Google Books and request marked as ADDED"
    )
