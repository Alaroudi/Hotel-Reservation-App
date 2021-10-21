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
Hotel_Room_Type = Base.classes.hotel_room_type
Reserved_Room_Type = Base.classes.reserved_room_type
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

        return jsonify({'message': 'New booking created.'})


# class for updating the booking status
class PromoteBookingStatus(Resource):
    @marshal_with(reservation_resource_fields)
    def put(self, reservation_id):
        Result = db.session.query(Reservations).filter_by(
            reservation_id=reservation_id).first()

        if not Result:
            abort(
                404, description="There is no reservation with that id in the database.")

        # If status is 1, change it to 0 and vice-versa
        if Result.status == "1":
            Result.status = "0"
        else:
            Result.status = "1"
        db.session.commit()

        return jsonify({'message': 'Status on booking has changed!'})


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

        return jsonify({'message': 'Booking has been deleted.'})


# add to each class to API
api.add_resource(AllBookings, "/api/bookings")
api.add_resource(SingleBooking, "/api/bookings/<int:reservation_id>")
api.add_resource(CreateBooking, "/api/bookings")
api.add_resource(PromoteBookingStatus, "/api/bookings/<int:reservation_id>")
api.add_resource(DeleteBooking, "/api/bookings/<int:reservation_id>")

if __name__ == "__main__":
    app.run(debug=True)


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
