import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

MIGRATIONS_DIR = os.path.join('department_app', 'migrations')
TEMPLATES_DIR = 'templates'

app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.config.from_object(Config)

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory = MIGRATIONS_DIR)

from .views import init_views
init_views()

from .models import department, employee