# Import dependencies
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save references to the tables
Measurement = Base.classes.measurement
Station=Base.classes.station

#Flask Setup
app=Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    """Return a list of the last year of Precipitation Data"""
    results=session.query(Measurement.date, Measurement.prcp).\
                    filter(measurement.date >= "2016-08-23").\
                    filter(measurement.date <= "2017-08-23").all()
                    
     session.close()
     
    #Convert results to dictionary
    prcp = []
    for date, prcp in results:
        prcp_dict ={}
        prcrp_dict["date"] = date
        prcp_dict["prcp"] = prcp
    
        prcp.append(prcp_dict)
    
    return jsonify(prcp)
    
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    """Return a list of all stations"""
    results=session.query(Station.station).\
                    order_by(Station.station).all()
                    
session.close()

all_stations=list(np.ravel(results))
return jsonify(all_stations)


#Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    
        """Return a list of tobs in the last year"""
        results=session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= "2016-08-23").\
                        filter(Measurement.date <= "2017-08-23").\
                        filter(Measurement.station=="USC00519281").all()
                        
        session.close()
        
#Convert results to a JSON list
    date_tobs=[]
    for date, tobs in results:
        tobs_dict= {}
        all_tobs["date"]= date
        all_tobs["tobs"]= tobs
        
        all_tobs.append(all_tobs)
        
return jsonify(all_tobs)


#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for tmin, tavg, tmax in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = tmin
        start_date_tobs_dict["avg_temp"] = tavg
        start_date_tobs_dict["max_temp"] = tmax
        start_date_tobs.append(start_date_tobs_dict)
    return jsonify(start_date_tobs)

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
 @app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for tmin, tavg, tmax in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = tmin
        start_end_tobs_dict["avg_temp"] = tavg
        start_end_tobs_dict["max_temp"] = tmax
        start_end_tobs.append(start_end_tobs_dict)
    

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)
        
