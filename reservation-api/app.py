from sqlalchemy.sql.functions import user
from database import *
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy.orm import sessionmaker
from sqlacodegen.codegen import CodeGenerator
from flask_cors import CORS
import dotenv
import io
import os
import sqlalchemy as sq
import sys

# set up request parser for POST
reservation_args = reqparse.RequestParser()
reservation_args.add_argument("user_id", type = int, help = "Enter the users ID. (int)", required = True)
reservation_args.add_argument("hotel_id", type = int, help = "Enter the hotel ID. (int)", required = True)
reservation_args.add_argument("check_in", type = str, help = "Enter the check_in of the reservation. (string)", required = True)
reservation_args.add_argument("check_out", type = str, help = "Enter the check_out of the reservation. (string)", required = True)
reservation_args.add_argument("total_price", type = int, help = "Enter the total price of the reservation (decimal number)", required = True)
reservation_args.add_argument("reserved_standard_count", type = int, help = "Enter the number of standard rooms (int)", required = True)
reservation_args.add_argument("reserved_queen_count", type = int, help = "Enter the number of queen rooms (int)", required = True)
reservation_args.add_argument("reserved_king_count", type = int, help = "Enter the number of king rooms (int)", required = True)



# global variable to set up session
session = None

# load Flask and API
app = Flask(__name__)
api = Api(app)
CORS(app)


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



# function to set a valid json for user object
# returns a list of dictionaries depending on the user query
# outputs each user and reservation in this format:
'''
[
    {
        "user_id": 1,
        "first_name": "Babara",
        "last_name": "MacCaffrey",
        "email": "barbara.Mac@gmail.com",
        "password": "1234",
        "isAdmin": 0,
        "phone_number": "781-932-9754",
        "date_of_birth": "1986-03-28",
        "reservations": [
            {
                "reservation_id": 2,
                "user_id": 1,
                "check_in": "2021-11-14",
                "check_out": "2021-11-17",
                "total_price": 1000.5,
                "reserved_standard_count": 5,
                "reserved_queen_count": 10,
                "reserved_king_count": 2,
                "hotel_information": {
                    "hotel_id": 1,
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
                    "standard_count": 10,
                    "standard_price": 100.0,
                    "queen_count": 5,
                    "queen_price": 150.0,
                    "king_count": 5,
                    "king_price": 250.0
                }
            },
            {
                "reservation_id": 5,
                "user_id": 1,
                "check_in": "2021-11-14",
                "check_out": "2021-11-17",
                "total_price": 1000.5,
                "reserved_standard_count": 5,
                "reserved_queen_count": 10,
                "reserved_king_count": 2,
                "hotel_information": {
                    "hotel_id": 5,
                    "hotel_name": "The Regency Rooms",
                    "street_address": "7 Manley Drive",
                    "city": "Chicago",
                    "state": "IL",
                    "zipcode": 54932,
                    "phone_number": "876-462-1211",
                    "weekend_diff_percentage": 0.25,
                    "number_of_rooms": 20,
                    "amenities": [
                        "Pool",
                        "Gym",
                        "Spa",
                        "Business Office"
                    ],
                    "standard_count": 10,
                    "standard_price": 100.0,
                    "queen_count": 5,
                    "queen_price": 150.0,
                    "king_count": 5,
                    "king_price": 250.0
                }
            }
        ]
    },
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

# generates the list of attributes a hotel has
'''
"amenities": [
                "Pool",
                "Gym",
                "Spa",
                "Business Office"
            ],
