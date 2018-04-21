#=======================================================================================================
# Step 4 - Climate App
#
#   Now that you have completed your initial analysis, design a Flask api
#   based on the queries that you have just developed.
#
#   * Use FLASK to create your routes.
#
#   Routes:
#
#           * '/api/v1.0/precipitation'
#                   * Query for the dates and precipitation observations from the last year.
#                   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#                   * Return the json representation of your dictionary.
#
#           * '/api/v1.0/stations'
#               * Return a json list of stations from the dataset.
#
#           * '/api/v1.0/tobs'
#               * Return a json list of Temperature Observations (tobs) for the previous year
#
#           * '/api/v1.0/<start>' and '/api/v1.0/<start>/<end>'
#               * Return a json list of the minimum temperature, the average temperature, and
#                   the max temperature for a given start or start-end range.
#               * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates
#                   greater than and equal to the start date.
#               * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX`
#                   for dates between the start and end date inclusive.
#=======================================================================================================

# import Pyhton dependencies
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt

# Python SQLAlchemy 'automap' and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#=====================================================
# Database Setup
#=====================================================
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#=====================================================
# Flask Setup
#=====================================================
app = Flask(__name__)

#=====================================================
# Flask Routes
#=====================================================


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Weather Data<br/><br/>"
        f"Pick from the available routes below:<br/><br/>"
        f"Precipiation from 2016-05-31 to 2017-06-01.<br/><br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"List of all Hawaii weather stations. <br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"The Temperature Observations (tobs) from 2016-08-23 to 2017-08-23.<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Input date (i.e., 2015-01-01) to get min_temp, avg_temp and max_temp temperature. <br/><br/>"
        f"/api/v1.0/calc_temps/<start><br/><br/>"
        f"Input date range (i.e., 2015-01-01/2015-01-10) o get min_temp, avg_temp and max_temp temperature for that date range.<br/><br/>"
        f"/api/v1.0/calc_temps/<start>/<end><br/><br/>"

    )
#=====================================================


@app.route("/api/v1.0/precipitation")
def precipitation():
    #    * Query all precipitation records from Hawaii Weather Stations from one last year.
    #    * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    #    * Return the json representation of your dictionary.
    prcp_data = session.query(Measurements.station, Measurements.date, Measurements.prcp).\
        filter(Measurements.date > '2016-05-31').\
        filter(Measurements.date < '2017-06-01').\
        order_by(Measurements.date.asc()).all()


# Create a list of dicts with `date` and `prcp` as the keys and values
    precip = []
    for result in prcp_df:
        row = {}
        row["station"] = result[0]
        row["date"] = result[1]
        row["prcp"] = result[2]
        precip.append(row)

    return jsonify(precip)


#=====================================================


@app.route("/api/v1.0/stations")
def stations():
    # Query all Hawaii Weather Stations
    station_res = session.query(Stations.station, Stations.station_name).group_by(Stations.station).all()

    list_station = list(np.ravel(station_res))
    return jsonify(list_station)


#=====================================================


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for prior year"""
#    * Query for the dates and temperature observations from the last year.
#    * Return the json representation of your dictionary.
    temperature = (session.query(Measurements.station, Measurements.date, Measurements.tobs).
                   filter(Measurements.station == 'USC00519281').
                   filter(Measurements.date > '2016-08-23').
                   order_by(Measurements.date)).all()

# Create a list of dicts with `date` and `tobs` as the keys and values
    list_temperature = []
    for res in temperature:
        row = {}
        row["station"] = res[0]
        row["date"] = res[1]
        row["tobs"] = res[2]
        list_temperature.append(row)

    return jsonify(list_temperature)


#=====================================================


@app.route("/api/v1.0/calc_temps/<start>")
def trip1_temp(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.timedelta(days=365)
    start = start_date - end_date
    end = dt.date(2017, 8, 23)

    res_temp = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    trip_temp = list(np.ravel(res_temp))
    return jsonify(trip_temp)


#=====================================================


@app.route("/api/v1.0/calc_temps/<start>/<end>")
def trip2_temp(start, end):

  # go back one year from start/end date and get Min/Avg/Max temp
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date - last_year
    end = end_date - last_year

    res_temp = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    trip_temp = list(np.ravel(res_temp))
    return jsonify(trip_temp)


#=====================================================


if __name__ == "__main__":
    app.run(debug=True)
