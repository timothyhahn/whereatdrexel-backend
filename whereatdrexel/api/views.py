## Application dependencies
from .models import Location, BuildingLocation, CourseLocation, TruckLocation, FacultyLocation, AlertLocation, location_type
from ..views import crossdomain
from ..extensions import db

## Flask Dependencies
from flask import Blueprint, jsonify

## External Dependencies
from sqlalchemy.sql import text
import re

api = Blueprint('api', __name__, url_prefix='/api')

## Helper functions

def get_all_locations(locationType):
    locations_list = list()
    locations = locationType.query.all()
    for location in locations:
        locations_list.append(location.data())
    locations_dict = dict()
    locations_dict['locations'] = locations_list
    return locations_dict

## API
@api.route('/locations')
@crossdomain(origin='*')
def get_locations():
    return jsonify(get_all_locations(Location))

@api.route('/buildings')
@api.route('/search/') ## For default empty search
@crossdomain(origin='*')
def get_buildings():
    return jsonify(get_all_locations(BuildingLocation))

@api.route('/courses')
def get_courses():
    return jsonify(get_all_locations(CourseLocation))

@api.route('/trucks')
def get_trucks():
    return jsonify(get_all_locations(TruckLocation))

@api.route('/faculty')
def get_faculty():
    return jsonify(get_all_locations(FacultyLocation))

@api.route('/alerts')
def get_alerts():
    return jsonify(get_all_locations(AlertLocation))

@api.route('/search/<term>', defaults={'type': 'all'})
@api.route('/search/<type>/<term>')
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
                location['exact_match'] = True
                locations_list.append(location) 
            elif re.search(r'\b' + re.escape(term) + r'\b', location['name'].lower()):
                location['exact_match'] = True
                locations_list.append(location)
        
    ## Add the rest of the answers
    for location in temp_list:
        if location not in locations_list:
            location['exact_match'] = False
            locations_list.append(location)

    locations_dict['locations'] = locations_list[:20]
    return jsonify(locations_dict)
