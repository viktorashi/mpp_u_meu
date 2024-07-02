from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from marshmallow import Schema, fields, ValidationError
import os
import json

class ItemSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Str(required=True)
    appearance = fields.Str(required=True)
    discovered_by = fields.Str(required=True)
    named_by = fields.Str(required=True)
    phase = fields.Str(required=True)
    bohr_model_image = fields.Str(required=True)
    summary = fields.Str(required=True)

item_schema = ItemSchema()
items = json.load(open('periodic-table.json','r'))
last_index= len(items)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

    app.config.from_mapping(
        SECRET_KEY='dbbb6fdcac399479b11da30061d36a173d2351ca64d4ef5a2daa7a2e4d798483',
        #inca nuuu
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    @app.get('/details/<int:number>')
    def get_item(number):
        item = next((item for item in items if item['number'] == number), None)
        if item is None:
            return jsonify({'message': 'Item not found'}), 404
        response = make_response(jsonify(item))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.get('/items') 
    def get_items():
        response = make_response(jsonify(items))
        response.headers.add('Access-Control-Allow-Origin', '*')
        # print(response.data)
        return response

    @app.post('/items')
    def create_item():
        global last_index
        data = request.get_json()
        print(data)
        try: 
            item =  item_schema.load(data)
            last_index +=1
            item['number'] = last_index
            items.append(item)
            response = make_response(jsonify(item), 201)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ValidationError as err:
            print(err)
            return make_response(jsonify( err.messages), 400)
            

    @app.put('/items/<int:item_id>')
    def update_item(item_id):
        #s-ar putea comenteze ca unu are id celelat n-are sau cv gen
        data = request.get_json()
        print(data)
        try: 
            item = item_schema.load(data)
            item = next((item for item in items if item['number'] == item_id), None)
            if item is None:
                return jsonify({'message': 'Item not found'}), 404
            #doar asa merge sa dai update la dict aparent numa sa fi atenta sa nu faci invers ca dupa ai mai multe keyuri in item
            for key in data:
                item[key] = data[key]
            response = make_response(jsonify(item))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ValidationError as err:
            print(err)
            return make_response(jsonify(  err.messages), 400)

    @app.delete('/items/<int:item_id>')
    def delete_item(item_id):
        global items
        if item_id < 1 or item_id > last_index:
            response = make_response(jsonify({'message': 'Item not found'}), 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response 

        items = [item for item in items if item['number'] != item_id]
        response = make_response('', 204)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return app
