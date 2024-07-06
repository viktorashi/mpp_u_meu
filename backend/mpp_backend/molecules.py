from flask import Blueprint, make_response, jsonify, request
import sqlite3
from marshmallow import Schema, fields, ValidationError
from .db import get_db

bp = Blueprint('molecules', __name__, url_prefix='/molecules')

class MoleculeSchema(Schema):
    id = fields.Int(required=True)
    formula = fields.Str(required=True)
    logp = fields.Float(required=True)
    primary_element_symbol = fields.Str(required=True)
    primary_element = fields.Int(required=True)

molecule_schema = MoleculeSchema()

@bp.get('')
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

@bp.get('/<int:id>') 
def get_molecule(id):
    db = get_db()
    cur = db.cursor()
    res = cur.execute(
        "SELECT * FROM molecules WHERE id = ?", [id]
    )
    element = res.fetchone()
    if element is None:
        response = make_response(jsonify({'message': 'Element not found!'}), 404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    response = make_response(element)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@bp.get('/primary/<int:atomic_number>')
def get_primary_molecules(atomic_number : int):
    ''' see for which molecules is this element the primary one, used for the second fetch call in the details page of the element'''
    db = get_db()
    cur = db.cursor()
    print('asta inaitne')
    try:
        res = cur.execute(
            "SELECT * FROM molecules WHERE primary_element = ?", [atomic_number]
        )
        elements = res.fetchall()
        if len(elements) == 0:
            print('lm  nu stiu molecules care au asta ca main')
            response = make_response(jsonify({'message': 'No such molecules'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        response = make_response(jsonify(elements),201)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as err:
        print(err)
        print('sa moara franta')
        response = make_response(jsonify({'message': 'sa moara franta a dat cv eroare drq stie'}), 404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

'''returns the id of the molecule added'''
@bp.post('')
def add_molecule():
    data = request.get_json()
    print(data)
    try: 
        molecule = molecule_schema.load(data)
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM molecules WHERE id = ?", [molecule['id']])
        if cur.fetchone() is not None:
            return make_response(jsonify({'message': 'Molecule already in there!'}), 409)

        cur.execute(
            "INSERT INTO molecules ( formula, logp, primary_element_symbol, primary_element) VALUES ( ?,?, ?, ?)",  [molecule['formula'],molecule['logp'], molecule['primary_element_symbol'], molecule['primary_element']]
        )
        db.commit()
        #get its assigned id
        cur.execute("SELECT id FROM molecules WHERE formula = ?", [molecule['formula']])
        id = cur.fetchone()
        response = make_response(jsonify(id), 201)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except ValidationError as err:
        print(err)
        return make_response(jsonify({'message': "Wrong format! there are fields you haven't specified "}), 403)


@bp.put('/<int:id>')
def update_molecule(id):
    data = request.get_json()
    print(data)
    try: 
        molecule = molecule_schema.load(data)
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM molecules WHERE id = ?", [id])
        if cur.fetchone() is None:
            return make_response(jsonify({'message': 'Molecule not found!'}), 404)

        cur.execute(
            "UPDATE molecules SET formula = ?, logp = ?, primary_element_symbol = ?, primary_element = ? WHERE id = ?", [molecule['formula'], molecule['logp'], molecule['primary_element_symbol'], molecule['primary_element'], id]
        )
        db.commit()
        response = make_response(jsonify(data), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except ValidationError as err:
        print(err)
        return make_response(jsonify({'message': 'Wrong format!'}), 403)

@bp.delete('/<int:id>')
def delete_molecule(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM molecules WHERE id = ?", [id])
    if cur.fetchone() is None:
        response = make_response(jsonify({'message': 'Element not found!'}), 404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    cur.execute("DELETE FROM molecules WHERE id = ?", [id])
    db.commit()
    response = make_response('', 204)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

