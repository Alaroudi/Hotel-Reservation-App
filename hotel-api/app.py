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

# set up request parser for POST
hotel_post_args = reqparse.RequestParser()
hotel_post_args.add_argument("hotel_id", type = int, help = "Enter the ID of the hotel. (int)", required = True)
hotel_post_args.add_argument("hotel_name", type = str, help = "Enter the name of the hotel. (string)", required = True)
hotel_post_args.add_argument("street_address", type = str, help = "Enter the street address of the hotel. (string)", required = True)
hotel_post_args.add_argument("city", type = str, help = "Enter the city of the hotel. (string)", required = True)
hotel_post_args.add_argument("state", type = str, help = "Enter the state of the hotel. (2-character string)", required = True)
hotel_post_args.add_argument("zipcode", type = int, help = "Enter the zipcode of the hotel. (5-digit int)", required = True)
hotel_post_args.add_argument("phone_number", type = str, help = "Enter phone number name of the hotel. (string)", required = True)
hotel_post_args.add_argument("weekend_diff_percentage", type = float, help = "Enter the price differential for the weekend of the hotel. (decimal number)", required = True)
hotel_post_args.add_argument("amenities", type = list, help = "Enter the amenities of the hotel. (list of strings)", required = True)
hotel_post_args.add_argument("room_types", type = list, help = "Enter the room type data of the hotel. (list of dictionaries)", required = True)

# set up request parser for PUT
hotel_put_args = reqparse.RequestParser()
hotel_put_args.add_argument("hotel_name", type = str, help = "Enter the name of the hotel. (string)")
hotel_put_args.add_argument("street_address", type = str, help = "Enter the street address of the hotel. (string)")
hotel_put_args.add_argument("city", type = str, help = "Enter the city of the hotel. (string)")
hotel_put_args.add_argument("state", type = str, help = "Enter the state of the hotel. (2-character string)")
hotel_put_args.add_argument("zipcode", type = int, help = "Enter the zipcode of the hotel. (5-digit int)")
hotel_put_args.add_argument("phone_number", type = str, help = "Enter phone number name of the hotel. (string)")
hotel_put_args.add_argument("weekend_diff_percentage", type = float, help = "Enter the price differential for the weekend of the hotel. (decimal number)")
hotel_put_args.add_argument("amenities", type = list, help = "Enter the amenities of the hotel. (list of strings)")
hotel_put_args.add_argument("room_types", type = list, help = "Enter the room type data of the hotel. (list of dictionaries)")


# set up list for valid amenities
valid_amenities = ["Pool", "Gym", "Spa", "Business Office", "Wifi"]

# set up list for valid room_types
valid_room_types = ["Standard", "Queen", "King"]

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

## function to set up amenities list
# returns a list of amenities that the hotel has
def generate_amenities(hotel):
    amenities = []
    # check if hotel has pool
    if hotel.Pool:
        amenities.append("Pool")
    # check if hotel has gym
    if hotel.Gym:
        amenities.append("Gym")
    # check if hotel has spa
    if hotel.Spa:
        amenities.append("Spa")
    # check if hotel has business office
    if hotel.Bussiness_Office:
        amenities.append("Business Office")
    # check if hotel as wifi
    if hotel.Wifi:
        amenities.append("Wifi")
    return amenities

## function to set up the amenity variables for the Hotel class
# returns a set of variables for Pool, Gym, Spa, Business Office, and Wifi
def generate_hotel_amenities(amenities):
    has_pool = 0
    has_gym = 0
    has_spa = 0
    has_bus = 0
    has_wifi = 0
    # go through the list and update each variable
    # hotel has pool
    if "Pool" in amenities:
        has_pool = 1
    # hotel has gym
    if "Gym" in amenities:
        has_gym = 1
    # hotel has spa
    if "Spa" in amenities:
        has_spa = 1
    # hotel has business office
    if "Business Office" in amenities:
        has_bus = 1
    # hotel has wifi
    if "Wifi" in amenities:
        has_wifi = 1
    # return all the values
    return (has_pool, has_gym, has_spa, has_bus, has_wifi)

