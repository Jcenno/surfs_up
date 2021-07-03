#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
#   return 'Hello world'


# dependencies imported
import datetime as dt
import numpy as np
import pandas as pd


# dependencies we need for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

#  reflect the database into our classes
Base = automap_base()
# reflect the database
Base.prepare(engine, reflect=True)

# create a variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app."
app = Flask(__name__)

# efine the welcome route
@app.route("/")

# create a function welcome() with a return statement. 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


# create the route
@app.route("/api/v1.0/precipitation")

# write a query to get the date and precipitation for the previous year.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# defining the route and route name. 
@app.route("/api/v1.0/stations")

# create a new function called stations()
def stations():
    # create a query that will allow us to get all of the stations in our database.
    results = session.query(Station.station).all()
    # unraveling our results into a one-dimensional array.
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#  temperature observations, defining the route
@app.route("/api/v1.0/tobs")
# create a function called temp_monthly()
def temp_monthly():
    # calculate the date one year ago from the last date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list. Then jsonify the list and return our results
    temps = list(np.ravel(results))
    # jsonify our temps list, and then return it.
    return jsonify(temps=temps)
    

