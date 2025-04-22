from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.utils.logger import logger
from internal.models.user import User, PublicUser
from internal.models.admin import PublicAdmin
from internal.utils.utils import hash_password, verify_token_owner
from internal.tokens.tokens import create_access_token, create_refresh_token
from internal.database.users import create_user, get_user_by_email
from internal.database.admins import get_admin_by_email
from internal.types.types import (
    LoginRequest, UserRequest,
    FAIL, SUCCESS
)
from internal.types.responses import (
    SuccessResponse, FailResponse,
    PublicUserResponse, PublicAdminResponse
)

router = APIRouter()


@router.post("/register", response_model=PublicUserResponse)
async def register_user(
    request_body: UserRequest,
    request: Request,
    response: Response
):
    existing_user = await get_user_by_email(request_body.email)
    if existing_user:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Email already registered"
            ))
        )

    user = User(
        username=request_body.username,
        email=request_body.email,
        password=hash_password(request_body.password),
        role="user",
    )

    created_user = await create_user(user)
    if not created_user:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Failed to create user in database"
            ))
        )

    # Assign access_token to current user
    if not verify_token_owner(request, user, "access_token"):
        err = create_access_token(user.id, response)
        if err:
            logger.error(f"Failed to create access token while registering new user: {err}")

    # Assign refresh_token to current user
    if not verify_token_owner(request, user, "refresh_token"):
        err = create_refresh_token(user.id, response)
        if err:
            logger.error(f"Failed to create refresh token while registering new user: {err}")

    return PublicUserResponse(
        code=SUCCESS,
        message="Creation and login successful",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
    )


@router.post("/login")
async def login_user(
    request_body: LoginRequest,
    request: Request,
    response: Response
):
    # Try user first
    entity = await get_user_by_email(request_body.email)
    role = "user"

    # If not user, try admin
    if not entity:
        entity = await get_admin_by_email(request_body.email)
        role = "admin"

    if not entity or not entity.check_password(request_body.password):
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Invalid email or password"
            ))
        )

    # Assign access_token to current user/admin
    if not verify_token_owner(request, entity, "access_token"):
        err = create_access_token(entity.id, entity.role, response)
        if err:
            logger.error(f"Failed to create access token while logging in the {role}: {err}")

    # If remember me is checked, assign refresh_token
    if request_body.remember_me:
        if not verify_token_owner(request, entity, "refresh_token"):
            err = create_refresh_token(entity.id, entity.role, response)
            if err:
                logger.error(f"Failed to create refresh token while logging in the {role}: {err}")
    else:
        response.delete_cookie("refresh_token")

    if role == "user":
        return PublicUserResponse(
            code=SUCCESS,
            message="Login successful",
            user=PublicUser(
                id=entity.id,
                username=entity.username,
                email=entity.email,
                role=entity.role
            )
        )
    else:
        return PublicAdminResponse(
            code=SUCCESS,
            message="Login successful",
            admin=PublicAdmin(
                id=entity.id,
                username=entity.username,
                email=entity.email,
                role=entity.role
            )
        )


@router.post("/logout", response_model=SuccessResponse)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return SuccessResponse(code=SUCCESS, message="Logged out successfully")
