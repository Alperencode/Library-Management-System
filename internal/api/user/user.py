from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.utils.utils import hash_password, get_current_user
from internal.database.admins import get_admin_by_email, get_admin_by_username
from internal.database.users import get_user_by_id, update_user, get_user_by_username, get_user_by_email
from internal.types.responses import FailResponse, PublicUserResponse
from internal.types.types import SUCCESS, FAIL, UserUpdateRequest
from internal.models.user import User, PublicUser

router = APIRouter()


@router.get("/me", response_model=PublicUserResponse)
async def get_current_user_info(user: User = Depends(get_current_user)):
    return PublicUserResponse(
        code=SUCCESS,
        message="User details retrieved successfully",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            borrowed_books=user.borrowed_books,
            borrowed_history=user.borrowed_history,
            overdue_books=user.overdue_books,
            notify_me_list=user.notify_me_list,
            penalties=user.penalties
        )
    )


@router.patch("/me", response_model=PublicUserResponse)
async def update_user_info(update_data: UserUpdateRequest, user: User = Depends(get_current_user)):
    user = await get_user_by_id(user.id)
    if not user:
        return JSONResponse(status_code=404, content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="User not found"
            )
        ))

    isUpdated = False
    if update_data.username and update_data.username != user.username:
        existing_username_user = await get_user_by_username(update_data.username)
        existing_username_admin = await get_admin_by_username(update_data.username)
        if (existing_username_user and existing_username_user.id != user.id) or existing_username_admin:
            return JSONResponse(status_code=409, content=jsonable_encoder(
                FailResponse(
                    code=FAIL,
                    message="Username already taken"
                )
            ))
        user.username = update_data.username
        isUpdated = True

    if update_data.email and update_data.email != user.email:
        existing_email_user = await get_user_by_email(update_data.email)
        existing_email_admin = await get_admin_by_email(update_data.email)
        if (existing_email_user and existing_email_user.id != user.id) or existing_email_admin:
            return JSONResponse(status_code=409, content=jsonable_encoder(
                FailResponse(
                    code=FAIL,
                    message="Email already registered"
                )
            ))
        user.email = update_data.email
        isUpdated = True

    if update_data.password and not user.check_password(update_data.password):
        user.password = hash_password(update_data.password)
        isUpdated = True

    if isUpdated:
        updated = await update_user(user)
        if not updated:
            return JSONResponse(status_code=500, content=jsonable_encoder(
                FailResponse(
                    code=FAIL,
                    message="Failed to update user details"
                )
            ))

    return PublicUserResponse(
        code=SUCCESS,
        message="User details updated successfully",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
    )