## function to set up the room_type variables for the Hotel class
# returns a set of variables for the room_type: its count and its price
def generate_hotel_room_type(room_types):
    standard_count = -1
    standard_price = -1
    queen_count = -1
    queen_price = -1
    king_count = -1
    king_price = -1
    # go through the list and store the values of each variable
    for room in room_types:
        # values for standard rooms
        if "Standard" in room:
            # check to see what values are being updated
            for room_type, inner in room.items():
                for key, value in inner.items():
                    # if count is being updated, store the value
                    if key == "count":
                        standard_count = room["Standard"]["count"]
                    # if price is being updated, store the value
                    if key == "price":
                        standard_price = room["Standard"]["price"]
        # values for queen rooms
        if "Queen" in room:
            # check to see what values are being updated
            for room_type, inner in room.items():
                for key, value in inner.items():
                    # if count is being updated, store the value
                    if key == "count":
                        queen_count = room["Queen"]["count"]
                    # if price is being updated, store the value
                    if key == "price":
                        queen_price = room["Queen"]["price"]
        # values for king rooms
        if "King" in room:
            # check to see what values are being updated
            for room_type, inner in room.items():
                for key, value in inner.items():
                    # if count is being updated, store the value
                    if key == "count":
                        king_count = room["King"]["count"]
                    # if price is being updated, store the value
                    if key == "price":
                        king_price = room["King"]["price"]
    # return all the values
    return (standard_count, standard_price, queen_count, queen_price, king_count, king_price)

## function to set up room_types list
# returns a list of dictionaries with the information of each room_type in them
def generate_rooms(hotel):
    # set up room_type list
    rooms = []
    # set up standard inner dictionary
    standard_information = {}
    standard_information["price"] = float(hotel.standard_price)
    standard_information["count"] = hotel.standard_count
    # set up queen inner dictionary
    queen_information = {}
    queen_information["price"] = float(hotel.queen_price)
    queen_information["count"] = hotel.queen_count
    # set up king inner dictionary
    king_information = {}
    king_information["price"] = float(hotel.king_price)
    king_information["count"] = hotel.king_count
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

## function to create a new hotel in the database
# returns a Hotel object with the variables given from POST
# expects input in this format:
'''
{
    "hotel_id": 2,
    "hotel_name": "The Magnolia All Suites",
    "street_address": "14187 Commercial Trail",
    "city": "Hampton",
    "state": "VA",
    "zipcode": 23452,
    "phone_number": "213-342-5433",
    "weekend_diff_percentage": 0.25,
    "number_of_rooms": 20,
    "amenities": [
        "Pool",
        "Gym",
        "Spa",
        "Business Office"
    ],
    "room_types": [
        {
            "Standard": {
                "price": 100.0,
                "count": 10
            }
        },
        {
            "Queen": {
                "price": 150.0,
                "count": 5
            }
        },
        {
            "King": {
                "price": 250.0,
                "count": 5
            }
        }
    ]
}
'''
def generate_new_hotel(hotel_id, hotel_name, street_address, city, state, zipcode, phone_number, weekend_diff_percentage, amenities, room_types):
    # extract data from the list received from amenities
    has_pool = 0
    has_gym = 0
    has_spa = 0
    has_bus = 0
    has_wifi = 0
    for amenity in amenities:
        # if the hotel has a pool, add to hotel
        if amenity == "Pool":
            has_pool = 1
        # if the hotel has a gym, add to hotel
        if amenity == "Gym":
            has_gym = 1
        # if the hotel has a spa, add to hotel
        if amenity == "Spa":
            has_spa = 1
        # if the hotel has a business office, add to hotel
        if amenity == "Business Office":
            has_bus = 1
        # if the hotel has a wifi, add to hotel
        if amenity == "Wifi":
            has_wifi = 1
    # extract data from the list received from room_types
    for room in room_types:
        if "Standard" in room:
            standard_count = room["Standard"]["count"]
            standard_price = room["Standard"]["price"]
        if "Queen" in room:
            queen_count = room["Queen"]["count"]
            queen_price = room["Queen"]["price"]
        if "King" in room:
            king_count = room["King"]["count"]
            king_price = room["King"]["price"]

    # create a new Hotel object from the information provided
    new_hotel = Hotel(hotel_id = hotel_id, hotel_name = hotel_name, street_address = street_address, city = city, state = state, zipcode = zipcode, 
                      phone_number = phone_number, standard_count = standard_count, queen_count = queen_count, king_count = king_count,
                      standard_price = standard_price, queen_price = queen_price, king_price = king_price, Pool = has_pool, Gym = has_gym,
                      Spa = has_spa, Bussiness_Office = has_bus, Wifi = has_wifi, weekend_diff_percentage = weekend_diff_percentage)

    # return the new Hotel object
    return new_hotel

