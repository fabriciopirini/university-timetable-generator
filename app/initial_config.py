from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import psycopg2

APP = Flask(__name__)

APP.debug = True

APP.config['TEMPLATES_AUTO_RELOAD'] = True

APP.config['SECRET_KEY'] = 'abc123-'

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s:%s/%s?sslmode=require' % (
    'manager@unifei-timetable', 'supersecretpass', 'unifei-timetable.postgres.database.azure.com', '5432', 'eventregistration'
)

# initialize the database connection
DB = SQLAlchemy(APP)

# debug SQLAlchemy queries
toolbar = DebugToolbarExtension(APP)

# initialize database migration management
MIGRATE = Migrate(APP, DB)
