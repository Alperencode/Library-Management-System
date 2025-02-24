from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.responses import FailResponse
from internal.types.types import FAIL


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(FailResponse(
            code=FAIL,
            message="An unexpected error occurred"
        ))
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors()
    message = error_details[0]['msg'] if error_details else "Validation failed"

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(FailResponse(
            code=FAIL,
            message=message.capitalize()
        ))
    )
