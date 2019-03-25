## To-Do Flask API

Simple to-do api built in [Flask](http://flask.pocoo.org/) that showcases some
of the most common patterns and configurations of RESTful api development in
this python microframework.

## Motivation

Mainly for personal reference. Publically available to help anyone who's getting
started with building RESTful APIs with Flask and needs some ideas on what technologies
or how to implement certain funcionalities.

## Technologies

- [Flask](http://flask.pocoo.org/) -> Microframework
- [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) -> RESTful API ext
- [SQLALCHEMY](https://www.sqlalchemy.org/) -> SQL ORM
- [Flask-SQLALCHEMY](http://flask-sqlalchemy.pocoo.org/2.3/) -> Adds support for
  SQLACHEMY
- [Psycopg](http://initd.org/psycopg/) -> PostgreSQL adapter for Python DBAPI
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) -> Add database migration support
  to SQLAlchemy
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) Adds database
  migration support for Alembic
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/) -> JSON Web Tokens support for python
- [pytest](https://docs.pytest.org/en/latest/) -> Testing framework

## Code Style

I'm using [Black](https://black.readthedocs.io/en/stable/) for code formatting.
I have configured Black for usage of single quotes. I find easier and faster to use 
single over double quotes. You can do so by setting the --skip-string-normalization flag in
your editor of choice. The rest is Black defaults. Check Black's docs.

## Usage

Setup the virtual environment in the project's root directory
```bash
python3 -m venv .venv # create virtual environment
source .venv/bin/activate # activates virtual environment
pip install -r requirements.txt # install required packages in virtual env
```

Supposing you have PostgreSQL installed and running, create a database
in order to complete migration steps:
```bash
psql -O [postgres user] [database name] # creates databse under given user
flask db migrate # migrates changes in databse
flask db upgrade # upgrades database
```

With the steps above completed, simply run the app as shown below.
Since Flask is configured with the FLASK_ENV in config, Flask takes cares of the rest
```bash
flask run
```

To run the tests simply run pytest from within the root directory
```bash
pytest -v
```
