## Admin Dependencies
from .models import User
## Flask Dependencies
from flask_wtf import Form
from wtforms import TextField, FloatField, BooleanField, IntegerField, PasswordField, validators

class LocationForm(Form):
    id = IntegerField('id')
    name = TextField('name')
    longitude = FloatField('longitude')
    latitude = FloatField('latitude')
    type = TextField('type')
    delete = BooleanField('delete', default='n')

class LoginForm(Form):
    username = TextField('username', [validators.Required()])
    password = PasswordField('password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.username==self.username.data).first()
        if user is None:
            return False

        if not user.is_valid(self.password.data):
            return False

        self.user = user
        return True

