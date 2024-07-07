from flask import Flask, request, jsonify, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
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
        #fa si tu cv cu kktu asta cand dai deploy un eviron var si din astea
        #get secret key from env var
        SECRET_KEY = os.environ.get('SECRET_KEY'),
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

#     app.wsgi_app = ProxyFix(
#     app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
# )
    
    return app
