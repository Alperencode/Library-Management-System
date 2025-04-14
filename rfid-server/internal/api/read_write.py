import nfc
import ndef
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.types import WriteRequest, FAIL, SUCCESS
from internal.types.responses import FailResponse, RFIDResponse
from internal.gpio.buzz import buzz
from internal.tokens.tokens import create_scanned_book_token

router = APIRouter()


@router.get("/read", response_model=RFIDResponse)
def read_rfid(response: Response):
    read_result = None

    def on_connect(tag):
        if tag.ndef and tag.ndef.length > 0:
            for record in tag.ndef.records:
                if isinstance(record, ndef.TextRecord):
                    buzz()
                    create_scanned_book_token(record.text, response)
                    return RFIDResponse(
                        code=SUCCESS,
                        message="Successfully retrieved RFID data",
                        data=record.text
                    )
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(
                    FailResponse(
                        code=FAIL,
                        message="Unsupported RFID record type."
                    )
                )
            )
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(
                    code=FAIL,
                    message="No NDEF data found or tag not writable."
                )
            )
        )

    with nfc.ContactlessFrontend('tty:AMA0') as clf:
        def connected(tag):
            nonlocal read_result
            read_result = on_connect(tag)
            return True
        clf.connect(rdwr={'on-connect': connected})

    return read_result


@router.post("/write", response_model=RFIDResponse)
def write_rfid(data: WriteRequest):
    write_result = None

    def on_connect(tag):
        if tag.ndef:
            tag.ndef.records = [ndef.TextRecord(data.text)]
            buzz()
            return RFIDResponse(
                code=SUCCESS,
                message="Successfully write the data to RFID tag.",
                data=data.text
            )
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                FailResponse(
                    code=FAIL,
                    message="Tag is not NDEF-formatted or not writable."
                )
            )
        )

    with nfc.ContactlessFrontend('tty:AMA0') as clf:
        def connected(tag):
            nonlocal write_result
            write_result = on_connect(tag)
            return True
        clf.connect(rdwr={'on-connect': connected})

    if isinstance(write_result, RFIDResponse):
        return write_result
    return write_result
