from whereatdrexel import app, login_manager, db
from flask.ext.login import login_required, login_user, current_user
from flask import url_for, redirect, request, render_template, jsonify
from models import Location, User, location_type

## For logins
@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

## API
@app.route('/api/locations')
def get_locations():
	locations_list = list()
	locations = Location.query.all()
	for location in locations:
		locations_list.append(location.name)
	
	locations_dict = dict()
	locations_dict['locations'] = locations_list
	return jsonify(locations_dict)


## ADMIN
@app.route('/admin')
def admin_home():
	print location_type._asdict().values()
	return render_template('hello.html')
