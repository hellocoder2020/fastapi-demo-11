from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence

metadata = MetaData()

users = Table(
    'my_users', metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('email', String(100)),
    Column('password', String(100)),
    Column('fullname', String(50)),
    Column('created_on', DateTime),
    Column('status', String(1)),
)

otps = Table(
    'my_otps', metadata,
    Column('id', Integer, Sequence('otp_id_seq'), primary_key=True),
    Column('recipient_id', String(100)),
    Column('session_id', String(100)),
    Column('otp_code', String(6)),
    Column('status', String(1)),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('otp_failed_count', Integer, default=0),
)

otpBlocks = Table(
    'my_otp_blocks', metadata,
    Column('id', Integer, Sequence('otp_block_id_seq'), primary_key=True),
    Column('recipient_id', String(100)),
    Column('created_on', DateTime),
)

blacklists = Table(
    'my_blacklists', metadata,
    Column('token', String(250), primary_key=True),
    Column('email', String(100)),
)
codes = Table(
    'my_codes', metadata,
    Column('id', Integer, Sequence('code_id_seq'), primary_key=True),
    Column('email', String(100)),
    Column('reset_code', String(50)),
    Column('status', String(1)),
    Column('expired_in', DateTime),
)

rooms = Table(
    'my_rooms', metadata,
    Column('id', Integer, Sequence('room_id_seq'), primary_key=True),
    Column('name', String(100)),
    Column('status', String(1)),
)

bookings = Table(
    'my_bookings', metadata,
    Column('id', Integer, Sequence('book_id_seq'), primary_key=True),
    Column('agenda', String(100)),
    Column('start_date', String(10)),
    Column('start_time', String(6)),
    Column('end_time', String(6)),
    Column('room_id', Integer),
    Column('register_id', String(100)),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('status', String(1)),
)
