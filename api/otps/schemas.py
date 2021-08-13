from pydantic import BaseModel, Field


class CreateOTP(BaseModel):
    recipient_id: str


class VerifyOTP(CreateOTP):
    session_id: str
    otp_code: str


class InfoOTP(VerifyOTP):
    otp_failed_count: int
    status: str

