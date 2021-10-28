from app import generate_amenities
from database import *
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy.orm import sessionmaker
from sqlacodegen.codegen import CodeGenerator
import dotenv
import io
import os
import sqlalchemy as sq
import sys

## function to set up room_types list
# returns a list of dictionaries with the information of each room_type in them
def generate_available_rooms(hotel, num_standard, num_queen, num_king):
    # set up room_type list
    rooms = []
    # set up standard inner dictionary
    standard_information = {}
    standard_information["price"] = float(hotel.standard_price)
    standard_information["count"] = num_standard
    # set up queen inner dictionary
    queen_information = {}
    queen_information["price"] = float(hotel.queen_price)
    queen_information["count"] = num_queen
    # set up king inner dictionary
    king_information = {}
    king_information["price"] = float(hotel.king_price)
    king_information["count"] = num_king
    # set up standard outer dictionary and add to rooms
    standard_dict = {}
    standard_dict["Standard"] = standard_information
    rooms.append(standard_dict)
    # set up queen outer dictionary and add to rooms
    queen_dict = {}
    queen_dict["Queen"] = queen_information
    rooms.append(queen_dict)
    # set up king outer dictionary and add to rooms
    king_dict = {}
    king_dict["King"] = king_information
    rooms.append(king_dict)
    return rooms

# hotel_reservation_results = session.query(Hotel, Reservation)....
## function to generate a valid json object for a hotel entry
# returns a list of dictionaries depending on the hotel_results query and reservation query
def generate_availability_entry(hotel_reservation_results):
    # set up list to return
    result_list = []
    for hotel, reservation in hotel_reservation_results:
        # set up dictionary to be added to result list
        new_entry = {}
        # enter each respective variable into the dictionary
        new_entry["hotel_id"] = hotel.hotel_id
        new_entry["hotel_name"] = hotel.hotel_name
        new_entry["street_address"] = hotel.street_address
        new_entry["city"] = hotel.city
        new_entry["state"] = hotel.state
        new_entry["zipcode"] = hotel.zipcode
        new_entry["phone_number"] = hotel.phone_number
        new_entry["weekend_diff_percentage"] = float(hotel.weekend_diff_percentage)
        # calculate total number of rooms
        num_standard = hotel.standard_count - reservation.reserved_standard_count
        num_queen = hotel.queen_count - reservation.reserved_queen_count
        num_king = hotel.king_count - reservation.reserved_king_count
        total_available_rooms = num_standard + num_queen + num_king
        new_entry["number_of_available_rooms"] = total_available_rooms
        # set up amenities list
        amenities_list = generate_amenities(hotel)
        new_entry["amenities"] = amenities_list
        # set up room_types list
        room_types_list = generate_available_rooms(hotel, num_standard, num_queen, num_king)
        new_entry["available_room_types"] = room_types_list
        # append the new_entry into results if it is not already added
        if new_entry not in result_list:
            result_list.append(new_entry)
    # return results
    return result_list
