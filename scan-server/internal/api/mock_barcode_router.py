import random
from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from internal.types.responses import ISBNResponse, FailResponse
from internal.types.types import SUCCESS, FAIL, WriteRequest
from internal.tokens.tokens import create_scanned_book_token

from PIL import Image, ImageDraw, ImageFont
import time
import io

router = APIRouter()

MOCK_BARCODE_ISBN = "9786053609902"
MOCK_BOOK_TITLE = "Mock Book Title"


@router.get("/barcode/scan", response_model=ISBNResponse)
def mock_scan_barcode(background_tasks: BackgroundTasks, response: Response):
    import time
    chance = random.random()
    print(f"[Mock Scan] Random chance: {chance}")

    time.sleep(5)

    if chance < 0.8:
        create_scanned_book_token(MOCK_BARCODE_ISBN, response)
        return ISBNResponse(
            code=SUCCESS,
            message="Successfully retrieved mock ISBN from barcode",
            data=MOCK_BARCODE_ISBN
        )
    return JSONResponse(
        status_code=408,
        content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Mock timeout: No barcode detected."
            )
        )
    )


@router.post("/barcode/write", response_model=ISBNResponse)
def mock_write_barcode(data: WriteRequest):
    global MOCK_BARCODE_ISBN
    if random.random() < 0.8:
        MOCK_BARCODE_ISBN = data.text
        return ISBNResponse(
            code=SUCCESS,
            message="Successfully wrote mock ISBN to barcode.",
            data=MOCK_BARCODE_ISBN
        )
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Mock failure to write ISBN to barcode."
            )
        )
    )


@router.get("/barcode/video")
def mock_video_feed():
    def generate_frames():
        for i in range(5, 0, -1):
            img = Image.new("RGB", (640, 480), color=(30, 30, 30))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            except Exception:
                font = ImageFont.load_default()

            text = f"Scanning in progress...\nCountdown: {i}\nISBN: {MOCK_BARCODE_ISBN}"
            draw.multiline_text((100, 200), text, font=font, fill=(255, 255, 255), spacing=10)

            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            frame = buf.getvalue()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )

            time.sleep(1)

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")