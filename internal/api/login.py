from fastapi import APIRouter
from internal.types.types import LoginRequest, RegisterRequest
from internal.types.responses import SuccessResponse, FailResponse
from internal.models.user import User

router = APIRouter()

# Temporary user storage
USER_DB = []


@router.post("/register", response_model=SuccessResponse)
def register_user(request: RegisterRequest):
    global USER_DB
    for user in USER_DB:
        if request.email == user.get_email():
            return FailResponse(code="Fail", message="Email already registered")

    user = User(username=request.name, email=request.email, password=request.password)
    USER_DB.append(user)

    return SuccessResponse(code="Success", message="User registered successfully")


@router.post("/login", response_model=SuccessResponse)
def login_user(request: LoginRequest):
    for u in USER_DB:
        print(u.get_email())

    user = next((u for u in USER_DB if u.get_email() == request.email), None)

    if not user:
        return FailResponse(code="Fail", message="User not found")

    if not user.check_password(request.password):
        return FailResponse(code="Fail", message="Invalid email or password")

    return SuccessResponse(code="Success", message="Login successful")
