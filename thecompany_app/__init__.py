"""
Initializes the WEB application and web service.
"""
import os

import sqlalchemy
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config


MIGRATIONS_DIR = os.path.join('thecompany_app', 'migrations')
TEMPLATES_DIR = 'templates'

# Flask
app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.config.from_object(Config)

# Flask RESTful
api = Api(app)

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATIONS_DIR)

from thecompany_app.rest import init_api

init_api()

from thecompany_app.views import init_views

init_views()

from thecompany_app.models import department, employee

# Creating the tables and populating the DB
if not (sqlalchemy.inspect(db.engine).has_table("department") or
        sqlalchemy.inspect(db.engine).has_table("employee")):
    from thecompany_app.models.populate import Populate
    Populate.populate()


