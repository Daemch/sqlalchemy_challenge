# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/Precipitation_Analysis<br/>"
        f"/api/v1.0/Stations_List<br/>"
        f"/api/v1.0/Most_Active_Station_TOBS<br/>"
        f"/api/v1.0/Start_Date<br/>"
        f"/api/v1.0/End_Date<br/>"
    )

@app.route("/api/v1.0/Precipitation_Analysis", methods=['GET'])
def get_Precipitation_Analysis():
    # Query the database
    percip_values = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()

    # Convert the query results to a dictionary
    percip_dict = {date: prcp for date, prcp in percip_values}
    return jsonify(percip_dict)

@app.route("/api/v1.0/Stations_List", methods=['GET'])
def get_Stations_List():
    # Query the database
    stations = session.query(Measurement.station, func.count(Measurement.station).label('count')).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # Convert the query results to a dictionary
    stations_dict = {station: count for station, count in stations}
    return jsonify(stations_dict)

@app.route("/api/v1.0/Most_Active_Station_TOBS", methods=['GET'])
def get_Most_Active_Station_TOBS():
    # Query the database to find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station).\
        label('count')).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]

    # Query the temperature observations for the most active station
    tobs_values = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == most_active_station).all()

    # Convert the query results to a dictionary
    tobs_dict = {date: tobs for date, tobs in tobs_values}
    return jsonify(tobs_dict)

@app.route("/api/v1.0/Start_Date")
@app.route("/api/v1.0/End_Date")
def temperature_range(start, end=None):
    # Convert start and end to date objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date() if end else dt.date.today()

    # Query the database for the date range
    if end:
        results = Measurement.query.filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    else:
        results = Measurement.query.filter(Measurement.date >= start_date).all()

    # Convert results to a list of dictionaries
    temperature_data = [
        {"date": result.date, "tmin": result.tmin, "tavg": result.tavg, "tmax": result.tmax}
        for result in results
    ]

    # Calculate TMIN, TAVG, and TMAX
    tmin = min(temp["tmin"] for temp in temperature_data)
    tavg = np.mean([temp["tavg"] for temp in temperature_data])
    tmax = max(temp["tmax"] for temp in temperature_data)

    return jsonify({"TMIN": tmin, "TAVG": tavg, "TMAX": tmax})

if __name__ == "__main__":
    app.run(debug=True)
    
    session.close()