from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.types.responses import ISBNResponse, FailResponse
from internal.types.types import SUCCESS, FAIL
from internal.gpio.buzz import buzz_and_blink, rgb_on
from internal.utils.utils import is_valid_isbn, get_font
from internal.tokens.tokens import create_scanned_book_token

from picamera2 import Picamera2
from pyzbar.pyzbar import decode
from isbnlib import meta
from PIL import Image, ImageDraw
import numpy as np
import cv2
import time

router = APIRouter()

shared_picam2 = None
last_scanned_frame = None
camera_active = False
flip_camera = True
display_title = ""
display_until = 0
camera_session_id = 0


def stop_camera_after_delay(delay: float, session_id: float):
    global shared_picam2, camera_active, display_title, display_until, camera_session_id
    time.sleep(delay)
    if session_id != camera_session_id:
        return
    if shared_picam2:
        shared_picam2.close()
        shared_picam2 = None
    camera_active = False
    display_title = ""
    display_until = 0
    time.sleep(0.3)


@router.get("/barcode/video")
def barcode_video_feed():
    global shared_picam2, camera_active, flip_camera, display_title, display_until, last_scanned_frame

    retry_start = time.time()
    while (not camera_active or shared_picam2 is None) and time.time() - retry_start < 1.5:
        time.sleep(0.1)

    if not camera_active or shared_picam2 is None:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Camera is not active. Start a scan first.")
            )
        )

    def generate_frames():
        font = get_font()
        global shared_picam2, camera_active, display_title, display_until, last_scanned_frame

        while True:
            if (not camera_active or shared_picam2 is None) and (time.time() > display_until):
                break

            if display_title and time.time() < display_until and last_scanned_frame is not None:
                frame = last_scanned_frame.copy()
            else:
                if shared_picam2 is None:
                    break
                try:
                    frame = shared_picam2.capture_array("main")
                except Exception:
                    break

            if flip_camera:
                frame = cv2.rotate(frame, cv2.ROTATE_180)

            if display_title and time.time() < display_until:
                pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_img)

                text = display_title
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                img_width, img_height = pil_img.size
                x = (img_width - text_width) // 2
                y = 30

                padding = 10
                rect_x0 = x - padding
                rect_y0 = y - padding
                rect_x1 = x + text_width + padding
                rect_y1 = y + text_height + padding

                overlay = Image.new("RGBA", pil_img.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=(0, 0, 0, 180))
                pil_img = Image.alpha_composite(pil_img.convert("RGBA"), overlay)

                draw = ImageDraw.Draw(pil_img)
                draw.text((x, y), text, font=font, fill=(255, 255, 255))

                frame = cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/barcode/scan", response_model=ISBNResponse)
def scan_barcode(background_tasks: BackgroundTasks, response: Response):
    global shared_picam2, camera_active, display_title, display_until, last_scanned_frame, camera_session_id

    timeout_seconds = 30
    start_time = time.time()

    try:
        # Reset any previous camera session
        if shared_picam2:
            try:
                shared_picam2.close()
            except Exception:
                pass
            shared_picam2 = None
            camera_active = False

        time.sleep(0.5)

        # Start camera
        shared_picam2 = Picamera2()
        video_config = shared_picam2.create_video_configuration(
            main={"size": (640, 480)},
            controls={"AwbMode": 1}
        )
        shared_picam2.configure(video_config)
        shared_picam2.start()
        time.sleep(0.5)
        metadata = shared_picam2.capture_metadata()

        shared_picam2.set_controls({
            "AwbEnable": False,
            "AeEnable": False,
            "AnalogueGain": metadata["AnalogueGain"],
            "ExposureTime": metadata["ExposureTime"]
        })

        camera_active = True
        camera_session_id = time.time()
        current_session_id = camera_session_id

        # turn the LED solid blue for the duration of the scan
        rgb_on(b=True)

        # Poll for barcodes until timeout
        while time.time() - start_time < timeout_seconds:
            frame = shared_picam2.capture_array("main")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            decoded_barcodes = decode(gray)

            for barcode in decoded_barcodes:
                isbn = barcode.data.decode("utf-8").strip()
                if is_valid_isbn(isbn):
                    # label the frame for display
                    try:
                        book_meta = meta(isbn)
                        title = book_meta.get("Title") or isbn
                    except Exception:
                        title = isbn

                    display_title = title
                    display_until = time.time() + 3

                    # draw polygon on last frame
                    for b in decoded_barcodes:
                        pts = np.array([b.polygon], np.int32)
                        cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                    last_scanned_frame = frame.copy()

                    create_scanned_book_token(isbn, response)

                    # turn off blue before green blink/buzz
                    rgb_on(False, False, False)
                    time.sleep(0.2)
                    buzz_and_blink(g=True)

                    background_tasks.add_task(stop_camera_after_delay, 2.5, current_session_id)
                    return ISBNResponse(
                        code=SUCCESS,
                        message="Successfully retrieved ISBN from barcode",
                        data=isbn
                    )

            time.sleep(0.2)

        # timeout path: turn off blue before red blink/buzz
        rgb_on(False, False, False)
        time.sleep(0.2)
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        background_tasks.add_task(stop_camera_after_delay, 0, current_session_id)
        return JSONResponse(
            status_code=408,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message="Barcode scan timeout: no valid ISBN detected.")
            )
        )

    except Exception as e:
        # exception path: turn off blue before red blink/buzz
        rgb_on(False, False, False)
        time.sleep(0.2)
        buzz_and_blink(r=True, buzz_times=2, blink_times=2)
        background_tasks.add_task(stop_camera_after_delay, 0, camera_session_id)
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                FailResponse(code=FAIL, message=f"Barcode scan failed: {str(e)}")
            )
        )
