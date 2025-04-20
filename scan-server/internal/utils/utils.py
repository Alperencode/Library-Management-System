from isbnlib import is_isbn10, is_isbn13
from PIL import ImageFont


def is_valid_isbn(isbn: str) -> bool:
    return is_isbn10(isbn) or is_isbn13(isbn)


def get_font():
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except IOError:
        return ImageFont.load_default()
