from datetime import datetime

from sqlalchemy import and_

from Application import db
from Application.models import Researchers, LocationPoints


def update_researcher_timestamp(device_id, time):
    researcher = Researchers.query.filter(Researchers.phone_id == device_id).first()
    if researcher:
        researcher.last_updated = time
        commit_and_flush(researcher)
    else:
        insert_or_update_existing_researcher(device_id, 'None', 'None', time)


def insert_location_point_in_db(device_id, latitude, longitude, timestamp):
    lp = LocationPoints(phone_id=device_id, latitude=latitude, longitude=longitude, timestamp=timestamp)
    commit_and_flush(lp)


def insert_or_update_existing_researcher(device_id, name, surname, timestamp = None):
    researcher = Researchers.query.filter(Researchers.phone_id == device_id).first()
    if not researcher:
        researcher = Researchers(phone_id=device_id, name=name, surname=surname, last_updated=timestamp)
    else:
        researcher.name = name
        researcher.surname = surname
    commit_and_flush(researcher)


def commit_and_flush(r):
    try:
        db.session.add(r)
        db.session.commit()
        db.session.flush()
    except:
        db.session.rollback()
    finally:
        db.session.close()


def get_all_researchers_from_db():
    return Researchers.query.all()


def get_location_points_with_id(phone_id):
    return LocationPoints.query.filter(LocationPoints.phone_id == phone_id).all()


def get_entries_with_phone_id(device_id):
    locations = get_location_points_with_id(device_id)
    serialized_locations = [i.serialize for i in locations]
    return serialized_locations


def get_filtered_entries_from_db(device_id, start_unix_time, end_unix_time):
    start_time = datetime.now().fromtimestamp(float(start_unix_time))
    end_time = datetime.now().fromtimestamp(float(end_unix_time))
    query = and_(LocationPoints.timestamp >= start_time,
                 LocationPoints.timestamp < end_time,
                 LocationPoints.phone_id == device_id)
    locations = LocationPoints.query.filter(query).all()
    serialized_locations = [i.serialize for i in locations]
    return serialized_locations


def get_locations_for_phone_ids(selected_phone_ids):
    q = LocationPoints.phone_id.in_(selected_phone_ids)
    locations = LocationPoints.query.filter(q).all()
    serialized_locations = [i.serialize for i in locations]
    return serialized_locations
