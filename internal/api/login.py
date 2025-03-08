from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.user import User, PublicUser
from internal.types.responses import SuccessResponse, FailResponse, PublicUserResponse
from internal.tokens.tokens import create_access_token, create_refresh_token
from internal.database.users import USER_DB
from internal.types.types import (
    LoginRequest, UserRequest,
    FAIL, SUCCESS
)

router = APIRouter()


@router.post("/register", response_model=PublicUserResponse)
def register_user(request: UserRequest, response: Response):
    global USER_DB
    for user in USER_DB:
        if request.email == user.email:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(FailResponse(
                    code=FAIL,
                    message="Email already registered"
                ))
            )

    user = User(
        username=request.username,
        email=request.email,
        password=request.password,
        role="user",
    )
    USER_DB.append(user)

    access_token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None"
    )

    return PublicUserResponse(
        code=SUCCESS,
        message="User registered successfully",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
    )


@router.post("/login", response_model=PublicUserResponse)
def login_user(request: LoginRequest, response: Response):
    user = next((u for u in USER_DB if u.email == request.email), None)

    if not user or not user.check_password(request.password):
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Invalid email or password"
            ))
        )

    access_token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None"
    )

    if request.remember_me:
        refresh_token = create_refresh_token(user.id)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None"
        )

    return PublicUserResponse(
        code=SUCCESS,
        message="Login successful",
        user=PublicUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
    )


@router.post("/logout", response_model=SuccessResponse)
def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return SuccessResponse(code=SUCCESS, message="Logged out successfully")
