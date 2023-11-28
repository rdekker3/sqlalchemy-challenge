# Import the dependencies.
import numpy as np

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
Base.prepare(autoload_with=engine)


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
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Date 12 months ago
    precip_data = session.query(measurement.date, func.avg(measurement.prcp)).group_by(measurement.date).all()
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.station, Station.name).all()
    return jsonify(station_data )
    
    @app.route("/api/v1.0/tobs")
def tobs():
    tobs_data = session.query(measurement.date, measurement.station, measurement.tobs).all()
    return jsonify(tobs_data)
    
if __name__ == '__main__':
    app.run(debug=True)
