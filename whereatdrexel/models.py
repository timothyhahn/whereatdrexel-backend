from whereatdrexel import db, bcrypt, app
from collections import namedtuple
import json

Column = db.Column
Integer = db.Integer
String = db.String
Model = db.Model
Float = db.Float
Text = db.Text
Enum = db.Enum

def create_named_tuple(*values):
    return namedtuple('NamedTuple', values)(*values)

location_type = create_named_tuple('building', 'course', 'faculty', 'truck', 'alert')

class Location(Model):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    name = Column(String(120), nullable=False)
    short_name = Column(String(20))
    description = Column(Text)
    type = Column(Enum(*location_type._asdict().values(), name='location_type'), nullable=False)
    __mapper_args__ ={'polymorphic_on':type}
    
    def __init__(self, longitude=None, latitude=None, name=None, short_name=None, description=None):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.short_name = short_name
        self.description = description

    def __repr__(self):
        return '<Location %r at %f x %f is of type %r>' % (self.name, self.longitude, self.latitude, self.type)
    
    def data(self):
        location_dict = dict()
        location_dict['id'] = self.id
        location_dict['name'] = self.name
        location_dict['short_name'] = self.short_name
        location_dict['description'] = self.description
        location_dict['longitude'] = self.longitude
        location_dict['latitude'] = self.latitude
        location_dict['type'] = self.type
        return location_dict

class CourseLocation(Location):
    __mapper_args__ = {'polymorphic_identity': location_type.course}

class BuildingLocation(Location):
    __mapper_args__ = {'polymorphic_identity': location_type.building}
    
class FacultyLocation(Location):
    __mapper_args__ = {'polymorphic_identity': location_type.faculty}

class TruckLocation(Location):
    __mapper_args__ = {'polymorphic_identity': location_type.truck}

class AlertLocation(Location):
    __mapper_args__ = {'polymorphic_identity': location_type.alert}

class User(Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    password = Column(String(60), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = bcrypt.generate_password_hash(password) 

    def __repr__(self):
        return '<User %r>' % (self.username)
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    
    def is_valid(self, password=None):
        return bcrypt.check_password_hash(self.password, password)

