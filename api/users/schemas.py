from pydantic import BaseModel


class UpdateUser(BaseModel):
    fullname: str