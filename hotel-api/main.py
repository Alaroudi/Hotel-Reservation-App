from db import *
from flask import Flask, request, abort
from flask_restful import Api, Resource, fields
from sqlalchemy.orm import sessionmaker
from sqlacodegen.codegen import CodeGenerator
import dotenv
import io
import os
import sqlalchemy as sq
import sys

# global variable to set up session
session = None

# load Flask and API
app = Flask(__name__)
api = Api(app)

# function to generate model
def generate_model(host, user, password, database, outfile = None):
    global session
    # set up mysql engine
    engine = sq.create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    metadata = sq.MetaData(bind = engine)
    metadata.reflect()
    # set up output file for database classes
    outfile = io.open(outfile, "w", encoding = "utf-8") if outfile else sys.stdout
    # generate code and output to outfile
    generator = CodeGenerator(metadata)
    generator.render(outfile)
    
    # generate session
    Session = sessionmaker(bind = engine)
    session = Session()

# function to set a valid json for a hotel object
def generate_hotel_entry(hotel_amenity_results, room_type_results):
    result_list = []
    # for each hotel and amenity object, make a new entry in the result list to be returned
    for hotel, amenity in hotel_amenity_results:
        # set current hotel
        current_hotel = hotel.hotel_id
        # set up dictionary to be added to result_list
        new_entry = {}
        # enter each respective variable into the dictionary
        new_entry["hotel_id"] = hotel.hotel_id
        new_entry["street_address"] = hotel.street_address
        new_entry["city"] = hotel.city
        new_entry["state"] = hotel.state
        new_entry["zipcode"] = hotel.zipcode
        new_entry["number_of_rooms"] = hotel.number_of_rooms
        new_entry["phone_number"] = hotel.phone_number
        new_entry["hotel_name"] = hotel.hotel_name
        new_entry["weekend_diff_percentage"] = float(hotel.weekend_diff_percentage)
        # set up amenities list
        amenities_list = []
        # append each matching amenity that is located in the hotel to the list
        for search_hotel_I, search_amenity in hotel_amenity_results:
            if search_hotel_I.hotel_id == current_hotel:
                amenities_list.append(search_amenity.amenity_name)
        new_entry["amenities"] = amenities_list
        # set up room type list
        room_type_list = []
        # append each matching room type that is located in the hotel to the list
        for search_hotel_II, search_room_type in room_type_results:
            if search_hotel_II.hotel_id == current_hotel:
                # add standard rooms to the list
                if search_room_type.room_type_id == 1:
                    inner_dict = {}
                    inner_dict["price"] = float(search_room_type.price_per_night)
                    inner_dict["count"] = search_room_type.room_type_count
                    standard_dict = {}
                    standard_dict["Standard"] = inner_dict
                    room_type_list.append(standard_dict)
                # add queen rooms to the list
                if search_room_type.room_type_id == 2:
                    inner_dict = {}
                    inner_dict["price"] = float(search_room_type.price_per_night)
                    inner_dict["count"] = search_room_type.room_type_count
                    queen_dict = {}
                    queen_dict["Queen"] = inner_dict
                    room_type_list.append(queen_dict)
                # add king rooms to the list
                if search_room_type.room_type_id == 3:
                    inner_dict = {}
                    inner_dict["price"] = float(search_room_type.price_per_night)
                    inner_dict["count"] = search_room_type.room_type_count
                    king_dict = {}
                    king_dict["King"] = inner_dict
                    room_type_list.append(king_dict)
        new_entry["room_types"] = room_type_list
        # append the entry to the result list
        if new_entry not in result_list:
            result_list.append(new_entry)
    return result_list

## ---------- Hotels ---------- ##
# class for interacting with all hotels in the database
class AllHotels(Resource):
    def get(self):
        # set up list for return
        result = []
        # query to join the matching Hotel and Amenity objects
        hotel_amenity_results = session.query(Hotel, Amenity).select_from(Hotel).join(t_hotel_amenities).filter((t_hotel_amenities.columns.hotel_id == Hotel.hotel_id) & (t_hotel_amenities.columns.amenity_id == Amenity.amenity_id)).all()
        # query to find the matching Hotel and HotelRoomType objects
        room_type_results = session.query(Hotel, HotelRoomType).filter(Hotel.hotel_id == HotelRoomType.hotel_id).all()
        # call function to generate entries
        result = generate_hotel_entry(hotel_amenity_results, room_type_results)
        # if there are no hotels in the database, show error message
        if not result:
            abort(404, description  = "There are no hotels in the database.")
        # return the list of hotels
        return result

# class for interacting with one hotel in the database
class SingleHotel(Resource):
    def get(self, hotel_id):
        # set up list for return
        result = []
        # query to join the matching Hotel and Amenity objects
        hotel_amenity_results = session.query(Hotel, Amenity).select_from(Hotel).join(t_hotel_amenities).filter((t_hotel_amenities.columns.hotel_id == hotel_id) & (t_hotel_amenities.columns.amenity_id == Amenity.amenity_id)).all()
        # query to find the matching Hotel and HotelRoomType objects
        room_type_results = session.query(Hotel, HotelRoomType).filter((Hotel.hotel_id == hotel_id) & (HotelRoomType.hotel_id == hotel_id)).all()
        # call function to generate entry
        result = generate_hotel_entry(hotel_amenity_results, room_type_results)
        # if there is no hotel that matches the id, show error message
        if not result:
            abort(404, description  = "There is no hotel with that id in the database.")
        # return the hotel
        return result[0]

## TODO: POST, PUT and DEL for hotels
#        GET, POST, PUT, and DEL for amenities
#        GET, POST, PUT, and DEL for room_types

# add resources to api
api.add_resource(SingleHotel, "/api/hotels/<int:hotel_id>")
api.add_resource(AllHotels, "/api/hotels")

if __name__ == "__main__":
    # load dotenv
    dotenv.load_dotenv()
    # get username, password, host, and database
    host = os.getenv("host")
    username = os.getenv("user")
    password = os.getenv("password")
    database = os.getenv("database")
    # generate model and output to db.py
    generate_model(host, username, password, database, "db.py")
    app.run(debug = True)