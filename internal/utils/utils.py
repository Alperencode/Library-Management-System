import os
import secrets
import bcrypt
import uuid
from dotenv import load_dotenv


def generate_user_id() -> str:
    return str(uuid.uuid4())


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_secret_key(env_path=".env") -> str:
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")

    if not secret_key:
        secret_key = secrets.token_hex(32)
        with open(env_path, "a") as env_file:
            env_file.write(f"\nSECRET_KEY={secret_key}")

    return secret_key
