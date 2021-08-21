#Dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Creating engine and reflection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

#Set up Flask
app = Flask(__name__)

#Making routes
@app.route("/")
def homepage():
    """Listing APIs as a directory"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>")  
    
@app.route("/api/v1.0/precipitation")    
def precipitation():
    session=Session(engine)
    data = [Measurement.date,Measurement.prcp]
    result= session.query(*data).all()
    session.close()
    precipitation =[]
    # From here on out for the remaining routes, I will create dictionaries to append to my list to display query results
    for date, precip in result:
        precip_dict={}
        precip_dict["Date"]=date
        precip_dict["Precipitation"]=precip
        precipitation.append(precip_dict)
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def Stations():
    session = Session(engine)
    station_data= [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    result= session.query(*station_data).all()
    session.close()

    Stations=[]
    for station,name,Lat,lon,elevation in result:
        station_dict={}
        station_dict["Station"]= station
        station_dict["Name"] = name
        station_dict["Lat"] = Lat
        station_dict["Lon"] = lon 
        station_dict["Elevation"] = elevation
        Stations.append(station_dict)
    return jsonify(Stations)
    
@app.route("/api/v1.0/tobs")
#Return a JSON list of Temperature Observations (tobs) for the previous year.
# Keeping in mind to filter for within the the year of specified date
def tobs():
    session=Session(engine)
    latestdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestformatted = dt.datetime.strptime(latestdate,'%Y-%m-%d')
    # Going back one year from the latest date
    date = dt.date(latestformatted.year-1,latestformatted.month,latestformatted.day)
    data=[Measurement.date,Measurement.tobs]
    result=session.query(*data).filter(Measurement.date >= date).all()
    session.close()
    alltobs = []
    for date, tobs in result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature Observations"] = tobs
        alltobs.append(tobs_dict)
    return jsonify(alltobs)
 

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.                                                                    
@app.route("/api/v1.0/<start>")
def temp_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    observations = []
    for min,avg,max in results:
        start_tobs_dict = {}
        start_tobs_dict["Min"] = min
        start_tobs_dict["Average"] = avg
        start_tobs_dict["Max"] = max
        observations.append(start_tobs_dict)

    return jsonify(observations)                 
                            
@app.route("/api/v1.0/<start>/<end>")
# Same as above but include start and end date
def temp_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    start_end_obs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["Min"] = min
        start_end_tobs_dict["Average"] = avg
        start_end_tobs_dict["Max"] = max
        start_end_obs.append(start_end_tobs_dict) 
    return jsonify(start_end_obs)
                                 
if __name__ == '__main__':
     app.run(debug=True)                            


                          
