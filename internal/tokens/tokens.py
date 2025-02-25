import jwt
from datetime import datetime, timedelta
from config.config import get_config


def create_jwt_token(data, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + expires_delta
    return jwt.encode(to_encode, get_config("secret_key"), algorithm=get_config("algorithm"))


def create_access_token(user):
    return create_jwt_token(
        {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        },
        timedelta(minutes=get_config("access_token_expire_minutes"))
    )


def create_refresh_token(user):
    return create_jwt_token(
        {"id": user["id"]},
        timedelta(days=get_config("refresh_token_expire_days"))
    )


def verify_jwt_token(token):
    try:
        return jwt.decode(token, get_config("secret_key"), algorithms=[get_config("algorithm")])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
