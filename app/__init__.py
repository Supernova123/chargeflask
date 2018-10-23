"""
filename: __init__.py
description: Initiate Charge Tracker app
created by: Omar De La Hoz (oed7416@rit.edu)
created on: 09/07/17
"""

from flask import Flask, request, abort, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import *
from sqlalchemy_utils import ChoiceType
from flask_socketio import SocketIO
from flask_login import LoginManager
from saml import SamlRequest, SamlManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Create the app and add configuration.
sentry_sdk.init()
app = Flask(__name__, template_folder = 'static', static_folder = 'static/static')
app.config.from_object('config')
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Setup flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/saml/login'

# Setup python-saml-flask
saml_manager = SamlManager()
saml_manager.init_app(app)

# Import each module created.
from app.users.controllers import *
from app.committees.controllers import *
from app.members.controllers import *
from app.charges.controllers import *
from app.actions.controllers import *
from app.committee_notes.controllers import *
from app.notes.controllers import *
from app.actions.models import Actions
from app.notes.models import Notes
db.create_all()

# Route to shibboleth login.
@app.route('/saml/login')
def login_page():
	return redirect("/saml/login")

# Route to everything else in the app.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# Route to get shibboleth metadata.
if app.config['DEBUG']:
	@app.route('/metadata/')
	def metadata():
	  saml = SamlRequest(request)
	  return saml.generate_metadata()
