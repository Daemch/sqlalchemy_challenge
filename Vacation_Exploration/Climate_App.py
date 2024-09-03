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

# reflect an existing database into a new model


# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# Sample data for demonstration purposes
data = {
    "precipitation": [
        {"date": "2023-09-01", "prcp": 0.1},
        {"date": "2023-09-02", "prcp": 0.2},
        # Add more data as needed
    ],
    "stations": [
        {"station": "STATION_1"},
        {"station": "STATION_2"},
        # Add more stations as needed
    ],
    "tobs": [
        {"date": "2023-09-01", "tobs": 70},
        {"date": "2023-09-02", "tobs": 72},
        # Add more temperature observations as needed
    ]
}

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert query results to a dictionary
    precipitation_dict = {item["date"]: item["prcp"] for item in data["precipitation"]}
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