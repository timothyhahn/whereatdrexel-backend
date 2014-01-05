from flask.ext.script import Manager, Server

from whereatdrexel import create_app

app = create_app()
manager = Manager(app)

manager.add_command('runserver', Server())

## Helpers

def clear_model(model):
    model.query.delete()

## Commands

@manager.command
def run():
    app.run()

@manager.command
def init_db():
    "Sets up the DB"
    print "Setting up DB"
    from whereatdrexel.database import init_db
    init_db()

@manager.command
def clear_db():
    "Clears the DB"
    print "Clearing DB"
    from whereatdrexel.database import clear_db
    clear_db()

@manager.command
def load_buildings():
    "Loads locations of buildings"
    from whereatdrexel.helpers import load_buildings
    load_buildings()

@manager.command
def clear_buildings():
    "Clear Buildings"
    from whereatdrexel.database import clear_buildings
    clear_buildings

@manager.command
def load_courses():
    "Loads courses"
    from whereatdrexel.helpers import load_courses
    load_courses()

def clear_courses():
    "Clear Courses"
    from whereatdrexel.database import clear_courses
    clear_courses()

@manager.command
def download_courses():
    "Downloads courses"
    from whereatdrexel.helpers import download_courses
    download_courses()

@manager.command
def migrate(message):
	"Migrate, needs a commit message"
	if not message:
		print "Usage: python manage.py migrate <commit-message>"
		return 1
	print "Migrating"
	import subprocess
	result = subprocess.call(['alembic','revision','-m', message])
	if result != 0:
		return result
	result = subprocess.call(['alembic','upgrade','head'])
	return result


if __name__ == "__main__":
    manager.run()

