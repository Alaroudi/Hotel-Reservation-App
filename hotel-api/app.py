from database import *
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
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
hotel_post_args.add_argument("hotel_name", type = str, help = "Enter the name of the hotel. (string)", required = True)
hotel_post_args.add_argument("street_address", type = str, help = "Enter the street address of the hotel. (string)", required = True)
hotel_post_args.add_argument("city", type = str, help = "Enter the city of the hotel. (string)", required = True)
hotel_post_args.add_argument("state", type = str, help = "Enter the state of the hotel. (2-character string)", required = True)
hotel_post_args.add_argument("zipcode", type = int, help = "Enter the zipcode of the hotel. (5-digit int)", required = True)
hotel_post_args.add_argument("phone_number", type = str, help = "Enter phone number name of the hotel. (string)", required = True)
hotel_post_args.add_argument("weekend_diff_percentage", type = float, help = "Enter the price differential for the weekend of the hotel. (decimal number)", required = True)
hotel_post_args.add_argument("amenities", type = list, help = "Enter the amenities of the hotel. (list of strings)", required = True)
hotel_post_args.add_argument("standard_count", type = int, help = "Enter number of standard rooms. (int)", required = True)
hotel_post_args.add_argument("standard_price", type = float, help = "Enter price of standard rooms. (float)", required = True)
hotel_post_args.add_argument("queen_count", type = int, help = "Enter number of queen rooms. (int)", required = True)
hotel_post_args.add_argument("queen_price", type = float, help = "Enter price of queen rooms. (float)", required = True)
hotel_post_args.add_argument("king_count", type = int, help = "Enter number of king rooms. (int)", required = True)
hotel_post_args.add_argument("king_price", type = float, help = "Enter price of king rooms. (float)", required = True)

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
hotel_put_args.add_argument("standard_count", type = int, help = "Enter number of standard rooms. (int)")
hotel_put_args.add_argument("standard_price", type = float, help = "Enter price of standard rooms. (float)")
hotel_put_args.add_argument("queen_count", type = int, help = "Enter number of queen rooms. (int)")
hotel_put_args.add_argument("queen_price", type = float, help = "Enter price of queen rooms. (float)")
hotel_put_args.add_argument("king_count", type = int, help = "Enter number of king rooms. (int)")
hotel_put_args.add_argument("king_price", type = float, help = "Enter price of king rooms. (float)")

# set up list for valid amenities
valid_amenities = ["Pool", "Gym", "Spa", "Business Office", "Wifi"]

# global variable to set up session
session = None

# load Flask and API
app = Flask(__name__)
api = Api(app)
CORS(app)

# function to generate model
def generate_model(host, user, password, database, outfile = None):
    global session
    
    # set up mysql engine
    try:
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
    except sq.exc.DBAPIError as e:
        abort(500, description = "The database is offline.")

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

## function to create a new hotel in the database
# returns a Hotel object with the variables given from POST
# expects input in this format:
def generate_new_hotel(hotel_name,
                       street_address,
                       city,
                       state,
                       zipcode,
                       phone_number,
                       weekend_diff_percentage,
                       amenities,
                       standard_count,
                       standard_price,
                       queen_count,
                       queen_price,
                       king_count,
                       king_price):
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
    # update room_type information
    standard_count = standard_count
    standard_price = standard_price
    queen_count = queen_count
    queen_price = queen_price
    king_count = king_count
    king_price = king_price

    # create a new Hotel object from the information provided
    new_hotel = Hotel(hotel_name = hotel_name,
                      street_address = street_address,
                      city = city,
                      state = state, 
                      zipcode = zipcode, 
                      phone_number = phone_number, 
                      standard_count = standard_count, 
                      queen_count = queen_count, 
                      king_count = king_count,
                      standard_price = standard_price, 
                      queen_price = queen_price, 
                      king_price = king_price, 
                      Pool = has_pool, 
                      Gym = has_gym,
                      Spa = has_spa,
                      Bussiness_Office = has_bus, 
                      Wifi = has_wifi, 
                      weekend_diff_percentage = weekend_diff_percentage)

    # return the new Hotel object
    return new_hotel

