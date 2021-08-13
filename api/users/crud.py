from api.utils.dbUtil import database
from api.utils import cryptoUtil
from api.users import schemas as user_schema
from api.auth import schemas as auth_schema
from api.models import blacklists


def update_user(
    request: user_schema.UpdateUser,
    currentUser: auth_schema.UserList
):
    query = "UPDATE my_users SET fullname=:fullname where email=:email"
    return database.execute(query, values={"fullname": request.fullname, "email": currentUser.email})


def deactivate_user(
    currentUser: auth_schema.UserList
):
    query = "UPDATE my_users SET status='9' where status='1' and email=:email"
    return database.execute(query, values={"email": currentUser.email})


def change_password(
    chgPwd: auth_schema.ChangePassword,
    currentUser: auth_schema.UserList
):
    query = "UPDATE my_users SET password=:password WHERE email=:email"
    return database.execute(query=query, values={"password": cryptoUtil.get_password_hash(chgPwd.new_password),
                                                "email": currentUser.email})


def set_black_list(
    token: str,
    currentUser: auth_schema.UserList
):
    query = blacklists.insert().values(
        token=token,
        email=currentUser.email,
    )
    return database.execute(query)
