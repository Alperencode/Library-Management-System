from pydantic import BaseModel, Field, field_validator
from internal.utils.utils import hash_password, verify_password, generate_user_id


class User(BaseModel):
    id: str = Field(default_factory=generate_user_id)
    username: str
    email: str
    password: str
    role: str
    refresh_token: str = ""

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, value: str) -> str:
        return hash_password(value)

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.password)

    def to_dict(self):
        user_data = self.model_dump()
        del user_data["password"]
        return user_data
