from typing import List
from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.user import User
from internal.types.responses import SuccessResponse, FailResponse, UserResponse
from internal.tokens.tokens import verify_jwt_token, create_access_token, create_refresh_token
from internal.types.types import (
    LoginRequest, RegisterRequest, RefreshTokenRequest,
    UserRequest, FAIL, SUCCESS
)

router = APIRouter()

USER_DB: List[User] = []


@router.post("/register", response_model=UserResponse)
def register_user(request: RegisterRequest):
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
        username=request.name,
        email=request.email,
        password=request.password,
        role="user",
    )
    user.refresh_token = create_refresh_token(user.id)

    USER_DB.append(user)
    return UserResponse(
        code=SUCCESS,
        message="User registered successfully",
        user=user
    )


@router.post("/login", response_model=UserResponse)
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
        user.set_refresh_token(refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None"
        )

    return UserResponse(
        code=SUCCESS,
        message="Login successful",
        user=user
    )


@router.post("/refresh-token", response_model=SuccessResponse)
def refresh_token(request: Request, body: RefreshTokenRequest, response: Response):
    user = body.user

    # If the session is still active, allow silent refresh
    if user:
        new_access_token = create_access_token(user.id)
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True, samesite="None")
        return SuccessResponse(
            code=SUCCESS,
            message="Token refreshed"
        )

    # Else, check if any refresh token exists
    refresh_token = request.cookies.get("refresh_token")
    decoded_refresh = verify_jwt_token(refresh_token) if refresh_token else None
    if decoded_refresh:
        if user and user.refresh_token == refresh_token:
            new_access_token = create_access_token(user.id)
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None"
            )
            return SuccessResponse(code=SUCCESS, message="Token refreshed")

    # If there is no refresh token, require authentication
    return JSONResponse(status_code=401, content=jsonable_encoder(
        FailResponse(
            code=FAIL,
            message="Authentication required"
        ))
    )


@router.post("/logout", response_model=SuccessResponse)
def logout_user(request: UserRequest, response: Response):
    user = next((u for u in USER_DB if u.email == request.email), None)
    if user:
        user.refresh_token = None

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return SuccessResponse(code=SUCCESS, message="Logged out successfully")
