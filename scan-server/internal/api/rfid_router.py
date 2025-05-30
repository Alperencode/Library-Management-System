import nfc
import ndef
import time as t
from time import time
from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.types import WriteRequest, FAIL, SUCCESS
from internal.types.responses import FailResponse, ISBNResponse
from internal.tokens.tokens import create_scanned_book_token
from internal.gpio.buzz import buzz_and_blink, rgb_on
from threading import Thread, Event
import asyncio


router = APIRouter()


@router.get("/read", response_model=ISBNResponse)
async def read_rfid(response: Response, request: Request):
    rgb_on(b=True)
    timeout_seconds = 10
    start_time = time()
    cancel_event = Event()
    read_result = {}

    def on_connect(tag):
        rgb_on(False, False, False)
        t.sleep(0.2)

        if tag.ndef and tag.ndef.length > 0:
            for record in tag.ndef.records:
                if isinstance(record, ndef.TextRecord):
                    buzz_and_blink(g=True)
                    create_scanned_book_token(record.text, response)
                    read_result['value'] = ISBNResponse(
                        code=SUCCESS,
                        message="Successfully retrieved RFID data",
                        data=record.text
                    )
                    return True
            buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        return True

    def terminate():
        return time() - start_time > timeout_seconds or cancel_event.is_set()

    def read_from_rfid():
        try:
            with nfc.ContactlessFrontend('tty:AMA0') as clf:
                clf.connect(rdwr={'on-connect': on_connect}, terminate=terminate)
        except Exception as e:
            read_result['value'] = JSONResponse(
                status_code=500,
                content=jsonable_encoder(
                    FailResponse(code=FAIL, message=f"RFID read error: {str(e)}")
                )
            )

    thread = Thread(target=read_from_rfid)
    thread.start()

    # Monitor client disconnect
    while thread.is_alive():
        if await request.is_disconnected():
            cancel_event.set()
            thread.join()
            rgb_on(False, False, False)
            return JSONResponse(
                status_code=499,
                content=jsonable_encoder(FailResponse(code=FAIL, message="Client disconnected."))
            )
        await asyncio.sleep(0.1)

    thread.join()
    rgb_on(False, False, False)
    await asyncio.sleep(0.2)
    if read_result.get('value'):
        return read_result.get('value')

    
    buzz_and_blink(r=True, buzz_times=2, blink_times=2)
    return JSONResponse(
        status_code=408,
        content=jsonable_encoder(
            FailResponse(code=FAIL, message="RFID read timeout or no tag.")
        )
    )


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
