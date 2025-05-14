from datetime import datetime
from typing import Optional
from fastapi import Query
from rapidfuzz import fuzz
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.request import BookRequest, RequestStatus
from internal.models.user import User
from internal.utils.utils import get_current_user
from internal.database.users import update_user, get_user_by_id
from internal.types.types import SUCCESS, FAIL
from internal.types.responses import (
    SuccessResponse,
    FailResponse,
    PaginatedBookRequestListResponse
)
router = APIRouter()


@router.post("/request-book", response_model=SuccessResponse)
async def request_book(data: BookRequest = Body(...), user: User = Depends(get_current_user)):
    user = await get_user_by_id(user.id)
    if not user.requested_books:
        user.requested_books = []

    # Check for duplicates
    for existing in user.requested_books:
        if existing.id and existing.id == data.id:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(FailResponse(
                    code=FAIL,
                    message="You have already requested this book."
                ))
            )

    # Count only active requests
    active_requests = [
        r for r in user.requested_books
        if r.status not in {RequestStatus.ADDED, RequestStatus.DENIED, RequestStatus.APPROVED}
    ]
    if len(active_requests) >= 10:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="You can only have up to 10 active book requests at a time." +
                " Please wait for current requests to be processed before adding more."
            ))
        )

    # Proceed with request
    data.requested_at = datetime.now()
    user.requested_books.append(data)
    updated = await update_user(user)
    if not updated:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Failed to update your request. Please try again later."
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message=f"Book request for '{data.title}' submitted successfully"
    )


@router.get("/request-book", response_model=PaginatedBookRequestListResponse)
async def get_requested_books(
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    q: Optional[str] = Query(None, min_length=1)
):
    if not user.requested_books:
        return PaginatedBookRequestListResponse(
            code=SUCCESS,
            message="No requested books found",
            books=[],
            total=0,
            page=1,
            last_page=1,
            has_next=False
        )

    q_lower = q.lower() if q else None
    threshold = 85
    filtered = []

    for req in user.requested_books:
        if not q_lower:
            filtered.append(req)
            continue

        title_score = fuzz.partial_ratio(q_lower, req.title.lower()) if req.title else 0
        author_score = max((fuzz.partial_ratio(q_lower, a.lower()) for a in req.authors), default=0)
        publisher_score = fuzz.partial_ratio(q_lower, req.publisher.lower()) if req.publisher else 0

        if max(title_score, author_score, publisher_score) >= threshold:
            filtered.append(req)

    deprioritized_statuses = {RequestStatus.ADDED, RequestStatus.DENIED}
    filtered.sort(key=lambda req: req.status in deprioritized_statuses)

    total = len(filtered)
    last_page = (total + limit - 1) // limit
    page = min(page, last_page) if last_page > 0 else 1
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]

    book_requests = [
        BookRequest(
            id=req.id,
            title=req.title,
            authors=req.authors,
            isbn=req.isbn,
            publisher=req.publisher,
            cover_image=req.cover_image,
            status=req.status,
            requested_at=req.requested_at,
        ) for req in paginated
    ]

    return PaginatedBookRequestListResponse(
        code=SUCCESS,
        message="Requested books retrieved successfully",
        books=book_requests,
        total=total,
        page=page,
        last_page=last_page,
        has_next=end < total and page < last_page
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

    matching = next((req for req in user.requested_books if req.id == request_id), None)
    if not matching:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Requested book not found"
            ))
        )

    # Disallow deletion for statuses: 'Approved', 'Added', 'Denied'
    if matching.status in {
        RequestStatus.APPROVED,
        RequestStatus.ADDED,
        RequestStatus.DENIED
    }:
        return JSONResponse(
            status_code=403,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message=f"Requests with status '{matching.status.value}' cannot be deleted."
            ))
        )

    user.requested_books = [req for req in user.requested_books if req.id != request_id]
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
