import flask
import pkg_resources
import flask_migrate as mg
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


def getDb() -> SQLAlchemy:
    db = getattr(flask.g, '_db', None)
    if db is None:
        db = flask.g._db = _connectDb()

    return db


def _connectDb():
    app = flask.current_app

    # Ohne Angabe den Treiber 'mysqldb' verwenden
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('mysql://', 'mysql+mysqldb://')
    db = SQLAlchemy(app)

    rows = db.session.query('1').from_statement(text('SELECT 1')).all()
    assert len(rows) == 1 and rows[0][0] == 1

    # DB Model-Migration setup
    # https://flask-migrate.readthedocs.io/en/latest/
    repoDir = pkg_resources.resource_filename(__name__, app.config['SQLALCHEMY_MIGRATE_REPO'])
    mg.Migrate(app, db, directory=repoDir)
    mg.upgrade(revision='head')

    return db
