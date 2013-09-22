# Where at Drexel? - Backend

> Python backend for "Where At Drexel?"

## Instructions

* Requirements: python, python-dev, pip, postgresql, postgresql-dev

* Install all the project requirements with pip:

```
pip install -r requirements.txt
```

* Create the database and fill in data required by the server, like the secret key and then database information

* Load the database with the models and the data.

```
python manage.py init_db
python manage.py load_buildings
python manage.py load_courses
```

* Start the application

```
python manage.py runserver
```


