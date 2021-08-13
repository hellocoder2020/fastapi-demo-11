import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import schemas
from api.auth import crud
from api.utils import cryptoUtil, constantUtil, emailUtil, jwtUtil
from api.exceptions.business import BusinessException

router = APIRouter(
    prefix='/api/v1'
)


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.find_existed_user(form_data.username)
    if not user:
        raise BusinessException(status_code=999, detail="User not found")

    user = schemas.UserPWD(**user)
    is_valid = cryptoUtil.verify_password(form_data.password, user.password)
    if not is_valid:
        raise BusinessException(status_code=999, detail="Incorrect username or password")

    access_token_expires = jwtUtil.timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwtUtil.create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )

    results = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    results.update({
        "user_info": {
            "email": user.email,
            "fullname": user.fullname
        }
    })

    return results


@router.post("/auth/register")
async def register(user: schemas.UserCreate):
    row = await crud.find_existed_user(user.email)
    if row:
        raise BusinessException(status_code=999, detail="User already registered!")

    # Create new user
    user.password = cryptoUtil.get_password_hash(user.password)
    await crud.save_user(user)

    return {**user.dict()}


@router.post("/auth/forgot-password")
async def forgot_password(request: schemas.EmailRequest):
    # Check exited user
    user = await crud.find_existed_user(request.email)
    if not user:
        raise BusinessException(status_code=999, detail="User not found")

    # Create reset code and save it in database
    reset_code = str(uuid.uuid1())
    await crud.create_reset_code(request, reset_code)

    # Sending email
    subject = "Testing Email For Dev."
    recipient = [request.email]
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">
        <h1>Hello, {0:}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
        <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={1:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """.format(request.email, reset_code)
    await emailUtil.send_email(subject, recipient, message)

    return {
        "code": 200,
        "message": "We've sent an email with instructions to reset your password."
    }


@router.post("/auth/reset-password")
async def reset_password(reset_password_token: str, request: schemas.ResetPassword):
    # Check valid reset password token
    reset_token = await crud.check_reset_password_token(reset_password_token)
    if not reset_token:
        raise BusinessException(status_code=999, detail="Reset password token has expired, please request a new one.")

    # Check both new & confirm password are matched
    if request.new_password != request.confirm_password:
        raise BusinessException(status_code=999, detail="New password is not match.")

    # Reset new password
    code_object = schemas.EmailRequest(**reset_token)
    new_hash_password = cryptoUtil.get_password_hash(request.new_password)
    await crud.reset_password(new_hash_password, code_object.email)

    # Disable reset code
    await crud.disable_reset_code(reset_password_token, code_object.email)

    return {
        "code": 200,
        "message": "Password has been reset successfully"
    }
