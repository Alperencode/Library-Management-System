from fastapi import APIRouter, Response, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from internal.types.responses import SuccessResponse, FailResponse, TokenResponse
from internal.tokens.tokens import verify_jwt_token, create_access_token
from internal.database.users import USER_DB
from internal.types.types import RefreshTokenRequest, FAIL, SUCCESS

router = APIRouter()


@router.post("/refresh-token", response_model=SuccessResponse)
def refresh_token(request: Request, body: RefreshTokenRequest, response: Response):
    user = body.user

    # If the session is still active, allow silent refresh
    if user:
        new_access_token = create_access_token(user.id)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="None"
        )

        return SuccessResponse(
            code=SUCCESS,
            message="Token refreshed"
        )

    # Else, check if any refresh token exists
    refresh_token = request.cookies.get("refresh_token")
    decoded_refresh = verify_jwt_token(refresh_token) if refresh_token else None
    if decoded_refresh:
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


@router.post("/access_token", response_model=TokenResponse)
def authenticate_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in USER_DB if u.username == form_data.username), None)

    if not user or not user.check_password(form_data.password):
        return JSONResponse(status_code=401, content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Invalid credentials"
            )
        ))

    if request.cookies.get("access_token"):
        return TokenResponse(
            code=SUCCESS,
            message="Successfully retrieved the access token",
            access_token=request.cookies.get("access_token"),
            token_type="bearer"
        )

    access_token = create_access_token(user.id)
    return TokenResponse(
        code=SUCCESS,
        message="Successfully created the access token",
        access_token=access_token,
        token_type="bearer"
    )
