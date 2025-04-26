from fastapi import APIRouter, Depends, Body, Query, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from rapidfuzz import fuzz
from internal.database.books import create_book
from internal.models.request import RequestStatus, BookRequestPreview, RequesterInfo, RequestDetails
from internal.utils.utils import get_current_admin
from internal.types.types import SUCCESS, FAIL
from internal.types.responses import (
    FailResponse, SuccessResponse,
    BookRequestPreviewListResponse, BookRequestDetailsResponse,
)
from internal.database.users import (
    get_all_users,
    update_request_status_for_all,
    delete_request_from_all_users,
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
    seen_ids = set()

    for u in users:
        for req in (u.requested_books or []):
            if req.id in seen_ids:
                continue
            seen_ids.add(req.id)

            if req.status in ("Added", "Denied"):
                continue  # Filter out here

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


@router.patch("/requested-books/{request_id}", response_model=SuccessResponse)
async def update_request_status(
    request_id: str = Path(...),
    status: str = Body(..., embed=True, min_length=1),
    admin=Depends(get_current_admin)
):
    try:
        new_status = RequestStatus(status)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Invalid status value"))
        )

    ok = await update_request_status_for_all(request_id, new_status)
    if not ok:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    return SuccessResponse(code=SUCCESS, message="Status updated")


@router.delete("/requested-books/{request_id}", response_model=SuccessResponse)
async def delete_request(
    request_id: str = Path(...),
    admin=Depends(get_current_admin)
):
    ok = await delete_request_from_all_users(request_id)
    if not ok:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    return SuccessResponse(code=SUCCESS, message="Request deleted")


@router.post("/add-book", response_model=SuccessResponse)
async def add_book_from_request(
    request_id: str = Body(..., embed=True),
    admin=Depends(get_current_admin)
):
    from internal.utils.google_books import fetch_google_book
    book_obj = fetch_google_book(request_id)

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
                message="Couldn't add book to catalog, Book might already exist in library"
            ))
        )

    updated = await update_request_status_for_all(request_id, RequestStatus.ADDED)
    if not updated:
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


@router.get("/requested-books/info/{request_id}", response_model=BookRequestDetailsResponse)
async def get_request_info(
    request_id: str = Path(...),
    admin=Depends(get_current_admin)
):
    users = await get_all_users()
    matched_users = []
    request_data = None

    for user in users:
        for req in user.requested_books or []:
            if req.id == request_id:
                if not request_data:
                    request_data = RequestDetails(
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
                matched_users.append(RequesterInfo(
                    id=user.id,
                    username=user.username,
                    email=user.email
                ))

    if not request_data:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(code=FAIL, message="Request not found"))
        )

    return BookRequestDetailsResponse(
        code=SUCCESS,
        message="Request info retrieved",
        request=request_data,
        requester_count=len(matched_users),
        requesters=matched_users
    )


@router.get("/requested-books/added", response_model=BookRequestPreviewListResponse)
async def list_added_requests(admin=Depends(get_current_admin)):
    users = await get_all_users()
    seen_ids = set()
    previews: List[BookRequestPreview] = []

    for u in users:
        for req in u.requested_books or []:
            if req.status == RequestStatus.ADDED and req.id not in seen_ids:
                seen_ids.add(req.id)
                previews.append(BookRequestPreview(
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
                ))

    return BookRequestPreviewListResponse(
        code=SUCCESS,
        message="Added requests retrieved",
        requests=previews,
        total=len(previews),
        page=1,
        has_next=False,
        last_page=1
    )


@router.get("/requested-books/denied", response_model=BookRequestPreviewListResponse)
async def list_denied_requests(admin=Depends(get_current_admin)):
    users = await get_all_users()
    seen_ids = set()
    previews: List[BookRequestPreview] = []

    for u in users:
        for req in u.requested_books or []:
            if req.status == RequestStatus.DENIED and req.id not in seen_ids:
                seen_ids.add(req.id)
                previews.append(BookRequestPreview(
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
                ))

    return BookRequestPreviewListResponse(
        code=SUCCESS,
        message="Denied requests retrieved",
        requests=previews,
        total=len(previews),
        page=1,
        has_next=False,
        last_page=1
    )
