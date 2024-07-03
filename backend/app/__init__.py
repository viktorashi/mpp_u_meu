from flask import Flask, request, jsonify, make_response
import sqlite3
from flask_cors import CORS
from marshmallow import Schema, fields, ValidationError
import os
import json
from .db import get_db

class ItemSchema(Schema):
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    atomic_number = fields.Int(required=True)
    appearance = fields.Str(required=True)
    discovered_by = fields.Str(required=True)
    named_by = fields.Str(required=True)
    phase = fields.Str(required=True)
    bohr_model_image = fields.Str(required=True)
    summary = fields.Str(required=True)
    symbol = fields.Str(required=True)

item_schema = ItemSchema()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

    app.config.from_mapping(
        SECRET_KEY='dbbb6fdcac399479b11da30061d36a173d2351ca64d4ef5a2daa7a2e4d798483',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
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

    @app.get('/details/<int:atomicnumber>')
    def get_item(atomicnumber):
        #query db for the element of id 'number' 
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM elements WHERE atomic_number = ?", (atomicnumber,)
        )
        item = res.fetchone()
        if item is None:
            response = make_response(jsonify({'message': 'Item not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        response = make_response(item)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.get('/elements') 
    def get_items():
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM elements"
        )
        items = res.fetchall()
        response = make_response(jsonify(items))
        response.headers.add('Access-Control-Allow-Origin', '*')
        # print(response.data)
        return response

    @app.put('/elements/<int:atomicnumber>')
    def update_item(atomicnumber):
        data = request.get_json()
        print(data)
        try: 
            item = item_schema.load(data)
            db = get_db()
            cur = db.cursor()
            cur.execute("select id from elements where atomic_number = ?", (int(atomicnumber),))
            if cur.fetchone() is None:
                response = make_response(jsonify({'message': 'Item not found!'}), 404)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            res = cur.execute(
                "UPDATE elements SET atomic_number = ?, symbol = ?, name = ?, category = ?, appearance = ?, discovered_by = ?, named_by = ?, phase = ?, bohr_model_image = ?, summary = ? WHERE atomic_number = ?", (item['atomic_number'], item['symbol'], item['name'], item['category'], item['appearance'], item['discovered_by'], item['named_by'], item['phase'], item['bohr_model_image'], item['summary'], atomicnumber )
            )
            db.commit()
            response = make_response(jsonify(item))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        #if it's not even in the correct format
        except ValidationError as err:
            print(err)
            response = make_response(jsonify({"message": "Wrong format! (maybe you haven't specified atomic number/ symbol)"}), 403)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except sqlite3.IntegrityError as err:
            print(err)
            return make_response(jsonify({"message" : "There's already an element with that symbol/atomic number"}) , 409)


    @app.post('/elements')
    def create_item():
        data = request.get_json()
        print(data)
        try: 
            item =  item_schema.load(data)
            #check if there's already one with the same number
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id FROM elements WHERE atomic_number = ?", (item['atomic_number'],))
            if cur.fetchone() is not None:
                return make_response(jsonify({'message': 'Atomic no. / symbol already in there!'}), 409)

            #add it there then
            cur.execute(
                "INSERT INTO elements (atomic_number, symbol, name, category, appearance, discovered_by, named_by, phase, bohr_model_image, summary) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)", (item['atomic_number'],item['symbol'], item['name'], item['category'], item['appearance'], item['discovered_by'], item['named_by'], item['phase'], item['bohr_model_image'], item['summary'],)
            )
            db.commit()
            response = make_response(jsonify(item), 201)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ValidationError as err:
            print(err)
            return make_response(jsonify({'message': "Wrong format! (maybe you haven't specified atomic number/ symbol)"}), 403)
        except sqlite3.IntegrityError as err:
            print(err)
            return make_response(jsonify({"message" : "Already an element with that symbol in there!"}) , 409)
 

    @app.delete('/elements/<int:atomicnumber>')
    def delete_item(atomicnumber):
        #check if already there or not
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM elements WHERE atomic_number = ?", (atomicnumber,))
        if cur.fetchone() is None:
            response = make_response(jsonify({'message': 'Item not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response 

        cur.execute("DELETE FROM elements WHERE atomic_number = ?", (atomicnumber,))
        db.commit()
        response = make_response('', 204)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    from . import db
    db.init_app(app)

    return app
