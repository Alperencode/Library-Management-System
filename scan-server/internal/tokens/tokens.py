from fastapi import Response
from datetime import timedelta, datetime
from config.config import get_config
import jwt


def create_scanned_book_token(book_isbn: str, response: Response):
    payload = {
        "book_isbn": book_isbn,
        "scanned": True,
        "exp": datetime.now() + timedelta(minutes=120)
    }

    token = jwt.encode(payload, get_config("secret_key"), algorithm=get_config("algorithm"))
    cookie_opts = _get_cookie_options()

    response.set_cookie(
        key="scanned_book",
        value=token,
        httponly=True,
        max_age=60*120,
        **cookie_opts
    )


def _get_cookie_options():
    environment = get_config("environment")
    if environment == "dev":
        return {"secure": False, "samesite": "Lax"}
    return {"secure": True, "samesite": "None"}
