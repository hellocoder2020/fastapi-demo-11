from api.utils.dbUtil import database
from api.otps import schemas


def find_otp_block(recipient_id: str):
    query = "select * from my_otp_blocks where recipient_id=:recipient_id and created_on >= now() at time zone 'utc' - interval '5 minutes'"
    return database.fetch_one(query, values={"recipient_id": recipient_id})


def find_otp_life_time(recipient_id: str, session_id: str):
    query = "select * from my_otps where recipient_id=:recipient_id and session_id=:session_id and " \
            "created_on >= now() at time zone 'utc' - interval '1 minutes'"
    return database.fetch_one(query, values={"recipient_id": recipient_id, "session_id": session_id})


def save_otp(
    request: schemas.CreateOTP,
    session_id: str,
    otp_code: str
):
    query = "INSERT INTO my_otps(id, recipient_id, session_id, otp_code, status, created_on, otp_failed_count) " \
            "VALUES (nextval('otp_id_seq'), :recipient_id, :session_id, :otp_code, '1', now() at time zone 'UTC', 0)"
    return database.execute(query, values={"recipient_id": request.recipient_id, "session_id": session_id, "otp_code": otp_code})


def save_otp_failed_count(request: schemas.VerifyOTP):
    print(request)
    query = "UPDATE my_otps SET otp_failed_count=otp_failed_count+1 where recipient_id=:recipient_id and session_id=:session_id and otp_code=:otp_code"
    return database.execute(query,
                           values={"recipient_id": request.recipient_id, "session_id": request.session_id,
                                   "otp_code": request.otp_code})


def save_block_otp(request: schemas.VerifyOTP):
    query = "INSERT INTO my_otp_blocks VALUES (nextval('otp_block_id_seq'), :recipient_id, now() at time zone 'UTC')"
    return database.execute(query, values={"recipient_id": request.recipient_id})


def disable_otp(request: schemas.VerifyOTP):
    query = "UPDATE my_otps SET status='9' where recipient_id=:recipient_id and session_id=:session_id and otp_code=:otp_code"
    return database.execute(query, values={"recipient_id": request.recipient_id, "session_id": request.session_id,
                                          "otp_code": request.otp_code})
