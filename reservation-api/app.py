from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
# SQLAlchemy imports
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session, mapper
from sqlalchemy.ext.declarative import declarative_base
# Form and table imports
from wtforms import Form, StringField, SelectField
from flask_table import Table, Col, ButtonCol
from flask_table.html import element


# flask instance
app = Flask(__name__)

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

# Automap will create equivalent classes (as opposed to reflection, which only allows querying)
# so that we can create/delete rows
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Reservations = Base.classes.reservations
Hotel_Room_Type = Base.classes.hotel_room_type
Reserved_Room_Type = Base.classes.reserved_room_type
Hotel = Base.classes.hotel

# engine = create_engine(
#    'mysql+pymysql://root:1234567890@localhost/hotel_reservation').connect()

# initial reservation (preliminary test of session adding and committing)
# datetime is formatted as year, month, day, hour, minute
# initial_res = Reservations(reservation_id=1, user_id=1, hotel_id=1,
#                          check_in=datetime(2021, 11, 15), check_out=datetime(2021, 11, 16), total_price=5000, status=0)
# db.session.add(initial_res)
# db.session.commit()
# results = db.session.query(Reservations).all()
# for r in results:
#    print(r.check_out)


# function to load reservations belonging to user_id
def loadUsersRes(user_id):
    return db.session.query(Reservations).filter_by(user_id=user_id).all()


# URL Routes
###################################


# home page for reservations API
@app.route('/')
def index():
    return render_template("index.html")


# this page shows the customers reservations
@app.route('/dashboard', methods=['GET'])
def dashboard(id=1, admin=""):
    # fetch ALL reservations that belong to userID
    usersRes = []
    usersRes = loadUsersRes(id)
    return render_template("dashboard.html", usersRes=usersRes)


'''
# allows customer to delete reservation

@app.route('/reservations')
def delete_res(id, admin):
    print()

# edit reservation


@app.route('/reservastions')
def edit_res(id, admin):  # send in jwt token id
    print()

# Add reservation


@app.route('/reservastions')
def add_res(id, admin):
    print()
'''

if __name__ == "__main__":
    app.run(debug=True)
