__author__ = 'dimitris'

from Application import app,db
from flask import render_template,request,flash,jsonify,json
from datetime import datetime
from models import LocationPoints


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

@app.route('/<device_id>', methods=['GET'])
def show_device_locations(device_id):
    locations = get_location_points_with_id(device_id)
    ser_locations = [l.serialize for l in locations]
    return render_template('index.html', location_points=json.dumps(ser_locations))

@app.route('/<device_id>', methods=['POST'])
def add_entry(device_id):
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    timestamp = request.args.get('time')
    time = datetime.now().fromtimestamp(float(timestamp))
    insert_location_point_in_db(device_id, lat, lon, time)
    return render_template("empty.html"), 200


def insert_location_point_in_db(device_id, latitude, longitude, timestamp):
    lp = LocationPoints(phone_id=device_id, latitude=latitude, longitude=longitude, timestamp=timestamp)
    db.session.add(lp)
    db.session.commit()


def get_location_points_with_id(phone_id):
    loc_points = LocationPoints.query.filter(LocationPoints.phone_id==phone_id).all()
    return loc_points