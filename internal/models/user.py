from pydantic import BaseModel
from internal.utils.utils import (
    hash_password, verify_password, generate_user_id
)


class User(BaseModel):
    def __init__(
        self, username: str, email: str, password: str,
        role: str, access_token: str = ""
    ):
        self.__id = generate_user_id()
        self.__username = username
        self.__email = email
        self.__password = hash_password(password)
        self.__role = role
        self.__access_token = access_token

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = hash_password(password)

    def check_password(self, plain_password):
        return verify_password(plain_password, self.__password)

    def get_role(self):
        return self.__role

    def set_role(self, role):
        self.__role = role

    def get_access_token(self):
        return self.__access_token

    def set_access_token(self, access_token):
        self.__access_token = access_token
