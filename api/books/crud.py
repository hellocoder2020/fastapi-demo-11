from api.utils.dbUtil import database
from api.models import bookings
from api.auth import schemas as auth_schema
from api.books import schemas as book_schema


def check_available_booking_room(request: book_schema.CreateBooking):
    query = "select * from my_bookings where status='1' and start_date=:start_date and room_id=:room_id and end_time > :start_time and start_time < :end_time"
    return database.fetch_one(query, values={"start_date": request.start_date, "room_id": request.room_id,
                                             "start_time": request.start_time, "end_time": request.end_time})


def get_reservation(start_date: str):
    query = bookings.select().where(bookings.columns.start_date == start_date)
    return database.fetch_all(query)


def get_reservation_by_id(book_id: int):
    query = bookings.select().where(bookings.columns.id == book_id)
    return database.fetch_one(query)


def register_new_reservation(
    request: book_schema.CreateBooking,
    currentUser: auth_schema.UserList
):
    query = "INSERT INTO my_bookings VALUES (nextval('book_id_seq'), :agenda, :start_date, :start_time, :end_time, :room_id, :register_id, now() at time zone 'UTC', now() at time zone 'UTC', '1')"
    return database.execute(query, values={"agenda": request.agenda, "start_date": request.start_date,
                                          "start_time": request.start_time, "end_time": request.end_time,
                                          "room_id": request.room_id, "register_id": currentUser.email})


def update_reservation_by_id(
    book_id: int,
    request: book_schema.CreateBooking,
    currentUser: auth_schema.UserList
):
    query = "UPDATE my_bookings SET agenda=:agenda, start_date=:start_date, start_time=:start_time, end_time=:end_time, room_id=:room_id, updated_on=now() at time zone 'UTC' where id=:book_id and register_id=:register_id"
    return database.execute(query, values={"agenda": request.agenda, "start_date": request.start_date,
                                          "start_time": request.start_time, "end_time": request.end_time,
                                          "room_id": request.room_id, "book_id": book_id, "register_id":currentUser.email})


def delete_reservation_by_id(
    book_id: int,
    currentUser: auth_schema.UserList
):
    query = "UPDATE my_bookings SET status='9' where status='1' and id=:book_id and register_id=:register_id"
    return database.execute(query, values={"book_id": book_id, "register_id": currentUser.email})
