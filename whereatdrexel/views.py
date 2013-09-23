from whereatdrexel import app, login_manager, db
from models import Location, BuildingLocation, CourseLocation, TruckLocation, FacultyLocation, AlertLocation, User, location_type
from flask import url_for, redirect, request, render_template, jsonify, json, g, Flask
from flask.ext.login import login_required, login_user, current_user
from sqlalchemy.sql import text
from flask_wtf import Form
from wtforms import TextField, FloatField, BooleanField, IntegerField
from wtforms.validators import Required


import re

## For logins
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

## Helper for crossdomain testing
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

## Helper for API

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
@crossdomain(origin='*')
def get_locations():
    return jsonify(get_all_locations(Location))

@app.route('/api/buildings')
@app.route('/api/search/') ## For default empty search
@crossdomain(origin='*')
def get_buildings():
    return jsonify(get_all_locations(BuildingLocation))

@app.route('/api/courses')
def get_courses():
    return jsonify(get_all_locations(CourseLocation))

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
@crossdomain(origin='*')
def search_locations(term, type):
    if type is not 'all' and type not in location_type._asdict().keys():
        return jsonify(dict())

    locations_list = list()
    locations_dict = dict()

    s = text('SELECT * FROM location WHERE similarity(name, :term) > 0.2 OR similarity(short_name, :term) > 0.1 OR similarity(description, :term) > 0.1;')
    results = db.engine.execute(s, term=term).fetchall()
    term = term.lower()

    ## Grab all answers
    temp_list = list()
    for result in results:
        location = Location.query.get(result.id)
        if type is 'all' or location.type == location_type._asdict()[type]:
            temp_list.append(location.data())

    ## Find the best answers
    for location in temp_list:
        if location['short_name']:
            if re.search(r'\b' + re.escape(term) + r'\b', location['short_name'].lower()):
                locations_list.append(location) 
            elif re.search(r'\b' + re.escape(term) + r'\b', location['name'].lower()):
                locations_list.append(location)
        
    ## Add the rest of the answers
    for location in temp_list:
        if location not in locations_list:
            locations_list.append(location)

    locations_dict['locations'] = locations_list[:20]
    return jsonify(locations_dict)

## ADMIN
class LocationForm(Form) :
    id = IntegerField('id')
    name = TextField('name')
    longitude = FloatField('longitude')
    latitude = FloatField('latitude')
    type = TextField('type')
    delete = BooleanField('delete', default='n')

@app.route('/admin', methods = ['GET','POST'])
def admin_home():
    locform = LocationForm()
    if locform.validate_on_submit() :
        ids = request.form.getlist('id')
        name = request.form.getlist('name')
        longitude = request.form.getlist('longitude')
        latitude = request.form.getlist('latitude')
        type = request.form.getlist('types')        
        for (i, id) in enumerate(ids) :
            if id.isdigit() :
                loc = Location.query.get(id)
                loc.longitude = longitude[i]
                loc.latitude = latitude[i]
                loc.name = name[i]
                loc.type = type[i].lower()
                db.session.commit()
            else :
                if longitude[i] and latitude[i] and name[i] :
                    loc = Location(float(longitude[i]), float(latitude[i]), name[i], 'N/A', 'N/A')
                    loc.type = type[i].lower()
                    db.session.add(loc)
                    db.session.commit()
    locations = Location.query.all()
    type_list = list()
    
    for type in location_type._asdict().values():
        type_list.append(type.capitalize())
    return render_template('hello.html', locations=locations, location_types=type_list, form=locform)

@app.route('/admin/delete/<id>')
def delete(id) :
    print 'here'
    l = Location.query.get(id)
    db.session.delete(l)
    db.session.commit()
    return redirect(url_for('/admin'))
