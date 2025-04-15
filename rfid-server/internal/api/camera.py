from fastapi import APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
from isbnlib import meta, is_isbn10, is_isbn13
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import time


router = APIRouter()

# Global metadata storage
result_dictionary = {}
last_book = ""

# Initialize and start camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration(
    main={"size": (640, 480)},
    controls={"AwbMode": 1}
)
picam2.configure(video_config)
picam2.start()


def ParseISBN(isbn: str):
    """
    Validate and parse ISBN.
    Returns metadata dictionary if valid, otherwise False.
    """
    if not is_isbn10(isbn) and not is_isbn13(isbn):
        return False
    return meta(isbn)


def ParseMeta(isbn_meta: dict):
    """
    Store and print metadata from ISBN every time.
    """
    print("Title:", isbn_meta.get("Title", "Unknown Title"))
    result_dictionary.update(isbn_meta)


def OutputTXT():
    """
    Output the collected metadata to a text file.
    """
    with open('output.txt', 'w', encoding='utf-8') as f:
        for key, value in result_dictionary.items():
            if isinstance(value, list):
                f.write(f"{key}: {', '.join(value)}\n")
            else:
                f.write(f"{key}: {value}\n")


def GetResult():
    """
    Return the collected metadata dictionary.
    """
    return result_dictionary


def generate_frames():
    last_displayed_title = ""
    last_valid_scan_time = 0
    DISPLAY_DURATION = 5  # seconds to persist the title

    # Load a font that supports Turkish characters (adjust path if needed)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except IOError:
        font = ImageFont.load_default()

    while True:
        frame = picam2.capture_array("main")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        updated = False

        for barcode in decode(gray):
            isbn = barcode.data.decode('utf-8').strip()
            isbn_meta = ParseISBN(isbn)

            if isbn_meta and isinstance(isbn_meta, dict) and "Title" in isbn_meta:
                title = isbn_meta["Title"]
                ParseMeta(isbn_meta)

                if title != last_displayed_title:
                    print("New book scanned:", title)
                    last_displayed_title = title
                    last_valid_scan_time = time.time()
                    updated = True
            else:
                print("Decoded but lookup failed:", isbn)

            pts = np.array([barcode.polygon], np.int32)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Convert frame to PIL Image for proper Unicode text drawing
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if last_displayed_title and (time.time() - last_valid_scan_time < DISPLAY_DURATION or updated):
            draw = ImageDraw.Draw(pil_img)
            draw.text((30, 30), last_displayed_title, font=font, fill=(255, 255, 255))

        # Convert back to OpenCV frame
        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )


@router.get("/video")
def video_feed():
    """
    MJPEG video stream endpoint.
    """
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@router.get("/view", response_class=HTMLResponse)
def view_page():
    """
    Web page displaying the live camera feed.
    """
    return """
    <html>
        <head><title>Live Camera Feed</title></head>
        <body>
            <h1>Live Feed</h1>
            <img src="/api/v1/video" width="640" height="480">
        </body>
    </html>
    """


@router.get("/output")
def get_output():
    """
    Write collected metadata to output.txt and return status message.
    """
    if GetResult():
        OutputTXT()
        return {"message": "Metadata written to output.txt"}
    return {"message": "No valid ISBN scanned yet"}
