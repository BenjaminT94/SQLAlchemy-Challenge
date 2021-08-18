#Dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
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
    station_data = session.query(Stations.station).all()
    station_all = list(np.ravel(results))
    return jsonify(station_all)
    
@app.route("/api/v1.0/tobs")
#Return a JSON list of Temperature Observations (tobs) for the previous year.
# Keeping in mind to filter for within the the year of specified date
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
def starting_calc(start):
     start = datetime.strptime('2016-08-23', '%Y-%m-%d').date()
     start_data = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).\
               filter(Measurement.date >= start)
     # Creating a list of dictionaries to append values
     start_tobs_list = []   
     for i in start_results:
       dict = {}
       dict["TMIN"] = float(tobs[1])                     
       dict["TMAX"] = float(tobs[0])
       dict["TAVG"] = float(tobs[2])
       start_tobs_list.append(dict)
     return jsonify(start_tobs_list)                    
                            
@app.route("/api/v1.0/<start>/<end>")
# start and end date in the "desired" Python format
def ending_calc(start,end):
     start = datetime.strptime('2016-08-23', '%Y-%m-%d').date()                      
     end = datetime.strptime('2017-08-23', '%Y-%m-%d').date()
     end_data = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).\
               filter(Measurement.date >= start)                     
     start_end_tobs_list = []
     for i in start_end_tobs_list:
       dict = {}
       dict["TMIN"] = float(tobs[1])                     
       dict["TMAX"] = float(tobs[0])
       dict["TAVG"] = float(tobs[2])
       start_end_tobs_list.append(dict)
     return jsonify(start__end_tobs_list)   
                                 
if __name__ == '__main__':
     app.run(debug=True)                            


                          
