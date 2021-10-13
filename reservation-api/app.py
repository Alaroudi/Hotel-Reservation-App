from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
# pip install mysql-connector if that does not work pip install mysql-connector-python
import mysql.connector



app = Flask(__name__)

# replace password with your servers password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:        password        @localhost/hotel_reservation'


# connectes to the actual database for flask to make the pages
db = SQLAlchemy(app)

# connect the table allowing commands
cont = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd = "                 ",
	)
# variable to actual use commands
exec = cont.cursor()

## proof it connects comment out everything below to test except 54-55

# exec.execute("SHOW DATABASE")

# for i in exec:
# 	print(i)

# this page shows the customers reservations
@app.route('/reservastions', methods=['GET'])
def dashboard(id, admin):
    print()

# allows customer to delete reservation
@app.route('/reservations')
def delete_res(id, admin):
	print()

# edit reservation
@app.route('/reservastions')
def edit_res(id, admin): #send in jwt token id
	print()

# Add reservation
@app.route('/reservastions')
def add_res(id, admin):
    print()


if __name__ == "__main__":
    app.run(debug=True)




#################################################################################################
#################################################################################################
# I could not get the things below to connect how we were wanting them to due to mysql not allowing
#  remote connections to my local host.
#################################################################################################
#################################################################################################


# import pyodbc
# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from sqlalchemy import and_
# from sqlalchemy import Column, String
# from sqlalchemy.orm import Session, sessionmaker, mapper
# from sqlalchemy.ext.automap import automap_base


# # Conect to DB using pyodbc to get all data into list
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
#                     'SERVER=mysql+pymysql://root:Dakil9898@localhost/hotel_reservation;'
#                     'DATABASE=hotel_reservation;'
#                     'UID=root; PWD=Dakil9898')
# cursor = cnxn.cursor()



# # Connect to DB using SQLAlchem;
# # the engine can be passed to a Session object to work with the ORM

# engine = sa.create_engine('mysql+pymysql://root:Dakil9898@localhost/hotel_reservation').connect()

# # Using SQLAlchemy ORM
# #########################################
# # create the Session class using sessionmaker.
# # Alternatively, you can create a session using session = Session(bind=engine),
# # but you would have to create it everytime you want to communicate with db.
# # With sessionmaker (global scope), you can use session = Session() w/o arguments
# # to instantiate the session as many times as you need.
# # Remember: session = Session() everytime.

# Session = sessionmaker(bind=engine)
# Base = automap_base()


# class db_table(Base):
#     __tablename__ = '_reservations'
#     Key = Column(String, primary_key=True)


# Base.prepare(engine, reflect=True)
# session = Session()



