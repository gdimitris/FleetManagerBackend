__author__ = 'dimitris'

from Application import app,db
from flask import render_template,request,flash
from datetime import datetime
from models import LocationPoints


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/<device_id>', methods=['GET'])
def add_entry(device_id):
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    timestamp = request.args.get('time')
    time = datetime.now().fromtimestamp(float(timestamp))
    insert_location_point_in_db(device_id, lat, lon, time);
    return render_template('test.html', lat=lat, lon=lon, timestamp=time)


def insert_location_point_in_db(device_id, latitude, longitude, timestamp):
    lp = LocationPoints(phone_id=device_id, latitude=latitude, longitude=longitude, timestamp=timestamp)
    db.session.add(lp)
    db.session.commit()
