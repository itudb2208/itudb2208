import os
import importlib
from flask import Flask
from . import db

BLUEPRINT_NAMES = ['home']  # Names of the blueprints (sub-applications) that will be registered by the main application

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
        
    for bp_name in BLUEPRINT_NAMES:  # Dynamic blueprint register
        bp_module = importlib.import_module(f"project.blueprints.{bp_name}")
        app.register_blueprint(bp_module.bp)
    
    return app