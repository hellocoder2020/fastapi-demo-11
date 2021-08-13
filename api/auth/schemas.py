from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str = Field(..., example="sjdecode@gmail.com")
    password: str = Field(..., example="sjdecode")
    fullname: str = Field(..., example="Neng Channa")


class UserList(BaseModel):
    id: int = None
    email: str
    fullname: str
    created_on: Optional[datetime] = None
    status: str = None


class UserListStatus(UserList):
    status: str


class UserPWD(UserList):
    password: str


class UserBasicInfo(BaseModel):
    id: str
    email: str
    fullname: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: UserBasicInfo


class TokenData(BaseModel):
    email: str = None


class ChangePassword(BaseModel):
    old_password: str = Field(..., example="old password")
    new_password: str = Field(..., example="new password")
    confirm_password: str = Field(..., example="confirm password")


class EmailRequest(BaseModel):
    email: str


class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str
