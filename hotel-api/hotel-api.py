from flask import Flask, request, abort
from flask_restful import Api, Resource, fields, marshal_with
import sqlalchemy as sq

app = Flask(__name__)
api = Api(app)
# change username and password to connect to database
engine = sq.create_engine("mysql+pymysql://username:password@localhost/hotel_reservation")
connection = engine.connect()
metadata = sq.MetaData()
# set up tables from the database
hotels = sq.Table("hotel", metadata, autoload = True, autoload_with = engine)
hotel_amenities = sq.Table("hotel_amenities", metadata, autoload = True, autoload_with = engine)
amenities = sq.Table("amenities", metadata, autoload = True, autoload_with = engine)

# for proper output of hotels
hotel_resource_fields = {
    'hotel_id': fields.Integer,
    'street_address': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zipcode': fields.Integer,
    'number_of_rooms': fields.Integer,
    'phone_number': fields.String,
    'hotel_name': fields.String,
    'weekend_diff_percentage': fields.Float
}

# for proper output of amenities
amenities_resource_fields = {
    'amenity_id': fields.Integer,
    'amenity_name': fields.String
}

# for proper output of hotel_amenities
hotel_amenities_resource_fields = {
    'hotel_id': fields.Integer,
    'amenity_id': fields.String
}

## ---------- Hotels ---------- ##
# class for interacting with all hotels in the database
class AllHotels(Resource):
    @marshal_with(hotel_resource_fields)
    def get(self):
        query = sq.select([hotels]).order_by(hotels.columns.hotel_id)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        if not ResultSet:
            abort(404, description  = "There are no hotels in the database.")
        return ResultSet

# class for interacting with one hotel in the database
class SingleHotel(Resource):
    @marshal_with(hotel_resource_fields)
    def get(self, hotel_id):
        query = sq.select([hotels]).where(hotels.columns.hotel_id == hotel_id)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        if not ResultSet:
            abort(404, description  = "There is no hotel with that id in the database.")
        return ResultSet

## ---------- Amenities ---------- ##
# class for interacting with all amenities in the database
class AllAmenities(Resource):
    @marshal_with(amenities_resource_fields)
    def get(self):
        query = sq.select([amenities]).order_by(amenities.columns.amenity_id)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        if not ResultSet:
            abort(404, description  = "There are no amenities in the database.")
        return ResultSet

# class for interacting with one amenity in the database
class SingleAmenity(Resource):
    @marshal_with(amenities_resource_fields)
    def get(self, amenity_id):
        query = sq.select([amenities]).where(amenities.columns.amenity_id == amenity_id)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        if not ResultSet:
            abort(404, description  = "There is no amenity with that id in the database.")
        return ResultSet

## ---------- Hotel_Amenities ---------- ##
# class for interacting with all hotel_amenities in the database
class AllHotelAmenities(Resource):
    @marshal_with(hotel_amenities_resource_fields)
    def get(self):
        query = sq.select([hotel_amenities]).order_by(hotel_amenities.columns.hotel_id)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        if not ResultSet:
            abort(404, description  = "There are no hotels_amenities in the database.")
        return ResultSet

# class for interacting with one hotel in the database
class SingleHotelAmenities(Resource):
    @marshal_with(hotel_amenities_resource_fields)
    def get(self, hotel_id):
        query = sq.select([hotel_amenities]).where(hotel_amenities.columns.hotel_id == hotel_id).order_by(hotel_amenities.columns.amenity_id)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        if not ResultSet:
            abort(404, description  = "There is no hotel with that id in the database.")
        return ResultSet

# add to each class to API
api.add_resource(SingleHotel, "/api/hotels/<int:hotel_id>")
api.add_resource(AllHotels, "/api/hotels")
api.add_resource(SingleAmenity, "/api/amenities/<int:amenity_id>")
api.add_resource(AllAmenities, "/api/amenities")
api.add_resource(SingleHotelAmenities, "/api/hotel_amenities/<int:hotel_id>")
api.add_resource(AllHotelAmenities, "/api/hotel_amenities")

if __name__ == "__main__":
    app.run(debug = True)