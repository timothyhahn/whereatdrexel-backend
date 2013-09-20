import json
from models import BuildingLocation
from whereatdrexel import db

def load_buildings():
    json_data = open('building-locations.json').read()
    data = json.loads(json_data)
    locations_list = data['locations']
    for location in locations_list:
        bl = BuildingLocation(name=location['name'],description=location['description'],latitude=location['latitude'],longitude=location['longitude'],short_name=location['short_name'])
        db.session.add(bl)
    db.session.commit()

