from enum import Enum


class OTPType(str, Enum):
    phone = "Phone"
    email = "Email"
