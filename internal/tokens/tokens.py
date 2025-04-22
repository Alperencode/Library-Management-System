from fastapi import Response
from datetime import datetime, timedelta
from config.config import get_config
import jwt


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + expires_delta
    return jwt.encode(to_encode, get_config("secret_key"), algorithm=get_config("algorithm"))


def create_access_token(model_id: str, role: str, response: Response):
    try:
        expire_minutes = get_config("access_token_expire_minutes")
        access_token = create_jwt_token(
            {"id": model_id, "role": role},
            timedelta(minutes=expire_minutes)
        )
        cookie_opts = _get_cookie_options()
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=expire_minutes * 60,
            **cookie_opts
        )
    except Exception as e:
        return e


def create_refresh_token(model_id: str, role: str, response: Response):
    try:
        expire_days = get_config("refresh_token_expire_days")
        refresh_token = create_jwt_token(
            {"id": model_id, "role": role},
            timedelta(days=expire_days)
        )
        cookie_opts = _get_cookie_options()
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=expire_days * 24 * 60 * 60,
            **cookie_opts
        )
    except Exception as e:
        return e


def verify_jwt_token(token: str):
    try:
        return jwt.decode(token, get_config("secret_key"), algorithms=[get_config("algorithm")])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def verify_scanned_book_token(token: str):
    try:
        payload = jwt.decode(token, get_config("secret_key"), algorithms=[get_config("algorithm")])
        return payload.get("book_id"), payload.get("scanned")
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None, None


def _get_cookie_options():
    environment = get_config("environment")
    if environment == "dev":
        return {"secure": False, "samesite": "Lax"}
    return {"secure": True, "samesite": "None"}