## function to set a valid json for a hotel object
# returns a list of dictionaries depending on the hotel_results query
# outputs each hotel in this format:
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
        new_entry["standard_count"] = hotel.standard_count
        new_entry["standard_price"] = float(hotel.standard_price)
        new_entry["queen_count"] = hotel.queen_count
        new_entry["queen_price"] = float(hotel.queen_price)
        new_entry["king_count"] = hotel.king_count
        new_entry["king_price"] = float(hotel.king_price)
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
        try:
            hotels = session.query(Hotel).order_by(Hotel.hotel_id).all()
        except sq.exc.DBAPIError as e:
            session.rollback()
            abort(500, description = "The database server is offline.")
        else:
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
        hotel_name = request.json["hotel_name"]
        street_address = request.json["street_address"]
        # check if this hotel already exists in the database
        try:
            result = session.query(Hotel).filter((Hotel.hotel_name == hotel_name) & (Hotel.street_address == street_address)).first()
        except sq.exc.DBAPIError as e:
            session.rollback()
            abort(500, description = "The database server is offline.")
        else:
            if result:
                # if it already exists, show error message
                abort(400, f"This hotel already exists in the database. (Hotel ID {result.hotel_id})")
            city = request.json["city"]
            state = request.json["state"]
            zipcode = request.json["zipcode"]
            phone_number = request.json["phone_number"]
            weekend_diff_percentage = request.json["weekend_diff_percentage"]
            amenities = request.json["amenities"]
            standard_count = request.json["standard_count"]
            standard_price = request.json["standard_price"]
            queen_count = request.json["queen_count"]
            queen_price = request.json["queen_price"]
            king_count = request.json["king_count"]
            king_price = request.json["king_price"]

            # generate the new Hotel object
            new_hotel = generate_new_hotel(hotel_name,
                                           street_address,
                                           city,
                                           state,
                                           zipcode,
                                           phone_number,
                                           weekend_diff_percentage,
                                           amenities,
                                           standard_count,
                                           standard_price,
                                           queen_count,
                                           queen_price,
                                           king_count,
                                           king_price)
            
            # add and commit the new hotel to database
            try:
                session.add(new_hotel)
                session.commit()
            except sq.exc.DBAPIError as e:
                session.rollback()
                abort(500, description = "The database server is offline.")
            else:
                # return success message
                return {"message": f"Hotel ID {new_hotel.hotel_id} was successfully added to the database."}

# class for interacting with one hotel in the database
class SingleHotel(Resource):

    # function to update information for a single hotel from the database by ID number
    def put(self, hotel_id):
        # select the correct instance
        try:
            hotel = session.query(Hotel).get(hotel_id)
        except sq.exc.DBAPIError as e:
            session.rollback()
            abort(500, description = "The database server is offline.")
        else:
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
                        abort(400, description = f"Amenity ({amenity}) is not valid.")
                # get the values
                has_pool, has_gym, has_spa, has_bus, has_wifi = generate_hotel_amenities(amenities)
                # update the hotel with the new values
                hotel.Pool = has_pool
                hotel.Gym = has_gym
                hotel.Spa = has_spa
                hotel.Bussiness_Office = has_bus
                hotel.Wifi = has_wifi
            if args["standard_count"]:
                hotel.standard_count = request.json["standard_count"]
            if args["standard_price"]:
                hotel.standard_count = request.json["standard_price"]
            if args["queen_count"]:
                hotel.standard_count = request.json["queen_count"]
            if args["queen_price"]:
                hotel.standard_count = request.json["queen_price"]
            if args["king_count"]:
                hotel.standard_count = request.json["king_count"]
            if args["king_price"]:
                hotel.standard_count = request.json["king_price"]
            # commit the changes to the database
            try:
                session.commit()
            except sq.exc.DBAPIError as e:
                session.rollback()
                abort(500, description = "The database server is offline.")
            else:
                # then return the new hotel
                try:
                    hotels = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).all()
                except sq.exc.DBAPIError as e:
                    session.rollback()
                    abort(500, description = "The database server is offline.")
                else:
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
        try:
            result = session.query(Hotel).get(hotel_id)
        except sq.exc.DBAPIError as e:
            session.rollback()
            abort(500, description = "The database server is offline.")
        else:
            # if there is no instance that matches the ID, show error message
            if not result:
                abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
            
            # delete the hotel and commit
            try:
                session.delete(result)
                session.commit()
            except sq.exc.DBAPIError as e:
                session.rollback()
                abort(500, description = "The database server is offline.")
            else:
                # return message on success
                return {"message": f"Hotel ID {hotel_id} was successfully deleted."}
    
    # function to get a single hotel from the database by ID number
    def get(self, hotel_id):
        # query to get the hotel and filter by hotel number
        try:
            hotels = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).all()
        except sq.exc.DBAPIError as e:
            session.rollback()
            abort(500, description = "The database server is offline.")
        else:
            # generate a list from hotels
            result = generate_hotel_entry(hotels)
            
            # if there are no hotels, show error
            if not result:
                abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
            
            # return the result
            return result[0]

