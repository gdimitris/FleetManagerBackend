import os
from datetime import datetime

from flask import render_template, request, jsonify, send_from_directory, url_for

from Application import app, db
from Application.db_operations import update_researcher_timestamp, insert_location_point_in_db, \
    insert_or_update_existing_researcher, get_all_researchers_from_db, get_entries_with_phone_id, \
    get_filtered_entries_from_db, get_locations_for_phone_ids


@app.errorhandler(404)
def not_found(error):
    message = "Page not found: %s \n Reason: %s" % (request.path, error)
    app.logger.error(str(message))
    return render_template('error.html', message=message), 404


@app.errorhandler(500)
@app.errorhandler(502)
def internal_error(error):
    db.session.rollback()
    message = "Internal server error: %s" % error
    app.logger.error(message)
    return render_template('error.html', message=message), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    db.session.rollback()
    message = "Unhandled exception: %s" % e
    app.logger.error(message)
    return render_template('error.html', message), 500


@app.route('/content/current_version.apk', methods=['GET'])
def get_apk():
    return send_from_directory(os.path.join(app.root_path, 'static/resources'), 'app-working.apk',
                               mimetype='application/vnd.android.package-archive')


@app.route('/json/current_apk_version', methods=['GET'])
def get_version():
    text_file = open('static/resources/current_apk_version.txt')
    version = text_file.readline()
    apk_url = url_for('get_apk', _external=True)
    return jsonify(version=version, url=apk_url)


@app.route('/', methods=['GET', 'POST'])
def root():
    researchers = get_all_researchers_from_db()
    return render_template('users.html', researchers=researchers)


@app.route('/<device_id>', methods=['GET'])
def show_device_locations(device_id):
    return render_template('index.html', device_id=device_id)


@app.route('/<device_id>', methods=['POST'])
def add_entry(device_id):
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    timestamp = request.args.get('time')
    time = datetime.now().fromtimestamp(float(timestamp))
    insert_location_point_in_db(device_id, lat, lon, time)
    update_researcher_timestamp(device_id, time)
    return render_template("empty.html"), 200


@app.route('/json/<device_id>', methods=['GET'])
def get_entries(device_id):
    entries = get_entries_with_phone_id(device_id)
    return jsonify(result=entries)


@app.route('/json/<device_id>/filtered', methods=['GET'])
def get_filtered_entries(device_id):
    start_unix_time = request.args.get('start')
    end_unix_time = request.args.get('end')
    entries = get_filtered_entries_from_db(device_id, start_unix_time, end_unix_time)
    return jsonify(result=entries)


@app.route('/<device_id>/register_full_name', methods=['GET', 'POST'])
def register_researcher(device_id):
    name = request.args.get('name')
    surname = request.args.get('surname')
    insert_or_update_existing_researcher(device_id, name, surname)
    return render_template("empty.html"), 200


@app.route('/multiselect_users', methods=['POST'])
def multiselect_users():
    selected = request.form.getlist('check')
    print selected
    res = get_locations_for_phone_ids(selected)
    return render_template("multiple_users.html", res=res)


if __name__ == '__main__':
    app.run()
