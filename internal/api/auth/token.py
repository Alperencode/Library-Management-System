from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.utils.logger import logger
from internal.tokens.tokens import verify_jwt_token, create_access_token
from internal.database.users import get_user_by_id
from internal.types.responses import SuccessResponse, FailResponse
from internal.types.types import FAIL, SUCCESS, IDRequest

router = APIRouter()


@router.post("/refresh-token", response_model=SuccessResponse)
async def refresh_token(request: Request, response: Response, request_body: IDRequest | None = None):
    # 1) Check if there is valid access_token
    present_access_token = request.cookies.get("access_token")
    decoded_access = verify_jwt_token(present_access_token) if present_access_token else None

    if decoded_access:
        user_id = decoded_access.get("id")
        u = await get_user_by_id(user_id)
        if u:
            return SuccessResponse(code=SUCCESS, message="You are already logged in.")

    # 2) Try to refresh using ID in request body
    if request_body and request_body.id:
        u = await get_user_by_id(request_body.id)
        if u:
            err = create_access_token(u.id, response)
            if err:
                logger.error(f"Failed to create access token (from request body): {err}")
                return JSONResponse(
                    status_code=500,
                    content=jsonable_encoder(
                        FailResponse(
                            code=FAIL,
                            message="Something went wrong while refreshing your session. Please try again."
                        )
                    )
                )
            return SuccessResponse(code=SUCCESS, message="Session refreshed successfully.")

    # 3) Try to refresh using refresh_token
    refresh_token = request.cookies.get("refresh_token")
    decoded_refresh = verify_jwt_token(refresh_token) if refresh_token else None

    if decoded_refresh:
        user_id = decoded_refresh.get("id")
        u = await get_user_by_id(user_id)
        if u:
            err = create_access_token(u.id, response)
            if err:
                logger.error(f"Failed to create access token (from refresh token): {err}")
                return JSONResponse(
                    status_code=500,
                    content=jsonable_encoder(
                        FailResponse(
                            code=FAIL,
                            message="Unable to restore your session. Please try again shortly."
                        )
                    )
                )
            return SuccessResponse(code=SUCCESS, message="Session refreshed successfully.")

    # 4) No valid token or user ID found
    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Your session has expired or is invalid. Please log in again."
            )
        )
    )
