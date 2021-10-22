from db import *
from flask import Flask, request, abort, jsonify
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
            # for the current hotel, add the room_type data
            if search_hotel_II.hotel_id == current_hotel:
                # set up dictionary for price and count
                inner_dict = {}
                inner_dict["price"] = float(search_room_type.price_per_night)
                inner_dict["count"] = search_room_type.room_type_count
                # set up dictionary to hold the information for the outer dictionary
                type_dict = {}
                # get the correct room_type
                query = session.query(RoomType).filter(RoomType.room_type_id == search_room_type.room_type_id).first()
                # store the name of the room_type
                room_type_name = query.room_type_name
                # add the data to the outer dictionary
                type_dict[room_type_name] = inner_dict
                # append that to the list
                room_type_list.append(type_dict)
        new_entry["room_types"] = room_type_list
        # append the entry to the result list
        if new_entry not in result_list:
            result_list.append(new_entry)
    return result_list

# function to set a valid json for an amenity object
def generate_amenity_entry(amenity_results):
    result_list = []
    for amenity in amenity_results:
        # set current amenity
        current_amenity = amenity.amenity_id
        # set up dictionary to be added to result_list
        new_entry = {}
        # enter each respective variable into the dictionary
        new_entry["amenity_id"] = amenity.amenity_id
        new_entry["amenity_name"] = amenity.amenity_name
        if new_entry not in result_list:
            result_list.append(new_entry)
    return result_list

# function to set a valid json for a room_type object
def generate_room_type_entry(room_type_results):
    result_list = []
    for room_type in room_type_results:
        # set current amenity
        current_room_type = room_type.room_type_id
        # set up dictionary to be added to result_list
        new_entry = {}
        # enter each respective variable into the dictionary
        new_entry["room_type_id"] = room_type.room_type_id
        new_entry["room_type_name"] = room_type.room_type_name
        if new_entry not in result_list:
            result_list.append(new_entry)
    return result_list

## ---------- SingleResource ---------- ##
# class for interacting with any class that deals with a single resource
class SingleResource(Resource):

    # function to delete an instance of a SingleResource
    def delete(self, table, id):
        # select the correct instance
        result = session.query(table).get(id)
        # if there is no instance that matches the ID, show error message
        if not result:
            abort(404, description  = f"ID {id} does not exist in the database.")
        
        # delete the hotel and commit
        session.delete(result)
        session.commit()

## ---------- Hotels ---------- ##
# class for interacting with all hotels in the database
class AllHotels(Resource):
    
    # function to add a new hotel to the database
    def post(self):
        # store each token into a variable
        hotel_id = request.json["hotel_id"]
        street_address = request.json["street_address"]
        city = request.json["city"]
        state = request.json["state"]
        zipcode = request.json["zipcode"]
        number_of_rooms = request.json["number_of_rooms"]
        phone_number = request.json["phone_number"]
        hotel_name = request.json["hotel_name"]
        weekend_diff_percentage = request.json["weekend_diff_percentage"]
        amenities = request.json["amenities"]
        room_types = request.json["room_types"]

        # check if this hotel_id is already in the database
        result = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).first()
        if result:
            abort(409, f"Hotel ID {hotel_id} already exists in the database.")

        # check if the number_of_rooms matches the total given in the room_types variable
        count = 0
        # for each room type
        for check in room_types:
            # tally up the number of rooms
            count += check[1][1]
        if count != number_of_rooms:
            abort(403, description = "The number of rooms does not match the total given in room_types.")

        # create a new Hotel object
        new_hotel = Hotel(hotel_id = hotel_id, street_address = street_address, city = city, state = state, zipcode = zipcode, number_of_rooms = number_of_rooms,  
                          phone_number = phone_number, hotel_name = hotel_name, weekend_diff_percentage = weekend_diff_percentage)
        
        # for each amenity 
        for amenity_id in amenities:
            # set current amenity
            current_amenity = session.query(Amenity).filter(Amenity.amenity_id == amenity_id).first()
            # if the amenity doesn't exist, send error message
            if not current_amenity:
                # delete new hotel and commit
                session.delete(new_hotel)
                session.commit()
                abort(409, description = f"Amenity ID {amenity_id} does not exist in the database.")
            # add the hotel to the current amenity
            current_amenity.hotels.append(new_hotel)

        # for each room type
        for room_type in room_types:
            # set current room_type
            current_room_type = session.query(RoomType).filter(RoomType.room_type_id == room_type[0]).first()
            # if the room_type doesn't exist, send error message
            if not current_room_type:
                # delete new hotel and commit
                session.delete(new_hotel)
                session.commit()
                abort(409, description = f"Room Type ID {room_type[0]} does not exist in the database.")
            
            # create new HotelRoomType object
            new_hotel_room_type = HotelRoomType(room_type_id = room_type[0], hotel_id = hotel_id, room_type_count = room_type[1][1], price_per_night = room_type[1][0])
            
            # add and commit new hotel room type to database
            session.add(new_hotel_room_type)
            session.commit()
        
        # add and commit new hotel to the database
        session.add(new_hotel)
        session.commit()
        return {"message": f"Hotel ID {hotel_id} was successfully added to the database."}
    
    # function to get all hotels in the database
    def get(self):
        # set up list for return
        result = []
        # query to join the matching Hotel and Amenity objects
        hotel_amenity_results = session.query(Hotel, Amenity).select_from(Hotel).join(t_hotel_amenities).filter((t_hotel_amenities.columns.hotel_id == Hotel.hotel_id) & (t_hotel_amenities.columns.amenity_id == Amenity.amenity_id)).order_by(Hotel.hotel_id).all()
        # query to find the matching Hotel and HotelRoomType objects
        room_type_results = session.query(Hotel, HotelRoomType).filter(Hotel.hotel_id == HotelRoomType.hotel_id).order_by(Hotel.hotel_id).all()
        # call function to generate entries
        result = generate_hotel_entry(hotel_amenity_results, room_type_results)
        # if there are no hotels in the database, show error message
        if not result:
            abort(404, description  = "There are no hotels in the database.")
        # return the list of hotels
        return result