# hotel_reservation_results = session.query(Hotel, Reservation)....
## function to generate a valid json object for a hotel entry
# returns a list of dictionaries depending on the hotel_results query and reservation query
def generate_availability_entry(hotel_reservation_results):
    # set up list to return
    result_list = []
    reserved_dict = {}
    # first loop to tally up the number of reserved rooms per hotel
    for hotel, reservation in hotel_reservation_results:
        # if the reservation is for the hotel, update the information
        if hotel.hotel_id == reservation.hotel_id:
            # if the hotel's information hasn't been initialized, initialize it
            if hotel.hotel_id not in reserved_dict:
                information_dict = {}
                information_dict["Standard"] = hotel.standard_count
                information_dict["Queen"] = hotel.queen_count
                information_dict["King"] = hotel.king_count
                reserved_dict[hotel.hotel_id] = information_dict
            # update the number of available rooms for the hotel
            reserved_dict[hotel.hotel_id]["Standard"] = reserved_dict[hotel.hotel_id]["Standard"] - reservation.reserved_standard_count
            reserved_dict[hotel.hotel_id]["Queen"] = reserved_dict[hotel.hotel_id]["Queen"] - reservation.reserved_queen_count
            reserved_dict[hotel.hotel_id]["King"] = reserved_dict[hotel.hotel_id]["King"] - reservation.reserved_king_count
    # second loop to make the entries
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
        if hotel.hotel_id in reserved_dict:
            # if the there were reservations in the hotel, update the output to reflect them
            num_standard = reserved_dict[hotel.hotel_id]["Standard"]
            num_queen = reserved_dict[hotel.hotel_id]["Queen"]
            num_king = reserved_dict[hotel.hotel_id]["King"]
        else:
            # if there were no reservations in the hotel, keep the output the default number of rooms
            num_standard = hotel.standard_count
            num_queen = hotel.queen_count
            num_king = hotel.king_count
        total_available_rooms = num_standard + num_queen + num_king
        new_entry["number_of_available_rooms"] = total_available_rooms
        # set up amenities list
        amenities_list = generate_amenities(hotel)
        new_entry["amenities"] = amenities_list
        new_entry["standard_count"] = num_standard
        new_entry["standard_price"] = float(hotel.standard_price)
        new_entry["queen_count"] = num_queen
        new_entry["queen_price"] = float(hotel.queen_price)
        new_entry["king_count"] = num_king
        new_entry["king_price"] = float(hotel.king_price)
        # append the new_entry into results if it is not already added
        if new_entry not in result_list:
            result_list.append(new_entry)
    # return results
    return result_list

## ---------- Availability ---------- ##
# class to interact with hotel availability
class HotelAvailability(Resource):

    # function to get availablity of a hotel according to check-in, check-out, and city
    def get(self):
        # parse the arguments passed through the api
        args = request.args
        # we expect city, check_in, and check_out
        try:
            city = args["city"]
            check_in = args["check_in"]
            check_out = args["check_out"]
        # if the request does not have all three, abort with 400
        except:
            abort(400, description = "Must provide for city, check_in, and check_out.")
        else:
            try:
                # find all the hotels cities with hotels that have check in and check out on the given days
                hotel_reservation_results = session.query(Hotel, Reservation).filter((Hotel.city == city) & 
                                                                                     (Reservation.check_in >= check_in) & 
                                                                                     (Reservation.check_out <= check_out)).all()
            except sq.exc.DBAPIError as e:
                abort(500, description = "The database is offline.")
            else:
                # if there are no hotels, show error
                if not hotel_reservation_results:
                    abort(400, description  = f"There are no hotels that are in that city ({city}).")
                results = generate_availability_entry(hotel_reservation_results)
                return results

# add to each class to API
api.add_resource(SingleHotel, "/api/hotels/<int:hotel_id>")
api.add_resource(AllHotels, "/api/hotels")
api.add_resource(HotelAvailability, "/api/hotel-availability/")

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