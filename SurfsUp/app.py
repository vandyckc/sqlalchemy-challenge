
# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

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
# Welcome route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date/<start><br/>"
        f"/api/v1.0/start-date/<start>/end-date/<end>"
    )


# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session_1 = Session(engine)

    """Return a list of precipitation measurements for one year"""
    # Query precipitaiton measurements
    results_1 = session_1.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(Measurement.date).all()
    session_1.close() 

    query_1_dict = []

    for date,  precip in results_1:
        precip_dict = {}
        precip_dict["Date"]=date
        precip_dict["Precipitation"]=precip
        query_1_dict.append(precip_dict)

        # return jsonify(all_names)
    return jsonify(query_1_dict)


# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session_2 = Session(engine)

    """Return a list of all precipitation measurement stations"""
    # Query stations
    results_2 = session_2.query(Station.station, Station.name).all()
    session_2.close() 

# Convert list of tuples into a normal list
    stations = list(np.ravel(results_2))
    return jsonify(stations)

# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session_3 = Session(engine)

    """Return a list of tobs"""
    # Query tobs
    results_3 = session_3.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.station=="USC00519281").all()
    session_3.close() 

    query_3_dict = []

    for date, tobs in results_3:
        tobs_dict = {}
        tobs_dict["Date"]=date
        tobs_dict["Temperature Observed"]=tobs
        query_3_dict.append(tobs_dict)

        # return jsonify(all_names)
    return jsonify(query_3_dict)

# Start, start and end routes
@app.route("/api/v1.0/start-date/<start>")
@app.route("/api/v1.0/start-date/<start>/end-date/<end>")
def start_end(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    print("start-date/yyyy-mm-dd/end-date/yyyy-mm-dd")
    print (start)
    print (end)
    if not end:
        # Query tobs values for dates greater than start when no end date is inputted
        results = session.query(*sel).filter(Measurement.date >= start).all()
        # Convert results into a normal list
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)

    # Calculate tobs values with user inputted start and stop dates
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Convert results into a normal list
    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)