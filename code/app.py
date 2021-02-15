#Dependencies
from flask import Flask, jsonify, render_template, request
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

######### MOVE #########
# Create our session (link) from Python to the DB
session = Session(engine)
#########################

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>" #From: https://github.com/goldenb85/sqlalchemy-challenge/blob/master/app.py
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]" #From: https://github.com/goldenb85/sqlalchemy-challenge/blob/master/app.py
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
    all_precip = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_precip.append(prcp_dict)
    session.close()
     
    return jsonify(all_precip)

   


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.name).\
        order_by(Station.station).all()
    all_stations = list(np.ravel(results))
    session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        all_tobs.append(tobs_dict)
    session.close()

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    session = Session(engine)

    results = session.query(
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
        

    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["TMIN"] = min
        start_date_tobs_dict["TAVG"] = avg
        start_date_tobs_dict["TMAX"] = max
        start_date_tobs.append(start_date_tobs_dict)

    session.close()

    return jsonify(start_date_tobs)


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    session = Session(engine)

    results = session.query(
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <=  end_date).all()
        

    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["TMIN"] = min
        start_end_tobs_dict["TAVG"] = avg
        start_end_tobs_dict["TMAX"] = max
        start_end_tobs.append(start_end_tobs_dict)

    session.close()

    return jsonify(start_end_tobs)

   
    


if __name__ == '__main__':
    app.run(debug=True)
