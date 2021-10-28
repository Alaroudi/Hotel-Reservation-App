from sqlalchemy.sql.functions import user
from database import *
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource
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


def generate_model(host, user, password, database, outfile=None):
    global session

    # set up mysql engine
    engine = sq.create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}")
    metadata = sq.MetaData(bind=engine)
    metadata.reflect()
    # set up output file for database classes
    outfile = io.open(outfile, "w",
                      encoding="utf-8") if outfile else sys.stdout
    # generate code and output to outfile
    generator = CodeGenerator(metadata)
    generator.render(outfile)

    # generate session
    Session = sessionmaker(bind=engine)
    session = Session()



# function to create a new hotel in the database
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


def generate_new_hotel():
    # store each token into a variable
    hotel_id = request.json["hotel_id"]
    # check if this hotel_id is already in the database
    result = session.query(Hotel).filter(Hotel.hotel_id == hotel_id).first()
    if result:
        # if it already exists, return the hotel_id
        return hotel_id
    # continue if it doesn't
    hotel_name = request.json["hotel_name"]
    street_address = request.json["street_address"]
    city = request.json["city"]
    state = request.json["state"]
    zipcode = request.json["zipcode"]
    phone_number = request.json["phone_number"]
    number_of_rooms = request.json["number_of_rooms"]
    weekend_diff_percentage = request.json["weekend_diff_percentage"]
    # extract data from the list received from amenities
    amenities = request.json["amenities"]
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
    rooms = request.json["room_types"]
    for room in rooms:
        if "Standard" in room:
            standard_count = room["Standard"]["count"]
            standard_price = room["Standard"]["price"]
        if "Queen" in room:
            queen_count = room["Queen"]["count"]
            queen_price = room["Queen"]["price"]
        if "King" in room:
            king_count = room["King"]["count"]
            king_price = room["King"]["price"]

    # check if the number of rooms matches the total of all the room types
    if number_of_rooms != (standard_count + queen_count + king_count):
        abort(403,
              description=
              "The number of rooms does not match the total in room_types.")

    # create a new Hotel object from the information provided
    new_hotel = Hotel(hotel_id=hotel_id,
                      hotel_name=hotel_name,
                      street_address=street_address,
                      city=city,
                      state=state,
                      zipcode=zipcode,
                      phone_number=phone_number,
                      standard_count=standard_count,
                      queen_count=queen_count,
                      king_count=king_count,
                      standard_price=standard_price,
                      queen_price=queen_price,
                      king_price=king_price,
                      Pool=has_pool,
                      Gym=has_gym,
                      Spa=has_spa,
                      Bussiness_Office=has_bus,
                      Wifi=has_wifi,
                      weekend_diff_percentage=weekend_diff_percentage)

    # return the new Hotel object
    return new_hotel


# function to set a valid json for user object
# returns a list of dictionaries depending on the user query
# outputs each user and reservation in this format:
'''
{
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "John.Doe@yahoo.com",
    "password": "1234",
    "isAdmin": 0,
    "phone_number": "210-222-2222",
    "date_of_birth": 2000-12-12,
    "reservations": [
        {   
            "reservation_id": 1,
            "user_id": 1,
            "hotel_id": 1,
            "check_in": "2021-12-12",
            "check_out": "2021-12-15",
            "total_price": 100.56,
            "reserved_standard_count": "1",
            "reserved_queen_count": 0,
            "reserved_king_count": 1
        },
        {
            "reservation_id": 12,
            "user_id": 1,
            "hotel_id": 4,
            "check_in": "2022-1-12",
            "check_out": "2022-1-25",
            "total_price": 1000.56,
            "reserved_standard_count": "1",
            "reserved_queen_count": 1,
            "reserved_king_count": 12
        }
    ]
}
'''


def generate_user_entry(user_results):
    # set up list to return
    result_list = []
    for cur_user in user_results:
        # set up dictionary to be added to result list
        new_entry = {}
        
        # enter each respective variable into the dictionary
        new_entry["user_id"] = cur_user.user_id
        new_entry["first_name"] = cur_user.first_name
        new_entry["last_name"] = cur_user.last_name
        new_entry["email"] = cur_user.email
        new_entry["password"] = cur_user.password
        new_entry["isAdmin"] = cur_user.isAdmin
        new_entry["phone_number"] = cur_user.phone_number
        new_entry["date_of_birth"] = str(cur_user.date_of_birth)

        # set up reservations
        reservation_info = generate_reservation_entry(cur_user.user_id)
        new_entry["reservations"] = reservation_info
        
        # append the new_entry into results if it is not already added
        if new_entry not in result_list:
            result_list.append(new_entry)
    # return results
    return result_list

