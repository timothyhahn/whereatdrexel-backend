## Admin Dependencies
from .models import User
from .forms import LoginForm, LocationForm

## App Dependencies
from ..extensions import login_manager, db
from ..api.models import Location, location_type

## Flask Dependencies
from flask import Blueprint, render_template, redirect, request, url_for
from flask.ext.login import login_required, current_user, login_user, logout_user

admin = Blueprint('admin', __name__, url_prefix='/admin')

## For logins
login_manager.login_view = "admin.login"

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


## ADMIN
@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(url_for('admin.admin_home'))
    return render_template('login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin.route('/', methods = ['GET','POST'])
@login_required
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
    return render_template('admin.html', locations=locations, location_types=type_list, form=locform, username=current_user.username)

@admin.route('/admin/delete/<id>')
@login_required
def delete(id) :
    print 'here'
    l = Location.query.get(id)
    db.session.delete(l)
    db.session.commit()
    return redirect(url_for('admin'))
