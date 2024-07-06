from flask import Blueprint, make_response, jsonify, request
import sqlite3
from marshmallow import Schema, fields, ValidationError
from .db import get_db

bp = Blueprint('elements', __name__, url_prefix='/elements')

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

element_schema = ElementSchema()

#get all elements
@bp.get('')
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

@bp.get('/<int:atomicnumber>')
def get_element(atomicnumber):
    db = get_db()
    cur = db.cursor()
    res = cur.execute(
        "SELECT * FROM elements WHERE atomic_number = ?", [atomicnumber]
    )
    element = res.fetchone()
    if element is None:
        response = make_response(jsonify({'message': 'Element not found!'}), 404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    response = make_response(element)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@bp.put('/<int:atomicnumber>')
def update_element(atomicnumber):
    data = request.get_json()
    print(data)
    try: 
        element = element_schema.load(data)
        db = get_db()
        cur = db.cursor()
        cur.execute("select id from elements where atomic_number = ?", [atomicnumber])
        if cur.fetchone() is None:
            print("Element not found!")
            response = make_response(jsonify({'message': 'Element not found!'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        res = cur.execute(
            "UPDATE elements SET atomic_number = ?, symbol = ?, name = ?, category = ?, appearance = ?, discovered_by = ?, named_by = ?, phase = ?, bohr_model_image = ?, summary = ? WHERE atomic_number = ?", [element['atomic_number'], element['symbol'], element['name'], element['category'], element['appearance'], element['discovered_by'], element['named_by'], element['phase'], element['bohr_model_image'], element['summary'], atomicnumber ]
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


@bp.post('')
def create_element():
    data = request.get_json()
    print(data)
    try: 
        element =  element_schema.load(data)
        #check if there's already one with the same number
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM elements WHERE atomic_number = ?", [element['atomic_number']])
        if cur.fetchone() is not None:
            return make_response(jsonify({'message': 'Atomic no. / symbol already in there!'}), 409)

        #add it there then
        cur.execute(
            "INSERT INTO elements (atomic_number, symbol, name, category, appearance, discovered_by, named_by, phase, bohr_model_image, summary) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)", [element['atomic_number'],element['symbol'], element['name'], element['category'], element['appearance'], element['discovered_by'], element['named_by'], element['phase'], element['bohr_model_image'], element['summary']]
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


@bp.delete('/<int:atomicnumber>')
def delete_element(atomicnumber):
    #check if already there or not
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM elements WHERE atomic_number = ?", [atomicnumber])
    if cur.fetchone() is None:
        response = make_response(jsonify({'message': 'Element not found!'}), 404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response 

    cur.execute("DELETE FROM elements WHERE atomic_number = ?", [atomicnumber])
    db.commit()
    response = make_response('', 204)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

