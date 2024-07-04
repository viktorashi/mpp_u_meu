from flask import Flask, request, jsonify, make_response
import sqlite3
from flask_cors import CORS
from marshmallow import Schema, fields, ValidationError
import os
import json
from .db import get_db

class ElementSchema(Schema):
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

class MoleculeSchema(Schema):
    id = fields.Int(required=True)
    formula = fields.Str(required=True)
    logp = fields.Float(required=True)
    primary_element_symbol = fields.Str(required=True)
    primary_element = fields.Int(required=True)

element_schema = ElementSchema()
molecule_schema = MoleculeSchema()

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
    def get_element(atomicnumber):
        #query db for the element of id 'number' 
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM elements WHERE atomic_number = ?", (atomicnumber,)
        )
        element = res.fetchone()
        if element is None:
            response = make_response(jsonify({'message': 'Element not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        response = make_response(element)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.get('/elements') 
    def get_elements():
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM elements"
        )
        elements = res.fetchall()
        response = make_response(jsonify(elements))
        response.headers.add('Access-Control-Allow-Origin', '*')
        # print(response.data)
        return response

    @app.put('/elements/<int:atomicnumber>')
    def update_element(atomicnumber):
        data = request.get_json()
        print(data)
        try: 
            element = element_schema.load(data)
            db = get_db()
            cur = db.cursor()
            cur.execute("select id from elements where atomic_number = ?", (int(atomicnumber),))
            if cur.fetchone() is None:
                response = make_response(jsonify({'message': 'Element not found!'}), 404)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            res = cur.execute(
                "UPDATE elements SET atomic_number = ?, symbol = ?, name = ?, category = ?, appearance = ?, discovered_by = ?, named_by = ?, phase = ?, bohr_model_image = ?, summary = ? WHERE atomic_number = ?", (element['atomic_number'], element['symbol'], element['name'], element['category'], element['appearance'], element['discovered_by'], element['named_by'], element['phase'], element['bohr_model_image'], element['summary'], atomicnumber )
            )
            db.commit()
            response = make_response(jsonify(element))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        #if it's not even in the correct format
        except ValidationError as err:
            print(err)
            response = make_response(jsonify({"message": "Wrong format! (maybe you haven't specified atomic number/ symbol)"}), 403)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


    @app.post('/elements')
    def create_element():
        data = request.get_json()
        print(data)
        try: 
            element =  element_schema.load(data)
            #check if there's already one with the same number
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id FROM elements WHERE atomic_number = ?", (element['atomic_number'],))
            if cur.fetchone() is not None:
                return make_response(jsonify({'message': 'Atomic no. / symbol already in there!'}), 409)

            #add it there then
            cur.execute(
                "INSERT INTO elements (atomic_number, symbol, name, category, appearance, discovered_by, named_by, phase, bohr_model_image, summary) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)", (element['atomic_number'],element['symbol'], element['name'], element['category'], element['appearance'], element['discovered_by'], element['named_by'], element['phase'], element['bohr_model_image'], element['summary'],)
            )
            db.commit()
            response = make_response(jsonify(element), 201)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ValidationError as err:
            print(err)
            return make_response(jsonify({'message': "Wrong format! (maybe you haven't specified atomic number/ symbol)"}), 403)
        except sqlite3.IntegrityError as err:
            print(err)
            return make_response(jsonify({"message" : "Already an element with that symbol in there!"}) , 409)
 

    @app.delete('/elements/<int:atomicnumber>')
    def delete_element(atomicnumber):
        #check if already there or not
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM elements WHERE atomic_number = ?", (atomicnumber,))
        if cur.fetchone() is None:
            response = make_response(jsonify({'message': 'Element not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response 

        cur.execute("DELETE FROM elements WHERE atomic_number = ?", (atomicnumber,))
        db.commit()
        response = make_response('', 204)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    @app.get('/molecules')
    def get_all_molecules():
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM molecules"
        )
        elements = res.fetchall()
        response = make_response(jsonify(elements))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.get('/molecules/<int:id>') 
    def get_molecule(id):
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM molecules WHERE id = ?", (id,)
        )
        element = res.fetchone()
        if element is None:
            response = make_response(jsonify({'message': 'Element not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        response = make_response(element)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.get('/primarymolecules/<int:atomic_number>')
    def get_primary_molecules(atomic_number):
        ''' see for which molecules is this element the primary one, used for the second fetch call in the details page of the element'''
        db = get_db()
        cur = db.cursor()
        res = cur.execute(
            "SELECT * FROM molecules WHERE primary_element = ?", (atomic_number,)
        )
        elements = res.fetchall()
        if len(elements) == 0:
            response = make_response(jsonify({'message': 'No such molecules'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        response = make_response(jsonify(elements),201)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    '''returns the id of the molecule added'''
    @app.post('/molecules')
    def add_molecule():
        data = request.get_json()
        print(data)
        try: 
            molecule = molecule_schema.load(data)
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id FROM molecules WHERE id = ?", (molecule['id'],))
            if cur.fetchone() is not None:
                return make_response(jsonify({'message': 'Molecule already in there!'}), 409)

            cur.execute(
                "INSERT INTO molecules ( formula, logp, primary_element_symbol, primary_element) VALUES ( ?,?, ?, ?)",  (molecule['formula'],molecule['logp'], molecule['primary_element_symbol'], molecule['primary_element'])
            )
            db.commit()
            #get its assigned id
            cur.execute("SELECT id FROM molecules WHERE formula = ?", (molecule['formula'],))
            id = cur.fetchone()
            response = make_response(jsonify(id), 201)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ValidationError as err:
            print(err)
            return make_response(jsonify({'message': "Wrong format! there are fields you haven't specified "}), 403)


    @app.put('/molecules/<int:id>')
    def update_molecule(id):
        data = request.get_json()
        print(data)
        try: 
            molecule = molecule_schema.load(data)
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT id FROM molecules WHERE id = ?", (id,))
            if cur.fetchone() is None:
                return make_response(jsonify({'message': 'Molecule not found!'}), 404)

            cur.execute(
                "UPDATE molecules SET formula = ?, logp = ?, primary_element_symbol = ?, primary_element = ? WHERE id = ?", (molecule['formula'], molecule['logp'], molecule['primary_element_symbol'], molecule['primary_element'], id)
            )
            db.commit()
            response = make_response(jsonify(data), 200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ValidationError as err:
            print(err)
            return make_response(jsonify({'message': 'Wrong format!'}), 403)

    @app.delete('/molecules/<int:id>')
    def delete_molecule(id):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM molecules WHERE id = ?", (id,))
        if cur.fetchone() is None:
            response = make_response(jsonify({'message': 'Element not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        cur.execute("DELETE FROM molecules WHERE id = ?", (id,))
        db.commit()
        response = make_response('', 204)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    from . import db
    db.init_app(app)

    return app
