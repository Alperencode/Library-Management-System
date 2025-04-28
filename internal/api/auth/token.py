from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.utils.logger import logger
from internal.tokens.tokens import verify_jwt_token, create_access_token
from internal.database.users import get_user_by_id
from internal.database.admins import get_admin_by_id
from internal.types.responses import SuccessResponse, FailResponse
from internal.types.types import FAIL, SUCCESS, IDRequest

router = APIRouter()


async def try_refresh(user_id: str, response: Response) -> bool:
    user = await get_user_by_id(user_id)
    if user:
        err = create_access_token(user.id, "user", response)
        if err:
            logger.error(f"Failed to create access token for user: {err}")
            return False
        return True

    admin = await get_admin_by_id(user_id)
    if admin:
        err = create_access_token(admin.id, "admin", response)
        if err:
            logger.error(f"Failed to create access token for admin: {err}")
            return False
        return True

    return False


@router.post("/refresh-token", response_model=SuccessResponse)
async def refresh_token(request: Request, response: Response, request_body: IDRequest | None = None):
    # 1) Check if there is a valid access_token
    present_access_token = request.cookies.get("access_token")
    decoded_access = verify_jwt_token(present_access_token) if present_access_token else None

    if decoded_access:
        user_id = decoded_access.get("id")
        user = await get_user_by_id(user_id)
        if user:
            return SuccessResponse(code=SUCCESS, message="You are already logged in.")
        admin = await get_admin_by_id(user_id)
        if admin:
            return SuccessResponse(code=SUCCESS, message="You are already logged in.")

    # 2) Try to refresh using ID in request body
    if request_body and request_body.id:
        if await try_refresh(request_body.id, response):
            return SuccessResponse(code=SUCCESS, message="Session refreshed successfully.")
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Something went wrong while refreshing your session. Please try again."
            ))
        )

    # 3) Try to refresh using refresh_token
    refresh_token_cookie = request.cookies.get("refresh_token")
    decoded_refresh = verify_jwt_token(refresh_token_cookie) if refresh_token_cookie else None

    if decoded_refresh:
        user_id = decoded_refresh.get("id")
        if await try_refresh(user_id, response):
            return SuccessResponse(code=SUCCESS, message="Session refreshed successfully.")
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Unable to restore your session. Please try again shortly."
            ))
        )

    # 4) No valid token or user/admin found
    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Your session has expired or is invalid. Please log in again."
            )
        )
    )
