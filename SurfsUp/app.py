# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<date>"
    )

@app.route("/api/v1.0/precipitation") #query precipitation records from the stations
def precipitation():
    precip_data = session.query(measurement.date,func.avg(measurement.prcp)).group_by(measurement.date).all()
    return jsonify(precip_data)#display the data populated within the JSON file

@app.route("/api/v1.0/stations") #query station name and info
def stations():
    station_data = session.query(station.station, station.name).all()
    return jsonify(station_data)#display the data populated within the JSON file
    

@app.route("/api/v1.0/tobs") #query temperature records from the stations
def tobs():
    tobs_data = session.query(measurement.date, measurement.station, measurement.tobs).all()
    return jsonify(tobs_data)#display the data populated within the JSON file
   
 @app.route("/api/v1.0/<date>") #find the minimum, maximum, and average percipitation from the days data
def daysmeasured(date):
    days_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).all()
    return jsonify(days_data)
    
if __name__ == "__main__":
    app.run(debug=True)
