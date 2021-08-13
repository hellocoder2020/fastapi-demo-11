from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from api.users import schemas as user_schema
from api.auth import schemas as auth_schema
from api.utils import cryptoUtil, jwtUtil
from api.users import crud as user_crud
from api.auth import crud as auth_crud
import os
from PIL import Image

router = APIRouter(
    prefix='/api/v1'
)


@router.get("/user/profile", response_model=auth_schema.UserList)
async def get_user_profile(currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)):
    return currentUser


@router.patch("/user/profile")
async def update_user(
        request: user_schema.UpdateUser,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # Update user
    await user_crud.update_user(request, currentUser)
    return {"status_code": 200, "detail": "User updated successfully"}


@router.delete("/user/profile")
async def deactivate_account(
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # Delete user
    await user_crud.deactivate_user(currentUser)
    return {
        "status_code": 200,
        "detail": "User account deactivated successfully"
    }


@router.get("/user/get-profile-image")
async def get_profile_image(
    currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    try:
        cwd = os.getcwd()
        path_image_dir = "upload-images/user/profile/"+str(currentUser.id)+"/"
        full_image_path = os.path.join(cwd, path_image_dir, "profile.png")
        if os.path.exists(full_image_path):
            # resize image
            image = Image.open(full_image_path)
            image.thumbnail((400, 400), Image.ANTIALIAS)

            full_new_image_path = os.path.join(cwd, path_image_dir, "profile_400x400.png")
            image.save(full_new_image_path)

            return {"profile_image": os.path.join(path_image_dir, "profile_400x400.png")}
    except Exception as e:
        print(e)
    return {
        "detail": "No such file or directory exists"
    }


@router.patch("/user/upload-profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    try:
        cwd = os.getcwd()
        path_image_dir = "upload-images/user/profile/"+str(currentUser.id)+"/"
        full_image_path = os.path.join(cwd, path_image_dir, file.filename)

        # Create directory if not exist
        if not os.path.exists(path_image_dir):
            os.mkdir(path_image_dir)

        # Rename file
        file_name = full_image_path.replace(file.filename, "profile.png")

        # Write file
        with open(file_name, 'wb+') as f:
            f.write(file.file.read())
            f.flush()
            f.close()

        return {"profile_image": os.path.join(path_image_dir, "profile.png")}

    except Exception as e:
        print(e)


@router.post("/user/change-password")
async def change_password(
        chgPwd: auth_schema.ChangePassword,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    user = await auth_crud.find_existed_user(currentUser.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = auth_schema.UserPWD(**user)
    valid = cryptoUtil.verify_password(chgPwd.old_password, user.password)
    if not valid:
        raise HTTPException(status_code=404, detail="Old password is not match")

    if chgPwd.new_password != chgPwd.confirm_password:
        raise HTTPException(status_code=404, detail="New password is not match.")

    # Change Password
    await user_crud.change_password(chgPwd, currentUser)
    return {"status_code": 200, "detail": "Operating successfully"}


@router.get("/user/logout")
async def logout(
        token: str = Depends(jwtUtil.get_token_user),
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    await user_crud.set_black_list(token, currentUser)
    return {"message": "you logged out successfully"}
