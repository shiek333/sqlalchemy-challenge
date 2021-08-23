###########################
### Import Dependencies ###
###########################

from flask.json import jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask

######################
### Database Setup ###
######################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

###################
### Flask Setup ###
###################
app = Flask(__name__)

def Tup_to_Dict(tup, dict):
    for x, y in tup:
        dict.setdefault(x, []).append(y)
    return dict

### Home Page ###


@app.route("/")
def home():
    return (
        f"<title>Hawaii Weather API </title>"
        f"<h1> Welcome to the Hawaii Weather API! </h1>"
        f"<h3>List of Available Routes:</h3>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/start_date<br/>"
        f"Type start date in format ****-**-** (year-month-day) ie. 2016-09-02<br/><br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"Type start and end date in format ****-**-** (year-month-day) ie. 2016-09-02"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    presults = session.query(measurement.date,measurement.prcp).filter(measurement.date >= '2016-08-23').all()
    session.close()
    p_dict = {}
    Tup_to_Dict(presults,p_dict)
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    stresults = session.query(station.station, station.name).all()
    session.close()
    s_dict = {}
    Tup_to_Dict(stresults,s_dict)
    return jsonify(s_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_id = 'USC00519281'
    tresults = (session.query(
                             measurement.date,
                             measurement.tobs).
                    filter(measurement.station == most_active_id).
                    filter(measurement.date >= '2016-08-23').all())
    session.close()

    t_dict = {}
    Tup_to_Dict(tresults,t_dict)
    return jsonify(t_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    sresult = (session.query(func.min(measurement.tobs),
                            func.max(measurement.tobs),
                            func.avg(measurement.tobs)).
                    filter(measurement.date >= start).all())
    session.close()
    result_df = pd.DataFrame(sresult, columns = ["Temp Min", "Temp Max","Temp Average"])
    result_dict = result_df.to_dict(orient='list')
    return jsonify(result_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    seresult = (session.query(func.min(measurement.tobs),
                            func.max(measurement.tobs),
                            func.avg(measurement.tobs)).
                    order_by(measurement.date.desc()).
                    filter(measurement.date <= end).
                    filter(measurement.date >= start).all())
    session.close()
    result_df = pd.DataFrame(seresult, columns = ["Temp Min", "Temp Max","Temp Average"])
    result_dict = result_df.to_dict(orient='list')
    return jsonify(result_dict)


if __name__ == "__main__":
    app.run(debug=True)

# # Close Session
# session.close()
