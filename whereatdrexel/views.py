from whereatdrexel import app, login_manager, db
from models import Location, BuildingLocation, TruckLocation, FacultyLocation, AlertLocation, User, location_type
from flask import url_for, redirect, request, render_template, jsonify
from flask.ext.login import login_required, login_user, current_user
from sqlalchemy.sql import text

## For logins
@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

def get_all_locations(locationType):
	locations_list = list()
	locations = locationType.query.all()
	for location in locations:
		locations_list.append(location.data())
	locations_dict = dict()
	locations_dict['locations'] = locations_list
	return locations_dict

## API
@app.route('/api/locations')
def get_locations():
	return jsonify(get_all_locations(Location))

@app.route('/api/buildings')
def get_buildings():
	return jsonify(get_all_locations(BuildingLocation))

@app.route('/api/trucks')
def get_trucks():
	return jsonify(get_all_locations(TruckLocation))

@app.route('/api/faculty')
def get_faculty():
	return jsonify(get_all_locations(FacultyLocation))

@app.route('/api/alerts')
def get_alerts():
	return jsonify(get_all_locations(AlertLocation))

@app.route('/api/search/<term>', defaults={'type': 'all'})
@app.route('/api/search/<type>/<term>')
def search_locations(term, type):
	if type is not 'all' and type not in location_type._asdict().keys():
		return jsonify(dict())

	locations_list = list()
	locations_dict = dict()

	s = text('SELECT * FROM location WHERE similarity(name, :term) > 0.2 OR similarity(short_name, :term) > 0.4 OR similarity(description, :term) > 0.1;')
	results = db.engine.execute(s, term=term).fetchall()
	for result in results:
		location = Location.query.get(result.id)
		if type is 'all' or location.type == location_type._asdict()[type]:
			locations_list.append(location.data())
	locations_dict['locations'] = locations_list
	return jsonify(locations_dict)

## ADMIN
@app.route('/admin')
def admin_home():
	print location_type._asdict().values()
	return render_template('hello.html')
