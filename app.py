#Dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql.selectable import Lateral

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")  
    
@app.route("/api/v1.0/precipitation")    
def precipitation():
    last_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).order_by(Measurement.date).all()

#Creating a dictionary with date and precipitation
    precipitation_data = []
    for i in precipitation:
        data = {}
        data['date'] = precipitation[0]
        data['prcp'] = precipitation[1]
        precipitation_data.append(data)
# Returning date and precipitation rate as json
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def Station():
    session = Session(engine)
    station_data= [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    result= session.query(*station_data).all()
    session.close()

    stations=[]
    for i in result:
        station_dict={}
        station_dict["Name"] = name
        station_dict["Station"]= station
        station_dict["Lat"] = Lat
        station_dict["Lon"] = lon 
        station_dict["Elevation"] = elevation
        stations.append(station_dict)
    return jsonify(stations)
    
@app.route("/api/v1.0/tobs")
#Return a JSON list of Temperature Observations (tobs) for the previous year.
# Keeping in mind to filter for within the the year of specified date
def tobs():
    tobs_data = session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    # Creating a list of dictionaries to append values
    list = []
    for i in tobs_results:
       dict = {}
       dict["station"] = tobs[0]
       dict["tobs"] = float(tobs[1])
       list.append(dict)                             
    return jsonify(list)

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
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    start_end_obs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_obs.append(start_end_tobs_dict)   
                                 
if __name__ == '__main__':
     app.run(debug=True)                            


                          
