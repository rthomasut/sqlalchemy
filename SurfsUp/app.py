# Import other necessary libraries here
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an instance of Flask
app = Flask(__name__)

# Define your routes
@app.route("/")
def home():
    return (
        "Welcome to the Hawaii Weather API!<br>"
        "Available Routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/start_date<br>"
        "/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a new session for this route
    session = Session(engine)
    # Query precipitation and date data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    # Convert list of tuples into dictionary
    all_precepitation=[]
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precepitation.append(precipitation_dict)

    return jsonify(all_precepitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()
    all_station=[]
    for id,station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict['Id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_station.append(station_dict)
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a new session for this route
    session = Session(engine)
    
    # Calculate the most recent date
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    
    # Calculate the date 12 months ago from the most recent date
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Query temperature observation data for the last 12 months for the most active station
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Create a list of dictionaries containing date and temperature data
    tobs_list = [{"date": date, "temperature": temp} for date, temp in temperature_data]

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    # Create a new session for this route
    session = Session(engine)
    # Query precipitation and date data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close() 
    # Convert the start date to a datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    
    # Query temperature statistics for dates greater than or equal to the start date
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).first()
    
    # Create a dictionary with the temperature statistics
    temp_stats = {
        "TMIN": temperature_stats[0],
        "TAVG": temperature_stats[1],
        "TMAX": temperature_stats[2]
    }
    
    # Return JSON representation of the temperature statistics
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_range(start, end):
    # Create a new session for this route
    session = Session(engine)
    # Query precipitation and date data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close() 
    # Convert the start and end dates to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    
    # Query temperature statistics for the date range
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.avg(Measurement.tobs),
                                      func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).first()
    
    # Create a dictionary with the temperature statistics
    temp_stats = {
        "TMIN": temperature_stats[0],
        "TAVG": temperature_stats[1],
        "TMAX": temperature_stats[2]
    }
    
    # Return JSON representation of the temperature statistics
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)