# function to set a valid json for a user_id
# returns a list of dictionaries depending on the user_id query
# outputs each reservastion in this format:
'''
{
    [
        {   
            "reservation_id": 1,
            "user_id": 1,
            "hotel_id": 1,
            "check_in": "2021-12-12",
            "check_out": "2021-12-15",
            "total_price": 100.56,
            "reserved_standard_count": "1",
            "reserved_queen_count": 0,
            "reserved_king_count": 1
        },
        {
            "reservation_id": 12,
            "user_id": 1,
            "hotel_id": 4,
            "check_in": "2022-1-12",
            "check_out": "2022-1-25",
            "total_price": 1000.56,
            "reserved_standard_count": "1",
            "reserved_queen_count": 1,
            "reserved_king_count": 12
        }
    ]
}
'''


def generate_reservation_entry(user_id):
    user_reservation = session.query(Reservation).filter(Reservation.user_id == user_id).order_by(Reservation.reservation_id).all()

    # set up list to return
    result_list = []
    for res in user_reservation:
        # set up dictionary to be added to result list
        new_entry = {}
        
        # enter each respective variable into the dictionary
        new_entry["reservation_id"] = res.reservation_id
        new_entry["user_id"] = res.user_id
        new_entry["hotel_id"] = res.hotel_id
        new_entry["check_in"] = str(res.check_in)
        new_entry["check_out"] = str(res.check_out)
        new_entry["total_price"] = float(res.total_price)
        new_entry["reserved_standard_count"] = res.reserved_standard_count
        new_entry["reserved_queen_count"] = res.reserved_queen_count
        new_entry["reserved_king_count"] = res.reserved_king_count

        # append the new_entry into results if it is not already added
        if new_entry not in result_list:
            result_list.append(new_entry)
    # return results
    return result_list




## ---------- Admin ---------- ##
# class for interacting with all Reservations in the database


class AllReservations(Resource):

    # function to get all hotels from the database
    def get(self):
        # query to get all hotels
        all_users = session.query(User).order_by(User.user_id).all()
        # generate a list from hotels
        result = generate_user_entry(all_users)

        # if there are no hotels, show error
        if not result:
            abort(404, description="There are no users in the database.")
        # return the results
        return result



## ---------- User ---------- ##
# class for interacting with user Reservations in the database

class UserReservation(Resource):
    
    # function to get a user reservations based on user_id from the database
    def get(self, user_id):

        # generate a list from hotels
        result = generate_reservation_entry(user_id)

        # if there are no hotels, show error
        if not result:
            abort(404,
                  description=
                  f"USER ID {user_id} does not exist in the database.")

        # return the result
        return result
    


class SingleBooking(Resource):
    # function to delete a single hotel from the database by ID number
    def delete(self, reservation_id):
        result = session.query(Reservation).get(reservation_id)
        if not result:
            abort(
                404,
                description=
                f"Reservation ID {reservation_id} does not exist in the database."
            )

        session.delete(result)
        session.commit()

        # return message on success
        return {
            "message":
            f"Reservation ID {reservation_id} was successfully deleted."
        }

    

    

# add to each class to API
api.add_resource(UserReservation, "/api/user/<int:user_id>")
api.add_resource(AllReservations, "/api/user")
api.add_resource(SingleBooking, "/api/bookings/<int:reservation_id>")

if __name__ == "__main__":
    # load dotenv
    dotenv.load_dotenv()
    # get username, password, host, and database
    host = os.getenv("host")
    username = os.getenv("user")
    password = os.getenv("password")
    database = os.getenv("database")
    # generate model and output to db.py
    generate_model(host, username, password, database, "database.py")
    app.run(debug=True)
