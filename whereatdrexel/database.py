from whereatdrexel import create_app
from .extensions import db
from .api.models import Location, BuildingLocation, CourseLocation

app = create_app()

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

