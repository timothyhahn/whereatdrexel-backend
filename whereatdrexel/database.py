from whereatdrexel import db

def init_db():
	db.create_all()

def clear_db():
	db.drop_all()


