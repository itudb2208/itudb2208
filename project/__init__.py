import os
import importlib
from flask import Flask
from flask_login import LoginManager, UserMixin,AnonymousUserMixin
from . import db

BLUEPRINT_NAMES = ['about','login','teams','players','coaches','query','player','coach','team','home','delete']  # Names of the blueprints (sub-applications) that will be registered by the main application

# user class for login
class User(UserMixin):
    def __init__(self, name, password, id, active=True):
        self.name = name
        self.password = password
        self.id = id
        self.active = active

    def is_active(self):
        return self.active
    
    def is_authenticated(self):
        return True

# anonymous user is used for not logged users
class Anonymous(AnonymousUserMixin):
    name = "Anonymous"

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db', 'db.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    db.register_app(app)
    login_manager.init_app(app)

    for bp_name in BLUEPRINT_NAMES:  # Dynamic blueprint register
        bp_module = importlib.import_module(f"project.blueprints.{bp_name}")
        app.register_blueprint(bp_module.bp)
    
    return app