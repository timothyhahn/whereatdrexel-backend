from flask.ext.script import Manager, Server

from whereatdrexel import app

import whereatdrexel.settings as settings

app.debug = settings.debug
app.config['SECRET_KEY'] = settings.secret_key

manager = Manager(app)
manager.add_command('runserver', Server())

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
