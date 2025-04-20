import nfc
import ndef
from time import time
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.types import WriteRequest, FAIL, SUCCESS
from internal.types.responses import FailResponse, ISBNResponse
from internal.tokens.tokens import create_scanned_book_token
from internal.gpio.buzz import buzz_and_blink

router = APIRouter()


@router.get("/read", response_model=ISBNResponse)
def read_rfid(response: Response):
    read_result = None
    timeout_seconds = 10
    start_time = time()

    def on_connect(tag):
        if tag.ndef and tag.ndef.length > 0:
            for record in tag.ndef.records:
                if isinstance(record, ndef.TextRecord):
                    buzz_and_blink(g=True)
                    create_scanned_book_token(record.text, response)
                    return ISBNResponse(
                        code=SUCCESS,
                        message="Successfully retrieved RFID data",
                        data=record.text
                    )
            buzz_and_blink(r=True, buzz_times=2, blink_times=2)
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(
                    FailResponse(code=FAIL, message="Unsupported RFID record type.")
                )
            )
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Invalid RFID tag")
            )
        )

    def terminate():
        return time() - start_time > timeout_seconds

    try:
        with nfc.ContactlessFrontend('tty:AMA0') as clf:
            def connected(tag):
                nonlocal read_result
                read_result = on_connect(tag)
                return True

            clf.connect(rdwr={'on-connect': connected}, terminate=terminate)

    except Exception as e:
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message=f"RFID read error: {str(e)}")
            )
        )

    if not read_result:
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        return JSONResponse(
            status_code=408,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="RFID read timeout: no tag detected.")
            )
        )

    return read_result


@router.post("/write", response_model=ISBNResponse)
def write_rfid(data: WriteRequest):
    write_result = None

    def on_connect(tag):
        if tag.ndef:
            try:
                tag.ndef.records = [ndef.TextRecord(data.text)]
                buzz_and_blink(g=True)
                return ISBNResponse(
                    code=SUCCESS,
                    message="Successfully write the data to RFID tag.",
                    data=data.text
                )
            except Exception as e:
                buzz_and_blink(r=True, buzz_times=2, blink_times=2)
                return JSONResponse(
                    status_code=500,
                    content=jsonable_encoder(
                        FailResponse(
                            code=FAIL,
                            message=f"Write failed: {str(e)}"
                        )
                    )
                )
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
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

    return write_result
