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
        # If there is a valid access_token, do not refresh and return
        user_id = decoded_access.get("id")
        u = await get_user_by_id(user_id)
        if u:
            return SuccessResponse(code=SUCCESS, message="There is already valid access_token exists")

    # 2) Try to get user from request's id
    if request_body.id:
        # If there is a valid user, refresh the access token
        u = await get_user_by_id(request_body.id)
        if u:
            err = create_access_token(u.id, response)
            if err:
                logger.error(f"Failed to create access token in refresh-token endpoint: {err}")
                return JSONResponse(status_code=500, content=jsonable_encoder(
                    FailResponse(code=FAIL, message="Failed to create access token using request id"))
                )
            return SuccessResponse(code=SUCCESS, message="Token refreshed")

    # 3) If no user is in the request body, check for refresh_token
    refresh_token = request.cookies.get("refresh_token")
    decoded_refresh = verify_jwt_token(refresh_token) if refresh_token else None

    if decoded_refresh:
        # If there is a valid refresh token, refresh the access token
        user_id = decoded_refresh.get("id")
        u = await get_user_by_id(user_id)
        if u:
            err = create_access_token(u.id, response)
            if err:
                logger.error(f"Failed to create access token in refresh-token endpoint: {err}")
                return JSONResponse(status_code=500, content=jsonable_encoder(
                    FailResponse(code=FAIL, message="Failed to create access token using refresh token"))
                )
            return SuccessResponse(code=SUCCESS, message="Token refreshed")

    # 4) Require authentication
    return JSONResponse(status_code=401, content=jsonable_encoder(
        FailResponse(code=FAIL, message="Authentication required"))
    )
