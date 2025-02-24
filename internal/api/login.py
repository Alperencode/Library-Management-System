from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.user import User
from internal.types.types import LoginRequest, RegisterRequest, FAIL, SUCCESS
from internal.types.responses import SuccessResponse, FailResponse

router = APIRouter()

# Temporary user storage
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

    user = User(username=request.name, email=request.email, password=request.password)
    USER_DB.append(user)

    return SuccessResponse(code=SUCCESS, message="User registered successfully")


@router.post("/login", response_model=SuccessResponse)
def login_user(request: LoginRequest):
    user = next((u for u in USER_DB if u.get_email() == request.email), None)

    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Invalid email or password"
            ))
        )

    if not user.check_password(request.password):
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Invalid email or password"
            ))
        )

    return SuccessResponse(code=SUCCESS, message="Login successful")
