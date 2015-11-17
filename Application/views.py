__author__ = 'dimitris'

from Application import app,db
from flask import render_template,request,flash,jsonify,json
from datetime import datetime
from models import LocationPoints


@app.route('/', methods=['GET', 'POST'])
def root():
    result_list = get_distinct_phone_ids_from_db()
    return render_template('users.html', phone_ids=result_list)


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
    db.session.flush()


def get_distinct_phone_ids_from_db():
    res = db.session.query(LocationPoints).distinct(LocationPoints.phone_id).group_by(LocationPoints.phone_id)
    result_list = list()
    for val in res:
        result_list.append(val.phone_id)
    return result_list


def get_location_points_with_id(phone_id):
    loc_points = LocationPoints.query.filter(LocationPoints.phone_id==phone_id).all()
    return loc_points