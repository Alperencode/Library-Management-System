from pydantic import BaseModel

SUCCESS = "Success"
FAIL = "Fail"


class WriteRequest(BaseModel):
    text: str