'''
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
    if hotel[25]:
        amenities.append("Business Office")
    # check if hotel as wifi
    if hotel.Wifi:
        amenities.append("Wifi")
    return amenities


# function to set a valid json for a user_id
# returns a list of dictionaries depending on the user_id query
# outputs each reservastion in this format:
'''
[
    {
        "reservation_id": 2,
        "user_id": 1,
        "check_in": "2021-11-14",
        "check_out": "2021-11-17",
        "total_price": 1000.5,
        "reserved_standard_count": 5,
        "reserved_queen_count": 10,
        "reserved_king_count": 2,
        "hotel_information": {
            "hotel_id": 1,
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
            "standard_count": 10,
            "standard_price": 100.0,
            "queen_count": 5,
            "queen_price": 150.0,
            "king_count": 5,
            "king_price": 250.0
        }
    }
]
'''
def generate_reservation_entry(user_id):

    try:

        command = f"""select * from reservations, hotel
where reservations.user_id = \"{user_id}\" and hotel.hotel_id = reservations.hotel_id"""
        
        user_reservation = session.execute(command)
        # set up list to return
        result_list = []
        for res in user_reservation:

            # set up dictionary to be added to result list
            new_entry = {}
            hotel_info = {}
            
            # enter each respective variable into the dictionary
            new_entry["reservation_id"] = res.reservation_id
            new_entry["user_id"] = res.user_id
            new_entry["check_in"] = str(res.check_in)
            new_entry["check_out"] = str(res.check_out)
            new_entry["total_price"] = float(res.total_price)
            new_entry["reserved_standard_count"] = res.reserved_standard_count
            new_entry["reserved_queen_count"] = res.reserved_queen_count
            new_entry["reserved_king_count"] = res.reserved_king_count

            # enter the info for the hotel
            hotel_info["hotel_id"] = res.hotel_id
            hotel_info["hotel_name"] = res.hotel_name
            hotel_info["street_address"] = res.street_address
            hotel_info["city"] = res.city
            hotel_info["state"] = res.state
            hotel_info["zipcode"] = res.zipcode
            hotel_info["phone_number"] = res.phone_number
            hotel_info["weekend_diff_percentage"] = float(res.weekend_diff_percentage)
            # calculate total number of rooms
            num_standard = res.standard_count
            num_queen = res.queen_count
            num_king = res.king_count
            total_rooms = num_standard + num_queen + num_king
            hotel_info["number_of_rooms"] = total_rooms
            # set up amenities list
            amenities_list = generate_amenities(res)
            hotel_info["amenities"] = amenities_list
            # set up room_types list
            hotel_info["standard_count"] = res.standard_count
            hotel_info["standard_price"] = float(res.standard_price)
            hotel_info["queen_count"] = res.queen_count
            hotel_info["queen_price"] = float(res.queen_price)
            hotel_info["king_count"] = res.king_count
            hotel_info["king_price"] = float(res.king_price)

            new_entry["hotel_information"] = hotel_info

            # append the new_entry into results if it is not already added
            if new_entry not in result_list:
                result_list.append(new_entry)

    except sq.exc.DBAPIError as e:
        session.rollback()
        return e
    # return results
    return result_list




## ---------- Admin ---------- ##
# class for interacting with all Reservations in the database


class AllReservations(Resource):

    # function to get all hotels from the database
    def get(self):
        # query to get all hotels
        try:
            all_users = session.query(User).order_by(User.user_id).all()
            
            # generate a list from hotels
            result = generate_user_entry(all_users)

            # if there are no hotels, show error
            if not result:
                abort(404, description="There are no users in the database.")
        # return the results
        except sq.exc.DBAPIError as e:
            session.rollback()
            return e

        return result

    def post(self):
        try:
            #checks to see if there are the proper arguments
            args = reservation_args.parse_args()
            # gets the reservation information
            user_id = request.json["user_id"]
            hotel_id = request.json["hotel_id"]
            check_in = request.json["check_in"]
            check_out = request.json["check_out"]
            total_price = request.json["total_price"]
            standard = request.json["reserved_standard_count"]
            queen = request.json["reserved_queen_count"]
            king = request.json["reserved_king_count"]
            # make insert statement for the database
            new_reservation = Reservation( user_id = user_id, hotel_id = hotel_id, check_in = check_in, check_out = check_out,
                                                        total_price = total_price, reserved_standard_count = standard,
                                                        reserved_queen_count = queen, reserved_king_count = king)
            # que the insert and commit the changes
            session.add(new_reservation)
            session.commit()

        except sq.exc.DBAPIError as e:
            session.rollback()
            return e

        return {
            "message":
            f"Reservation ID {new_reservation.reservation_id} was successfully created."
        } 


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
    # function to delete a single reservation from the database by ID number
    def delete(self, reservation_id):
        try:
            result = session.query(Reservation).get(reservation_id)
            
            
            if not result:
                abort(
                    404,
                    description=
                    f"Reservation ID {reservation_id} does not exist in the database."
                )

        
            session.delete(result)
            session.commit()

        except sq.exc.DBAPIError as e:
            session.rollback()
            return e    
        # return message on success
        return {
            "message":
            f"Reservation ID {reservation_id} was successfully deleted."
        }

    def put(self, reservation_id):
        
        try:
            # finds the reservation based on reservation ID
            result = session.query(Reservation).get(reservation_id)
            # if it doesn't exsist error
            if not result:
                abort(
                    404,
                    description=
                    f"Reservation ID {reservation_id} does not exist in the database."
                )
            # checks to see if the necessary argument have been passed 
            args = reservation_args.parse_args()

            result.user_id = request.json["user_id"]
            result.hotel_id = request.json["hotel_id"]
            result.check_in = request.json["check_in"]
            result.check_out = request.json["check_out"]
            result.total_price = request.json["total_price"]
            result.standard = request.json["reserved_standard_count"]
            result.queen = request.json["reserved_queen_count"]
            result.king = request.json["reserved_king_count"]
            
            # update the information in the entry
            session.commit()
        
        except sq.exc.DBAPIError as e:
            session.rollback()
            return e

        # return message on success
        return {
            "message":
            f"Reservation ID {reservation_id} was successfully updated."
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