## function to set a valid json for a hotel object
# returns a list of dictionaries depending on the hotel_results query
# outputs each hotel in this format:
'''
{
    "hotel_id": 2,
    "hotel_name": "The Magnolia All Suites",
    "street_address": "14187 Commercial Trail",
    "city": "Hampton",
    "state": "VA",
    "zipcode": 23452,
    "phone_number": "213-342-5433",
    "weekend_diff_percentage": 0.25,
    "number_of_rooms": 20,
    "amenities": [
        "Pool",
        "Gym",
        "Spa",
        "Business Office"
    ],
    "room_types": [
        {
            "Standard": {
                "price": 100.0,
                "count": 10
            }
        },
        {
            "Queen": {
                "price": 150.0,
                "count": 5
            }
        },
        {
            "King": {
                "price": 250.0,
                "count": 5
            }
        }
    ]
}
'''
def generate_hotel_entry(hotel_results):
    # set up list to return
    result_list = []
    for hotel in hotel_results:
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
        num_standard = hotel.standard_count
        num_queen = hotel.queen_count
        num_king = hotel.king_count
        total_rooms = num_standard + num_queen + num_king
        new_entry["number_of_rooms"] = total_rooms
        # set up amenities list
        amenities_list = generate_amenities(hotel)
        new_entry["amenities"] = amenities_list
        # set up room_types list
        room_types_list = generate_rooms(hotel)
        new_entry["room_types"] = room_types_list
        # append the new_entry into results if it is not already added
        if new_entry not in result_list:
            result_list.append(new_entry)
    # return results
    return result_list

## ---------- Hotels ---------- ##
# class for interacting with all hotels in the database
class AllHotels(Resource):
    
    # function to get all hotels from the database
    def get(self):
        # query to get all hotels
        hotels = session.query(Hotel).order_by(Hotel.hotel_id).all()
        # generate a list from hotels
        result = generate_hotel_entry(hotels)

        # if there are no hotels, show error
        if not result:
            abort(404, description  = "There are no hotels in the database.")
        
        # return the results
        return result

    # function to add a new hotel to the database
    def post(self):
        # check to see if the required arguments are passed
        args = hotel_post_args.parse_args()
        # store each token into a variable
        hotel_id = request.json["hotel_id"]
        # check if this hotel_id is already in the database
        result = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).first()
        if result:
            # if it already exists, show error message
            abort(409, f"Hotel ID {hotel_id} already exists in the database.")
        hotel_name = request.json["hotel_name"]
        street_address = request.json["street_address"]
        city = request.json["city"]
        state = request.json["state"]
        zipcode = request.json["zipcode"]
        phone_number = request.json["phone_number"]
        number_of_rooms = request.json["number_of_rooms"]
        weekend_diff_percentage = request.json["weekend_diff_percentage"]
        amenities = request.json["amenities"]
        room_types = request.json["room_types"]

        # check to see if the number_of_rooms matches the total from room_types
        for room in room_types:
            if "Standard" in room:
                standard_count = room["Standard"]["count"]
            if "Queen" in room:
                queen_count = room["Queen"]["count"]
            if "King" in room:
                king_count = room["King"]["count"]
        if number_of_rooms != (standard_count + queen_count + king_count):
            abort(403, description = "The number of rooms does not match the total in room_types.")
        
        # generate the new Hotel object
        new_hotel = generate_new_hotel(hotel_id, hotel_name, street_address, city, state, zipcode, phone_number, weekend_diff_percentage, amenities, room_types)
        
        # add and commit the new hotel to database
        session.add(new_hotel)
        session.commit()

        # return success message
        return {"message": f"Hotel ID {new_hotel.hotel_id} was successfully added to the database."}