## TODO: PUT for SingleHotel

# class for interacting with one hotel in the database
class SingleHotel(SingleResource):
    
    # function to delete a hotel
    def delete(self, hotel_id):
        super().delete(Hotel, hotel_id)
        return {"message": f"Hotel ID {hotel_id} was successfully deleted."}

    # function to get a single hotel in the database by hotel_id
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
            abort(404, description  = f"Hotel ID {hotel_id} does not exist in the database.")
        # return the hotel
        return result[0]

## ---------- Amenities ---------- ##
# class for interacting with all amenities in the database
class AllAmenities(Resource):
    
    # function to get all amenities in the database
    def get(self):
        # set up list for return
        result = []
        # query to find all Amenity objects
        amenity_results = session.query(Amenity).order_by(Amenity.amenity_id).all()
        # call function to generate entry
        result = generate_amenity_entry(amenity_results)
        # if there are no amenities in the database, show error message
        if not result:
            abort(404, description = "There are no amenities in the database.")
        # return the list of amenities
        return result

    # function to add a new amenity into the database
    def post(self):
        # store each token into a variable
        amenity_id = request.json["amenity_id"]
        amenity_name = request.json["amenity_name"]

        # check if this amenity_id is already in the database
        result = session.query(Amenity).filter(Amenity.amenity_id == amenity_id).first()
        if result:
            (409, f"Amenity ID {amenity_id} exists in the database.")
        
        # create a new RoomType object
        new_amenity = Amenity(amenity_id = amenity_id, amenity_name = amenity_name)

        # add and commit new amenity to database
        session.add(new_amenity)
        session.commit()
        return {"message": f"Amenity ID {amenity_id} was successfully added to the database."}

## TODO: PUT for Single Amenity

# class for interacting with one amenity in the database
class SingleAmenity(SingleResource):
    
    # function to delete an amenity
    def delete(self, amenity_id):
        super().delete(Amenity, amenity_id)
        return {"message": f"Amenity ID {amenity_id} was successfully deleted."}
    
    # function to get a single amenity in the database by amenity_id
    def get(self, amenity_id):
        # set up list for return
        result = []
        # query to find all Amenity objects
        amenity_results = session.query(Amenity).filter(Amenity.amenity_id == amenity_id).all()
        # call function to generate entry
        result = generate_amenity_entry(amenity_results)
        # if there are no amenities in the database, show error message
        if not result:
            abort(404, description = f"Amenity ID {amenity_id} already exists in the database.")
        # return the list of amenities
        return result[0]

## ---------- Room Types ---------- ##
# class for interacting with all room types in the database
class AllRoomTypes(Resource):
    
    # function to get all room types in the database
    def get(self):
        # set up list for return
        result = []
        # query to find all RoomType objects
        room_type_results = session.query(RoomType).order_by(RoomType.room_type_id).all()
        # call function to generate entry
        result = generate_room_type_entry(room_type_results)
        # if there are no room type in the database, show error message
        if not result:
            abort(404, description = "There are no room types in the database.")
        # return the list of room types
        return result

    # function to add a new room_type to the database
    def post(self):
        # store each token into a variable
        room_type_id = request.json["room_type_id"]
        room_type_name = request.json["room_type_name"]

        # check if this room_type_id is already in the database
        result = session.query(RoomType).filter(RoomType.room_type_id == room_type_id).first()
        if result:
            (409, f"Room type ID {room_type_id} exists in the database.")
        
        # create a new RoomType object
        new_room_type = RoomType(room_type_id = room_type_id, room_type_name = room_type_name)

        # add and commit new room_type to database
        session.add(new_room_type)
        session.commit()
        return {"message": f"Room type ID {room_type_id} was successfully added to the database."}

## TODO: PUT for SingleRoomType

# class for interacting with one room type in the database
class SingleRoomType(SingleResource):
    
    # function to delete a room_type
    def delete(self, room_type_id):
        super().delete(RoomType, room_type_id)
        return {"message": f"Room_type ID {room_type_id} was successfully deleted."}
    
    # function to get a single room type in the database by room_type_id
    def get(self, room_type_id):
        # set up list for return
        result = []
        # query to find all RoomType objects
        room_type_results = session.query(RoomType).filter(RoomType.room_type_id == room_type_id).all()
        # call function to generate entry
        result = generate_room_type_entry(room_type_results)
        # if there are no room type in the database, show error message
        if not result:
            abort(404, description = f"Room type ID {room_type_id} already exists in the database.")
        # return the list of room types
        return result[0]

# add resources to api
# Hotel resources
api.add_resource(SingleHotel, "/api/hotels/<int:hotel_id>")
api.add_resource(AllHotels, "/api/hotels")
# Amenity resources
api.add_resource(SingleAmenity, "/api/amenities/<int:amenity_id>")
api.add_resource(AllAmenities, "/api/amenities")
# RoomType resources
api.add_resource(SingleRoomType, "/api/room_types/<int:room_type_id>")
api.add_resource(AllRoomTypes, "/api/room_types")

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