import bcrypt
from jose import jwt
from fastapi import Request
from config.config import get_config
from internal.database.users import get_user_by_id
from internal.database.admins import get_admin_by_id
from internal.database.books import get_book_by_isbn
from internal.types.exceptions import FailResponseException


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def verify_token_owner(request: Request, model, token_name: str) -> bool:
    token = request.cookies.get(token_name)
    if not token:
        return False

    try:
        payload = jwt.decode(token, get_config("secret_key"), algorithms=[get_config("algorithm")])
        return payload.get("id") == model.id and payload.get("role") == model.role
    except jwt.JWTError:
        return False


async def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise FailResponseException(401, "You must be logged in to continue.")

    try:
        payload = jwt.decode(
            access_token,
            get_config("secret_key"),
            algorithms=[get_config("algorithm")]
        )
        user_id = payload.get("id")
        if not user_id:
            raise FailResponseException(401, "Authentication token is invalid or corrupted.")

        user = await get_user_by_id(user_id)
        if not user:
            raise FailResponseException(404, "User account not found. Please contact support.")

        return user

    except jwt.ExpiredSignatureError:
        raise FailResponseException(401, "Your session has expired. Please log in again.")
    except jwt.JWTError:
        raise FailResponseException(401, "Authentication token could not be verified.")


async def get_scanned_book(request: Request):
    token = request.cookies.get("scanned_book")
    if not token:
        raise FailResponseException(401, "Please scan a book to proceed.")

    try:
        payload = jwt.decode(
            token,
            get_config("secret_key"),
            algorithms=[get_config("algorithm")]
        )
        isbn = payload.get("book_isbn")
        scanned = payload.get("scanned")

        if not isbn or not scanned:
            raise FailResponseException(401, "Scanned data is incomplete or invalid.")

        book = await get_book_by_isbn(isbn)
        if not book:
            raise FailResponseException(404, "Scanned book was not found in the library catalog.")

        return book

    except jwt.ExpiredSignatureError:
        raise FailResponseException(401, "Scan expired. Please scan the book again.")
    except jwt.InvalidTokenError:
        raise FailResponseException(401, "The scanned book token is invalid or has been tampered with.")


async def get_current_admin(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise FailResponseException(401, "You must be logged in as an admin to continue.")

    try:
        payload = jwt.decode(
            access_token,
            get_config("secret_key"),
            algorithms=[get_config("algorithm")]
        )
        admin_id = payload.get("id")
        role = payload.get("role")
        if not admin_id or role != "admin":
            raise FailResponseException(401, "Authentication token is invalid or does not belong to an admin.")

        admin = await get_admin_by_id(admin_id)
        if not admin:
            raise FailResponseException(404, "Admin account not found. Please contact support.")

        return admin

    except jwt.ExpiredSignatureError:
        raise FailResponseException(401, "Your session has expired. Please log in again.")
    except jwt.JWTError:
        raise FailResponseException(401, "Authentication token could not be verified.")