# class for interacting with one hotel in the database
class SingleHotel(Resource):

    # function to update information for a single hotel from the database by ID number
    def put(self, hotel_id):
        # select the correct instance
        hotel = session.query(Hotel).get(hotel_id)
        # get the args from the request
        args = hotel_put_args.parse_args()

        # if there is no instance that matches the ID, show error message
        if not hotel:
            abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
        
        # check to see which arguments have values
        if args["hotel_name"]:
            hotel.hotel_name = request.json["hotel_name"]
        if args["street_address"]:
            hotel.street_address = request.json["street_address"]
        if args["city"]:
            hotel.city = request.json["city"]
        if args["state"]:
            hotel.state = request.json["state"]
        if args["zipcode"]:
            hotel.zipcode = request.json["zipcode"]
        if args["phone_number"]:
            hotel.phone_number = request.json["phone_number"]
        if args["weekend_diff_percentage"]:
            hotel.weekend_diff_percentage = request.json["weekend_diff_percentage"]
        if args["amenities"]:
            amenities = request.json["amenities"]
            # check to see if the amenities are valid
            for amenity in amenities:
                if amenity not in valid_amenities:
                    abort(403, description = f"Amenity ({amenity}) is not valid.")
            # get the values
            has_pool, has_gym, has_spa, has_bus, has_wifi = generate_hotel_amenities(amenities)
            # update the hotel with the new values
            hotel.Pool = has_pool
            hotel.Gym = has_gym
            hotel.Spa = has_spa
            hotel.Bussiness_Office = has_bus
            hotel.Wifi = has_wifi
        if args["room_types"]:
            room_types = request.json["room_types"]
            for room in room_types:
                # check to see if the room types are valid
                for key, value in room.items():
                    if key not in valid_room_types:
                        abort(403, description = f"Room type ({key}) is not valid.")
            # get the values
            standard_count, standard_price, queen_count, queen_price, king_count, king_price = generate_hotel_room_type(room_types)
            # update the hotel with the new values if they got changed
            if standard_count != -1:
                hotel.standard_count = standard_count
            if standard_price != -1:
                hotel.standard_price = standard_price
            if queen_count != -1:
                hotel.queen_count = queen_count
            if queen_price != -1:
                hotel.queen_price = queen_price
            if king_count != -1:
                hotel.king_count = king_count
            if king_price != -1:
                hotel.king_price = king_price
        
        # commit the changes to the database
        session.commit()

        # then return the new hotel
        hotels = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).all()
        # generate a list from hotels
        result = generate_hotel_entry(hotels)
        
        # if there are no hotels, show error
        if not result:
            abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
        
        # return the result
        return result[0]
    
    # function to delete a single hotel from the database by ID number
    def delete(self, hotel_id):
        # select the correct instance
        result = session.query(Hotel).get(hotel_id)
        
        # if there is no instance that matches the ID, show error message
        if not result:
            abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
        
        # delete the hotel and commit
        session.delete(result)
        session.commit()

        # return message on success
        return {"message": f"Hotel ID {hotel_id} was successfully deleted."}
    
    # function to get a single hotel from the database by ID number
    def get(self, hotel_id):
        # query to get the hotel and filter by hotel number
        hotels = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).all()
        # generate a list from hotels
        result = generate_hotel_entry(hotels)
        
        # if there are no hotels, show error
        if not result:
            abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
        
        # return the result
        return result[0]


# add to each class to API
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
    # generate model and output to database.py
    generate_model(host, username, password, database, "database.py")
    app.run(debug = True)