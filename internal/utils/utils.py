import bcrypt
import jwt
from fastapi import Request
from config.config import get_config
from internal.models.user import User


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def verify_token_owner(request: Request, user: User, token_name: str) -> bool:
    existing_access_token = request.cookies.get(token_name)
    if existing_access_token:
        payload = jwt.decode(existing_access_token, get_config("secret_key"), algorithms=[get_config("algorithm")])
        user_id = payload.get("id")
        return user_id == user.id
    return False
