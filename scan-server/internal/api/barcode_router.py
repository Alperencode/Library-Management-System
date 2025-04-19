from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.responses import RFIDResponse, FailResponse
from internal.types.types import SUCCESS, FAIL
from internal.gpio.buzz import buzz_and_blink

from picamera2 import Picamera2
from pyzbar.pyzbar import decode
from isbnlib import is_isbn10, is_isbn13
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import time
import threading

router = APIRouter()

# Global shared camera and state
shared_picam2 = None
camera_lock = threading.Lock()
camera_active = False
flip_camera = True


def is_valid_isbn(isbn: str) -> bool:
    return is_isbn10(isbn) or is_isbn13(isbn)


def get_font():
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except IOError:
        return ImageFont.load_default()


@router.get("/barcode/video")
def barcode_video_feed():
    def generate_frames():
        font = get_font()
        last_title = ""
        last_valid_time = 0
        DISPLAY_DURATION = 5

        global shared_picam2, camera_active, flip_camera
        while True:
            if not camera_active or shared_picam2 is None:
                time.sleep(0.1)
                continue

            try:
                frame = shared_picam2.capture_array("main")
            except Exception:
                break

            if flip_camera:
                frame = cv2.rotate(frame, cv2.ROTATE_180)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for barcode in decode(gray):
                isbn = barcode.data.decode("utf-8").strip()
                if is_valid_isbn(isbn):
                    last_title = isbn
                    last_valid_time = time.time()

                pts = np.array([barcode.polygon], np.int32)
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if last_title and time.time() - last_valid_time < DISPLAY_DURATION:
                draw = ImageDraw.Draw(pil_img)
                draw.text((30, 30), last_title, font=font, fill=(255, 255, 255))
            frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/barcode/scan", response_model=RFIDResponse)
def scan_barcode():
    timeout_seconds = 30
    start_time = time.time()

    global shared_picam2, camera_active

    try:
        # Initialize camera
        shared_picam2 = Picamera2()
        video_config = shared_picam2.create_video_configuration(
            main={"size": (640, 480)},
            controls={"AwbMode": 1}
        )
        shared_picam2.configure(video_config)
        shared_picam2.start()
        camera_active = True

        while time.time() - start_time < timeout_seconds:
            frame = shared_picam2.capture_array("main")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            for barcode in decode(gray):
                isbn = barcode.data.decode("utf-8").strip()
                if is_valid_isbn(isbn):
                    buzz_and_blink(g=True)
                    return RFIDResponse(
                        code=SUCCESS,
                        message="Successfully retrieved ISBN from barcode",
                        data=isbn
                    )

            time.sleep(0.2)

        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        return JSONResponse(
            status_code=408,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Barcode scan timeout: no valid ISBN detected.")
            )
        )

    except Exception as e:
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message=f"Barcode scan failed: {str(e)}")
            )
        )

    finally:
        if shared_picam2:
            shared_picam2.close()
            shared_picam2 = None
        camera_active = False
