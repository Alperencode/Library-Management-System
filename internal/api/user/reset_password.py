from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.tokens.tokens import create_password_reset_token, verify_password_reset_token
from internal.utils.email import send_reset_password_email
from internal.utils.utils import hash_password
from internal.database.users import get_user_by_email, get_user_by_id, update_user
from internal.types.types import ResetPasswordRequest, EmailRequest, FAIL, SUCCESS
from internal.types.responses import SuccessResponse, FailResponse

router = APIRouter()


@router.post("/forgot-password", response_model=SuccessResponse)
async def forgot_password(request_body: EmailRequest):
    user = await get_user_by_email(request_body.email)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="We couldn't find an account with that email address."
            ))
        )

    token = create_password_reset_token(user.id)
    success = await send_reset_password_email(user=user, token=token)
    if not success:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Something went wrong while sending the reset email. Please try again later."
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="Password reset link has been sent successfully."
    )


@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(request_body: ResetPasswordRequest):
    user_id = verify_password_reset_token(request_body.token)
    if not user_id:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Your password reset link is invalid or has expired."
            ))
        )

    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="We couldn't verify your account. Please try again."
            ))
        )

    user.password = hash_password(request_body.new_password)
    success = await update_user(user)

    if not success:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Something went wrong while updating your password. Please try again."
            ))
        )

    return SuccessResponse(
        code=SUCCESS,
        message="Your password has been successfully reset. You can now log in with your new password."
    )
