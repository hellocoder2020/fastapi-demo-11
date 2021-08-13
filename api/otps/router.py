import uuid
from fastapi import APIRouter, HTTPException
from api.otps import schemas
from api.utils import otpUtil, emailUtil
from api.enums import otp
from api.otps import crud

router = APIRouter(
    prefix='/api/v1'
)


@router.post("/otp/send")
async def send_otp(
    type: otp.OTPType,
    request: schemas.CreateOTP
):
    # Check block OTP
    opt_blocks = await crud.find_otp_block(request.recipient_id)
    if opt_blocks:
        raise HTTPException(status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

    # Generate and save to table OTPs
    otp_code = otpUtil.random(6)
    session_id = str(uuid.uuid1())
    await crud.save_otp(request, session_id, otp_code)

    # Send OTP to email
    if type == otp.OTPType.email:
        # Sending email
        subject = "OTP Code"
        recipient = [request.recipient_id]
        message = """
            <!DOCTYPE html>
            <html>
            <title>Reset Password</title>
            <body>
            <div style="width:100%;font-family: monospace;">
                <h1>{0:}</h1>
            </div>
            </body>
            </html>
            """.format(otp_code)

        await emailUtil.send_email(subject, recipient, message)

    else:
        print("OTP via phone number")

    return {
        "session_id": session_id,
        "otp_code": otp_code
    }


@router.post("/otp/verify")
async def verify_otp(request: schemas.VerifyOTP):
    # Check block OTP
    opt_blocks = await crud.find_otp_block(request.recipient_id)
    if opt_blocks:
        raise HTTPException(status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

    # Check OTP code 6 digit life time
    otp_result = await crud.find_otp_life_time(request.recipient_id, request.session_id)
    if not otp_result:
        raise HTTPException(status_code=404, detail="OTP code has expired, please request a new one.")

    otp_result = schemas.InfoOTP(**otp_result)

    # Check if OTP code is already used
    if otp_result.status == "9":
        raise HTTPException(status_code=404, detail="OTP code has used, please request a new one.")

    # Verify OTP code, if not verified,
    if otp_result.otp_code != request.otp_code:
        # Increment OTP failed count
        await crud.save_otp_failed_count(otp_result)

        # If OTP failed count = 5
        # then block otp
        if otp_result.otp_failed_count + 1 == 5:
            await crud.save_block_otp(otp_result)
            raise HTTPException(status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

        # Throw exceptions
        raise HTTPException(status_code=404, detail="The OTP code you've entered is incorrect.")

    # Disable otp code when succeed verified
    await crud.disable_otp(otp_result)

    return {
        "status_code": 200,
        "detail": "OTP verified successfully"
    }
