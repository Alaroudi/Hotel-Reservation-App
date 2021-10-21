# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT, TINYTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Amenity(Base):
    __tablename__ = 'amenities'

    amenity_id = Column(Integer, primary_key=True)
    amenity_name = Column(CHAR(70), nullable=False, unique=True)

    hotels = relationship('Hotel', secondary='hotel_amenities')


class Hotel(Base):
    __tablename__ = 'hotel'

    hotel_id = Column(Integer, primary_key=True)
    street_address = Column(String(50), nullable=False)
    city = Column(CHAR(25), nullable=False)
    state = Column(CHAR(2), nullable=False)
    zipcode = Column(Integer, nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    phone_number = Column(CHAR(15), nullable=False)
    hotel_name = Column(String(50), nullable=False)
    weekend_diff_percentage = Column(DECIMAL(3, 2))


class RoomType(Base):
    __tablename__ = 'room_type'

    room_type_id = Column(Integer, primary_key=True)
    room_type_name = Column(String(128), nullable=False, unique=True)


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(CHAR(50), nullable=False)
    last_name = Column(CHAR(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    isAdmin = Column(TINYINT(1), server_default=text("'0'"))
    phone_number = Column(CHAR(15))
    date_of_birth = Column(Date, nullable=False)


t_hotel_amenities = Table(
    'hotel_amenities', metadata,
    Column('hotel_id', ForeignKey('hotel.hotel_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('amenity_id', ForeignKey('amenities.amenity_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class HotelRoomType(Base):
    __tablename__ = 'hotel_room_type'

    room_type_id = Column(ForeignKey('room_type.room_type_id'), primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey('hotel.hotel_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    room_type_count = Column(Integer, nullable=False)
    price_per_night = Column(DECIMAL(10, 2), nullable=False)

    hotel = relationship('Hotel')
    room_type = relationship('RoomType')


class Reservation(Base):
    __tablename__ = 'reservations'

    reservation_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    hotel_id = Column(ForeignKey('hotel.hotel_id'), nullable=False, index=True)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(DECIMAL(10, 2))
    status = Column(TINYTEXT)

    hotel = relationship('Hotel')
    user = relationship('User')


class ReservedRoomType(Base):
    __tablename__ = 'reserved_room_type'

    id = Column(Integer, primary_key=True)
    reservation_id = Column(ForeignKey('reservations.reservation_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    room_type_id = Column(ForeignKey('room_type.room_type_id'), nullable=False, index=True)

    reservation = relationship('Reservation')
    room_type = relationship('RoomType')
