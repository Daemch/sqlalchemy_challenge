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
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# engine = create_engine('sqlite:///your_database.db') 
# Session = sessionmaker(bind=engine)

# reflect the tables
Base.prepare(autoload_with=engine)

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
        f"/api/v1.0/Precipitation Analysis<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/Precipitation Analysis")
def precipitation():
    # Convert query results to a dictionary
    precipitation_dict = {item["date"]: item["prcp"] for item in data["precipitation"]}
    
    # @app.route('/precipitation', methods=['GET'])
# def get_precipitation():
    # Query the database
    #percip_values = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).\
       # filter(Measurement.date >= '2016-08-23').\
        # filter(Measurement.date <= '2017-08-23').all()

    # Convert the query results to a dictionary
    percip_dict = {date: prcp for date, prcp in percip_values}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations
    stations_list = [station["station"] for station in data["stations"]]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Return a JSON list of temperature observations for the previous year
    tobs_list = [tob["tobs"] for tob in data["tobs"]]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    # Sample temperature data for demonstration
    temperature_data = [
        {"date": "2023-09-01", "tmin": 65, "tavg": 70, "tmax": 75},
        {"date": "2023-09-02", "tmin": 66, "tavg": 71, "tmax": 76},
        # Add more data as needed
    ]

    # Filter data based on start and end dates
    filtered_data = [
        temp for temp in temperature_data
        if temp["date"] >= start and (end is None or temp["date"] <= end)
    ]

    # Calculate TMIN, TAVG, and TMAX
    tmin = min(temp["tmin"] for temp in filtered_data)
    tavg = np.mean([temp["tavg"] for temp in filtered_data])
    tmax = max(temp["tmax"] for temp in filtered_data)

    return jsonify({"TMIN": tmin, "TAVG": tavg, "TMAX": tmax})

if __name__ == "__main__":
    app.run(debug=True)