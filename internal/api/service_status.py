from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.responses import SuccessResponse, FailResponse
from internal.types.types import SUCCESS, FAIL
from internal.types.responses import VersionResponse
from config.config import get_config, VERSION

router = APIRouter()


@router.get("/version", response_model=VersionResponse, summary="Get version of the service")
def api_version():
    response = VersionResponse(
        code=SUCCESS,
        message="Successfully retrieved version",
        version=VERSION
    )
    return response


@router.get("/health", response_model=SuccessResponse, summary="Get health of the service")
def api_health():
    if get_config("health"):
        return SuccessResponse(
            code=SUCCESS,
            message="Service health is OK",
        )
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(FailResponse(
            code=FAIL,
            message="Service health is not OK"
        ))
    )


@router.get("/ready", response_model=SuccessResponse, summary="Get readiness of the service")
def api_ready():
    if get_config("ready"):
        return SuccessResponse(
            code=SUCCESS,
            message="Service is ready",
        )
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(FailResponse(
            code=FAIL,
            message="Service is not ready"
        ))
    )
