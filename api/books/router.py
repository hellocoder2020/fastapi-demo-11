from fastapi import APIRouter, Depends, HTTPException
from api.auth import schemas as auth_schema
from api.books import schemas as book_schema
from api.utils import jwtUtil
from api.books import crud

router = APIRouter(
    prefix='/api/v1'
)


@router.get("/room/book")
async def get_reservation(
        start_date: str,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    return await crud.get_reservation(start_date)


@router.get("/room/book/{book_id}")
async def get_reservation_by_id(
        book_id: int,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    result = await crud.get_reservation_by_id(book_id)
    if not result: result = {}
    return result


@router.post("/room/book")
async def register_new_reservation(
        request: book_schema.CreateBooking,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # (python date time has problem in my pc)
    # Check Start Date is Today or Future
    # local_current_date = dateUtil.get_local_date().strftime("%Y-%m-%d")
    # local_current_date = dateUtil.get_tz_date("Asia/Phnom_Penh").strftime("%Y-%m-%d")
    # if request.start_date < local_current_date:
    #     raise HTTPException(status_code=404, detail="Booking date must greater than or equal current date.")

    # Check Start Time is greater than Now
    # Check End Time is greater than Start Time

    # Check available room
    result = await crud.check_available_booking_room(request)
    if result:
        raise HTTPException(status_code=404, detail="Sorry, It's not available.")

    # Create a reservation
    await crud.register_new_reservation(request, currentUser)

    return {
        "status_code": 200,
        "detail": "Room booked successfully"
    }


@router.put("/room/book/{book_id}")
async def update_reservation_by_id(
        book_id: int,
        request: book_schema.CreateBooking,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # Check available room
    result = await crud.check_available_booking_room(request)
    if result:
        raise HTTPException(status_code=404, detail="Sorry, It's not available.")

    # Update a reservation
    await crud.update_reservation_by_id(book_id, request, currentUser)
    return {
        "status_code": 200,
        "detail": "Room updated successfully"
    }


@router.delete("/room/book/{book_id}")
async def delete_reservation_by_id(
        book_id: int,
        currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user)
):
    # Update a reservation
    await crud.delete_reservation_by_id(book_id, currentUser)

    return {
        "status_code": 200,
        "detail": "Room deleted successfully"
    }
