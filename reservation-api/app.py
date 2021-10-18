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


# names of hotels match id's
hotel_names = {}
hotel_list = db.session.query(Hotel).order_by(Hotel.hotel_id).all()

for i in hotel_list:
    hotel_names[i.hotel_id] = str(i.hotel_name)


# engine = create_engine(
#    'mysql+pymysql://root:1234567890@localhost/hotel_reservation').connect()

# initial reservation (preliminary test of session adding and committing)
# datetime is formatted as year, month, day, hour, minute
'''
for i in range(1, 10):
    if i % 5 == 1:
        initial_res = Reservations(reservation_id=1 + i, user_id=1, hotel_id=i+1,
                                   check_in=datetime(2021, 11, 15), check_out=datetime(2021, 11, 16), total_price=5000 + 50 * i, status=0)
    elif i % 5 == 2:
        initial_res = Reservations(reservation_id=1 + i, user_id=2, hotel_id=i,
                                   check_in=datetime(2021, 11, 15), check_out=datetime(2021, 11, 16), total_price=5000 + 50 * i, status=0)
    elif i % 5 == 3:
        initial_res = Reservations(reservation_id=1 + i, user_id=2, hotel_id=2,
                                   check_in=datetime(2021, 11, 15), check_out=datetime(2021, 11, 16), total_price=5000 + 50 - i, status=0)
    elif i % 5 == 4:
        initial_res = Reservations(reservation_id=1 + i, user_id=3, hotel_id=4,
                                   check_in=datetime(2021, 11, 15), check_out=datetime(2021, 11, 16), total_price=5000 + 50 + i, status=0)
    else:
        initial_res = Reservations(reservation_id=1 + i, user_id=4, hotel_id=10,
                                   check_in=datetime(2021, 11, 15), check_out=datetime(2021, 11, 16), total_price=5000 + 50 / i, status=0)

    db.session.add(initial_res)

db.session.commit()
'''
# results = db.session.query(Reservations).all()
# for r in results:
#    print(r.check_out)


# function to load reservations belonging to user_id
def loadUsersRes(user_id):
    return db.session.query(Reservations).filter_by(user_id=user_id).all()


# function to load the reservation with reservation_id
def loadResByResID(reservation_id):
    return db.session.query(Reservations).filter_by(reservation_id=reservation_id).first()


# Update Functions
###################################
# updates a reservation for a customer
@app.route('/updateRes', methods=['POST'])
def updateRes():
    formID = request.form.get('formID')
    newCheckIn = request.form.get("newCheckIn")
    newCheckOut = request.form.get("newCheckOut")

    # fetch the reservation with reservation_id (formID)
    res = None
    res = loadResByResID(formID)

    if newCheckIn == "None" or not newCheckIn:
        res.check_in = None
    else:
        res.check_in = newCheckIn

    if newCheckOut == "None" or not newCheckOut:
        res.check_out = None
    else:
        res.check_out = newCheckOut

    db.session.add(res)
    db.session.commit()

    return redirect("/dashboard")


# Delete Functions
###################################
@app.route('/deleteRes', methods=['POST'])
def deleteRes():
    formID = request.form.get('formID')

    # fetch the reservation with reservation_id (formID)
    res = None
    res = loadResByResID(formID)

    db.session.delete(res)
    db.session.commit()

    return redirect("/dashboard")


# URL Routes
###################################


# home page for reservations API
@app.route('/')
def index():
    return render_template("index.html")


# this page shows the customers reservations
@app.route('/dashboard', methods=['GET'])
def dashboard(id=2, admin=""):
    # fetch ALL reservations that belong to userID
    usersRes = []
    usersRes = loadUsersRes(id)

    for i in usersRes:
        i.hotel_id = hotel_names[i.hotel_id]

    return render_template("dashboard.html", usersRes=usersRes)


# form for customer to update reservations
@app.route('/updateResForm', methods=['GET', 'POST'])
def updateResForm():

    formID = request.args.get('form')
    # fetch the reservation with reservation_id (formID)
    res = None
    res = loadResByResID(formID)
    return render_template("updateResForm.html", res=res, formID=formID)


# confirmation for customer to delete reservation
@app.route('/deleteResConfirmation', methods=['GET', 'POST'])
def deleteResConfirmation():

    formID = request.args.get('form')
    # fetch the reservation with reservation_id (formID)
    res = None
    res = loadResByResID(formID)
    return render_template("deleteResConfirmation.html", res=res, formID=formID)


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
