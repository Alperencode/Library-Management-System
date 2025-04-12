import random
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from internal.types.types import WriteRequest, FAIL, SUCCESS
from internal.types.responses import FailResponse, RFIDResponse

router = APIRouter()

MOCK_STORAGE = "9786053609902"


@router.get("/read", response_model=RFIDResponse)
def mock_read():
    if random.random() < 0.75:
        return RFIDResponse(
            code=SUCCESS,
            message="Successfully retrieved mock RFID data",
            data=MOCK_STORAGE
        )
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Mock failure to read data from RFID tag."
            )
        )
    )


@router.post("/write", response_model=RFIDResponse)
def mock_write(data: WriteRequest):
    global MOCK_STORAGE
    if random.random() < 0.75:
        MOCK_STORAGE = data.text
        return RFIDResponse(
            code=SUCCESS,
            message="Successfully wrote mock data to RFID tag.",
            data=data.text
        )
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Mock failure to write data to RFID tag."
            )
        )
    )