'''
from flask import Flask, request, jsonify, abort
from datetime import datetime, date
# SQLAlchemy imports
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session, mapper
from sqlalchemy.ext.declarative import declarative_base
# Flask RESTful
from flask_restful import Api, Resource, fields, marshal_with
import json

# flask instance
app = Flask(__name__)

# declare RESTful api
api = Api(app)

# add database
# replace password with your servers password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234567890@localhost/hotel_reservation'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234567890"
)

cursor = mydb.cursor()

# test for cursor
# cursor.execute("SHOW DATABASES")
# for db in cursor:
#    print(db)

# connectes to the actual database for flask to make the pages
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Reservations = Base.classes.reservations
Hotel = Base.classes.hotel


# for proper output of bookings
reservation_resource_fields = {
    'reservation_id': fields.Integer,
    'user_id': fields.Integer,
    'hotel_id': fields.Integer,
    'check_in': fields.DateTime(dt_format='iso8601'),
    'check_out': fields.DateTime(dt_format='iso8601'),
    'total_price': fields.Float,
    'status': fields.String
}

## ---------- bookings ---------- ##


# class for getting all bookings in the database
class AllBookings(Resource):
    @marshal_with(reservation_resource_fields)
    def get(self):
        ResultSet = db.session.query(Reservations).all()

        if not ResultSet:
            abort(404, description="There are no bookings in the database.")
        return ResultSet


# class for getting one hotel in the database
class SingleBooking(Resource):
    @marshal_with(reservation_resource_fields)
    def get(self, reservation_id):
        Result = db.session.query(Reservations).filter_by(
            reservation_id=reservation_id).first()

        if not Result:
            abort(
                404, description="There is no reservation with that id in the database.")
        return Result


# class for creating one hotel in the database
class CreateBooking(Resource):
    @marshal_with(reservation_resource_fields)
    def post(self):
        data = request.get_json()

        new_reservation = Reservations(reservation_id=data['reservation_id'], user_id=data['user_id'], hotel_id=data['hotel_id'],
                                       check_in=data['check_in'], check_out=data['check_out'], total_price=data['total_price'], status=data['status'])
        db.session.add(new_reservation)
        db.session.commit()

        return {'message': 'New booking created.'}


# class for updating the booking status
class IncrementStandardBooking(Resource):
    @marshal_with(reservation_resource_fields)
    def put(self, reservation_id):
        Result = db.session.query(Reservations).filter_by(
            reservation_id=reservation_id).first()

        if not Result:
            abort(
                404, description="There is no reservation with that id in the database.")

        db.session.commit()

        return {'message': 'Status on booking has changed!'}


# class for deleting a booking
class DeleteBooking(Resource):
    @marshal_with(reservation_resource_fields)
    def delete(self, reservation_id):
        Result = db.session.query(Reservations).filter_by(
            reservation_id=reservation_id).first()

        if not Result:
            abort(
                404, description="There is no reservation with that id in the database.")

        db.session.delete(Result)
        db.session.commit()

        return{'message': 'Booking has been deleted.'}


# add to each class to API
api.add_resource(AllBookings, "/api/bookings")
api.add_resource(SingleBooking, "/api/bookings/<int:reservation_id>")
api.add_resource(CreateBooking, "/api/bookings")
api.add_resource(PromoteBookingStatus, "/api/bookings/<int:reservation_id>")
api.add_resource(DeleteBooking, "/api/bookings/<int:reservation_id>")

if __name__ == "__main__":
    app.run(debug=True)

'''
'''

@app.route('/bookings', methods=['GET'])
def get_all_reservations():
    reservations = db.session.query(Reservations).all()

    output = []
    for res in reservations:
        res_data = {}
        res_data['reservation_id'] = res.reservation_id
        res_data['user_id'] = res.user_id
        res_data['hotel_id'] = res.hotel_id
        res_data['check_in'] = res.check_in
        res_data['check_out'] = res.check_out
        res_data['total_price'] = res.total_price
        res_data['status'] = res.status
        output.append(res_data)

    return jsonify({'bookings': output})


@app.route('/bookings/<id>', methods=['GET'])
def get_one_reservation(id):
    res = db.session.query(Reservations).filter_by(reservation_id=id).first()

    if not res:
        return jsonify({'message': 'No booking found!'})

    res_data = {}
    res_data['reservation_id'] = res.reservation_id
    res_data['user_id'] = res.user_id
    res_data['hotel_id'] = res.hotel_id
    res_data['check_in'] = res.check_in
    res_data['check_out'] = res.check_out
    res_data['total_price'] = res.total_price
    res_data['status'] = res.status

    return jsonify({'bookings': res_data})


@app.route('/bookings', methods=['POST'])
def create_reservation():
    data = request.get_json()

    new_reservation = Reservations(reservation_id=data['reservation_id'], user_id=data['user_id'], hotel_id=data['hotel_id'],
                                   check_in=data['check_in'], check_out=data['check_out'], total_price=data['total_price'], status=data['status'])
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({'message': 'New booking created.'})


@app.route('/bookings/<id>', methods=['PUT'])
def promote_status_reservation(id):
    res = db.session.query(Reservations).filter_by(reservation_id=id).first()

    if not res:
        return jsonify({'message': 'No booking found!'})

    res.status = 1
    db.session.commit()

    return jsonify({'message': 'Status on booking has changed!'})


@app.route('/bookings/<id>', methods=['DELETE'])
def delete_reservation(id):
    res = db.session.query(Reservations).filter_by(reservation_id=id).first()

    if not res:
        return jsonify({'message': 'No booking found!'})

    db.session.delete(res)
    db.session.commit()

    return jsonify({'message': 'Booking has been deleted.'})


if __name__ == "__main__":

    app.run(debug=True)
'''
