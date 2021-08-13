from pydantic import BaseModel


class CreateBooking(BaseModel):
    agenda: str
    start_date: str
    start_time: str
    end_time: str
    room_id: int


class ListBookingRoom(CreateBooking):
    id: int
    status: str
    register_id: str
    created_on: str
    updated_on: str
