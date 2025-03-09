import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.config import get_config
from internal.utils.utils import hash_password
from internal.database.users import get_user_by_id, update_user
from internal.types.responses import FailResponse, PublicUserResponse
from internal.types.types import SUCCESS, FAIL, UserUpdateRequest
from internal.models.user import User, PublicUser

router = APIRouter()


async def get_current_user(request: Request):
    # Check for access_token cookie
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        payload = jwt.decode(access_token, get_config("secret_key"), algorithms=[get_config("algorithm")])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from database
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/me", response_model=PublicUserResponse)
async def get_current_user_info(user: User = Depends(get_current_user)):
    return PublicUserResponse(
        code=SUCCESS,
        message="User details retrieved successfully",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
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
        user.username = update_data.username
        isUpdated = True
    if update_data.email and update_data.email != user.email:
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
