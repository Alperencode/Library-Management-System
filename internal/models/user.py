from pydantic import BaseModel, Field, field_validator
from internal.utils.utils import hash_password, verify_password, generate_user_id


class User(BaseModel):
    id: str = Field(default_factory=generate_user_id)
    username: str
    email: str
    password: str
    role: str

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, value: str) -> str:
        return hash_password(value)

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.password)

    def __setattr__(self, name, value):
        if name == "id" and hasattr(self, "id"):
            raise AttributeError("The 'id' field is immutable and cannot be changed after creation.")
        super().__setattr__(name, value)


class PublicUser(BaseModel):
    id: str
    username: str
    email: str
    role: str
