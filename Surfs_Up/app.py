# Import the dependencies.
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

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
def Homepage():
    """List all available api routes."""
    return(
        f"Welcome to my API page on Hawaii's weather statistics!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Please enter a start date formatted yyyy-mm-dd following the route below.<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"Please enter a start date and end date seperated by the / and formatted yyyy-mm-dd following the route below.<br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )

# Create a route to the precipitation API data.
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    """Return a list of the precipitation data for the last 12 months of the data"""

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores.
    results = session.query(measurement.date, measurement.prcp).\
                  filter(measurement.date >= year_ago).all()
    
    # Close the session
    session.close()
    
    # Create a dictionary from the precipitation data and append to a list with corresponding date.
    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        date_prcp.append(prcp_dict)

    # Return the data in json format.    
    return jsonify(date_prcp)


# Create a route to the station API data.
@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB.
    session = Session(engine)

    """Return a list of the stations in the dataset"""

    # Perform a query to retrieve the data on all the stations.
    results = session.query(station.station).all()

    #Close the session.
    session.close()

    # Convert list of tuples into normal list.
    all_stations = list(np.ravel(results))

    # Return the data in json format.
    return jsonify(all_stations)


# Create a route to the temperature API data.
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB.
    session = Session(engine)
   
    """Return a list of the date and temperatures for the most active station in the data"""

    # Calculate the date one year from the last date in data set for the most active station.
    twelve_months = dt.date(2017, 8, 18) - dt.timedelta(days=366)

    # Query the last 12 months of temperature observation data for this station.
    results = session.query(measurement.date, measurement.tobs).\
                    filter(measurement.date >= twelve_months).\
                    filter(measurement.station =='USC00519281').all()
                    
    # Close the session.                              
    session.close()

    # Create a dictionary from the temperature data and append to a list for the most active station with its corresponding date.
    station_temp = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        station_temp.append(temp_dict)


    # Return the data in json format.
    return jsonify(station_temp)


# Create a route for the user inputted start date.
@app.route("/api/v1.0/start/<start>")
def start(start):

    # Create our session (link) from Python to the DB.
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date"""
    
    # Calculate the lowest, highest, and average temperature.
    mma = [func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]

    # Query temperature statistics of the data based on the user's inputted start date
    results = session.query(*mma).\
        filter(measurement.date >= start).all()
    
    # Close the session.                              
    session.close()

    # Create a dictionary from the temperature statistics.
    start_date_tobs_stats = []
    for min, max, avg in results:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Max"] = max
        stats_dict["Avg"] = avg
        start_date_tobs_stats.append(stats_dict)


        # Return the user inputted start date temperature statistics in json format
        return jsonify(start_date_tobs_stats)

    
# Create a route for the user inputted start date and end date.
@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the maximum temperature for a specified start and end date"""

    # Calculate the lowest, highest, and average temperature.
    mma = [func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]
    
    # Query temperature statistics of the data based on the user's inputted start date and end date.
    results = session.query(*mma).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    
    # Close the session.                              
    session.close()
        
    # Create a dictionary from the temperature statistics.
    start_end_date_tobs_stats = []
    for min, max, avg in results:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Max"] = max
        stats_dict["Avg"] = avg
        start_end_date_tobs_stats.append(stats_dict)


        # Return the user inputted start date and end date temperature statistics in json format.
        return jsonify(start_end_date_tobs_stats)


   
# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)
