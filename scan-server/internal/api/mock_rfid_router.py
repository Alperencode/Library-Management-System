import random
from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from internal.types.types import WriteRequest, FAIL, SUCCESS
from internal.types.responses import FailResponse, ISBNResponse
from internal.tokens.tokens import create_scanned_book_token

router = APIRouter()

MOCK_STORAGE = "9786053609902"


@router.get("/read", response_model=ISBNResponse)
def mock_read(response: Response):
    if random.random() < 0.75:
        create_scanned_book_token(MOCK_STORAGE, response)
        return ISBNResponse(
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


@router.post("/write", response_model=ISBNResponse)
def mock_write(data: WriteRequest):
    global MOCK_STORAGE
    if random.random() < 0.75:
        MOCK_STORAGE = data.text
        return ISBNResponse(
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
