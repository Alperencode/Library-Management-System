from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.tokens.tokens import verify_jwt_token, create_access_token
from internal.database.users import USER_DB
from internal.types.responses import SuccessResponse, FailResponse
from internal.types.types import FAIL, SUCCESS, UserRequest

router = APIRouter()


@router.post("/refresh-token", response_model=SuccessResponse)
async def refresh_token(request: Request, response: Response, body: UserRequest | None = None):
    # Try to get user from body
    user = None
    try:
        body = await request.json()
        user = body.get("user", None)
    except Exception:
        pass

    if user:
        # If there is a valid user in body, refresh the access token
        u = next((u for u in USER_DB if u.id == user.get("id")), None)
        if u:
            new_access_token = create_access_token(u.id)
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None"
            )
            return SuccessResponse(code=SUCCESS, message="Token refreshed")

    # If no user is in the request body, check for refresh_token
    refresh_token = request.cookies.get("refresh_token")
    decoded_refresh = verify_jwt_token(refresh_token) if refresh_token else None

    if decoded_refresh:
        # If there is a valid refresh token, refresh the access token
        user_id = decoded_refresh.get("id")
        u = next((u for u in USER_DB if u.id == user_id), None)
        if u:
            new_access_token = create_access_token(u.id)
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="None"
            )
            return SuccessResponse(code=SUCCESS, message="Token refreshed")

    return JSONResponse(status_code=401, content=jsonable_encoder(
        FailResponse(code=FAIL, message="Authentication required"))
    )
