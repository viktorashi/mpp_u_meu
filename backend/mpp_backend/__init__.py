from flask import Flask, request, jsonify, make_response
import sqlite3
from flask_cors import CORS
import os
import json
from .db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

    app.config.from_mapping(
        SECRET_KEY='dbbb6fdcac399479b11da30061d36a173d2351ca64d4ef5a2daa7a2e4d798483',
        DATABASE=os.path.join(app.instance_path, 'mpp_backend.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    db.init_app(app)

    from . import elements
    from . import molecules
    app.register_blueprint(elements.bp)
    app.register_blueprint(molecules.bp)
    
    return app
