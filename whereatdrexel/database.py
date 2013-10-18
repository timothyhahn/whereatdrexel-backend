from whereatdrexel import db
from whereatdrexel.models import Location, BuildingLocation, CourseLocation

def init_db():
	db.create_all()

def clear_model(model):
    model.query.delete()
    
def clear_locations():
    clear_model(Location)

def clear_buildings():
    clear_model(BuildingLocation)

def clear_courses():
    clear_model(CourseLocation)

def clear_db():
	db.drop_all()

