# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Hotel(Base):
    __tablename__ = 'hotel'

    hotel_id = Column(Integer, primary_key=True)
    hotel_name = Column(String(50), nullable=False)
    street_address = Column(String(50), nullable=False)
    city = Column(CHAR(25), nullable=False)
    state = Column(CHAR(2), nullable=False)
    zipcode = Column(Integer, nullable=False)
    phone_number = Column(CHAR(15), nullable=False)
    standard_count = Column(Integer, server_default=text("'0'"))
    queen_count = Column(Integer, server_default=text("'0'"))
    king_count = Column(Integer, server_default=text("'0'"))
    standard_price = Column(DECIMAL(10, 2), server_default=text("'0.00'"))
    queen_price = Column(DECIMAL(10, 2), server_default=text("'0.00'"))
    king_price = Column(DECIMAL(10, 2), server_default=text("'0.00'"))
    Pool = Column(TINYINT(1), server_default=text("'0'"))
    Gym = Column(TINYINT(1), server_default=text("'0'"))
    Spa = Column(TINYINT(1), server_default=text("'0'"))
    Bussiness_Office = Column('Bussiness Office', TINYINT(1), server_default=text("'0'"))
    Wifi = Column(TINYINT(1), server_default=text("'0'"))
    weekend_diff_percentage = Column(DECIMAL(3, 2), server_default=text("'0.00'"))


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


class Reservation(Base):
    __tablename__ = 'reservations'

    reservation_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    hotel_id = Column(Integer, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(DECIMAL(10, 2))
    reserved_standard_count = Column(Integer, server_default=text("'0'"))
    reserved_queen_count = Column(Integer, server_default=text("'0'"))
    reserved_king_count = Column(Integer, server_default=text("'0'"))

    user = relationship('User')
