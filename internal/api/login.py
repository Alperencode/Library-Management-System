from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.user import User
from internal.types.types import LoginRequest, RegisterRequest, FAIL, SUCCESS
from internal.types.responses import SuccessResponse, FailResponse
from internal.tokens.tokens import create_access_token, create_refresh_token

router = APIRouter()

USER_DB = []


@router.post("/register", response_model=SuccessResponse)
def register_user(request: RegisterRequest):
    global USER_DB
    for user in USER_DB:
        if request.email == user.get_email():
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
        role="user"
    )
    USER_DB.append(user)

    return SuccessResponse(code=SUCCESS, message="User registered successfully")


@router.post("/login", response_model=SuccessResponse)
def login_user(request: LoginRequest, response: Response):
    user = next((u for u in USER_DB if u.get_email() == request.email), None)

    if not user or not user.check_password(request.password):
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Invalid email or password"
            ))
        )

    user_data = {
        "user_id": user.get_id(),
        "username": user.get_username(),
        "email": user.get_email(),
        "role": user.get_role()
    }

    access_token = create_access_token(user_data)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None"
    )

    if request.remember_me:
        refresh_token = create_refresh_token(user_data)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None"
        )

    return SuccessResponse(code=SUCCESS, message="Login successful")
