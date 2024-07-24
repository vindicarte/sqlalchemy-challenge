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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
## 1. / 
@app.route("/")
def welcome():
    return(
        f"Welcome to the Climate Info Site! <br/>"
        f"Available Routines:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        f"Note: Use Start/End Date in the format YYYY-MM-DD."
    )

## 2. /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    precep = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= '2016-08-23').\
    order_by(measurement.date).all()

    all_precep = []
    for date, prcp in precep:
        precep_dict = {}
        precep_dict["date"] = date
        precep_dict["prcp"] = prcp
        all_precep.append(precep_dict)

    return jsonify(all_precep)

## 3. /api.v.10/stations
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    stations = list(np.ravel(stations))
    
    return jsonify(stations)



## 4. /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(measurement.date, measurement.tobs).all()
    tobs = list(np.ravel(tobs))

    return jsonify(tobs)


## 5. /api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(
        measurement.date,
        func.min(measurement.tobs), 
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    result = list(np.ravel(result))

    return jsonify(result)
    

## 5b. /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    result = session.query(
        measurement.date,
        func.min(measurement.tobs), 
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).filter(measurement.date >=start).filter(measurement.date <= end).all()
    result = list(np.ravel(result))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)