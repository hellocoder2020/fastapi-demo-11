from api.utils.dbUtil import database
from api.auth import schemas


def save_user(user: schemas.UserCreate):
    query = "INSERT INTO my_users VALUES (nextval('user_id_seq'), :email, :password, :fullname, now() at time zone 'UTC', '1')"
    return database.execute(query, values={"email": user.email, "password": user.password, "fullname": user.fullname})


def create_reset_code(request: schemas.EmailRequest, reset_code: str):
    query = "INSERT INTO my_codes VALUES (nextval('code_id_seq'), :email, :reset_code, '1', now() at time zone 'UTC')"
    return database.execute(query, values={"email": request.email, "reset_code": reset_code})


def reset_password(new_password: str, email: str):
    query = "UPDATE my_users SET password=:password WHERE email=:email"
    return database.execute(query=query, values={"password": new_password, "email": email})


def disable_reset_code(reset_password_token: str, email: str):
    query = "UPDATE my_codes SET status='9' WHERE status='1' AND reset_code=:reset_code and email=:email"
    return database.execute(query, values={"reset_code": reset_password_token, "email": email})


def find_existed_user(email: str):
    query = "select * from my_users where email=:email and status='1'"
    return database.fetch_one(query, values={"email": email})


def find_token_black_lists(token: str):
    query = "select * from my_blacklists where token=:token"
    return database.fetch_one(query, values={"token": token})


def check_reset_password_token(token: str):
    query = "select * from my_codes where status='1' and reset_code=:token and expired_in >= now() at time zone 'utc' - interval '10 minutes'"
    return database.fetch_one(query, values={"token": token})
