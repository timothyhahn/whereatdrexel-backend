## App Dependencies
from ..extensions import db, bcrypt

Column = db.Column
Integer = db.Integer
String = db.String
Model = db.Model
Float = db.Float
Text = db.Text
Enum = db.Enum


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

