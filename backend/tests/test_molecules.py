import json
import sqlite3
from mpp_backend import create_app
from mpp_backend.db import get_db


def test_get_all_molecules(client, app):
    response = client.get('/molecules')
    assert response.status_code == 200
    data = json.loads(response.data)
    con = sqlite3.connect(app.config['DATABASE'])
    cur = con.cursor()
    cur.execute("SELECT * FROM molecules")
    items = cur.fetchall()
    # print (items)
    # print (data)
    assert len(data) == len(items)

def test_get_molecule(client):
    response = client.get('/molecules/1')
    print(client.get('molecules').data)
    print(response.data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['formula'] == "C[C@H]([C@@H](C)Cl)Cl"

def test_get_primary_molecules(client):
    response = client.get('/molecules/primary/1')
    assert response.status_code == 201
    assert len(json.loads(response.data)) == 6

    response = client.get('/molecules/primary/119')
    assert response.status_code == 404

def test_add_molecule(client):
    data = {'formula': 'KaKaMaKa', 'logp' : 69, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 48593485}
    response = client.post('/molecules', json=data)
    assert response.status_code == 201
    id  = json.loads(response.data)['id'] 
    assert json.loads( client.get('/molecules/'+str(id)).data)['formula'] == 'KaKaMaKa'

    already_in_there = {'formula': 'C[C@H]([C@@H](C)Cl)Cl', 'logp' : 2.3, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 1}
    response = client.post('/molecules', json=already_in_there)
    assert response.status_code == 409

    bad_format = {'lmao' : 'lmao'}
    response = client.post('/molecules', json=bad_format)
    assert response.status_code == 403


def test_update_molecule(client):
    data = {'formula': 'C[C@H]([C@@H](C)Cl)Cl', 'logp' : 69, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 1}
    old_data = {'formula': 'C[C@H]([C@@H](C)Cl)Cl', 'logp' : 2.3, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 1}

    response = client.put('/molecules/1', json=data)
    assert response.status_code == 200

    response = client.get('/molecules/1')
    data = json.loads(response.data)
    assert data['logp'] == 69

    data = {'sa moara':'franta'}
    response = client.put('/molecules/1', json=data)
    assert response.status_code == 403

    not_found = {'formula': 'C[C@H]([C@@H](C)Cl)Cl', 'logp' : 69, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 999}
    response = client.put('/molecules/999', json=not_found)
    assert response.status_code == 404

def test_delete_molecule(client):
    data = {'formula': 'KaKaMaKa', 'logp' : 69, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 48593485}
    response = client.post('/molecules', json=data)
    assert response.status_code == 201
    id = json.loads(response.data)['id']
    print(id)
    response = client.delete('/molecules/'+str(id))
    assert response.status_code == 204

    response = client.get('/molecules/'+str(id))
    assert response.status_code == 404

    not_found = {'formula': 'KaKaMaKa', 'logp' : 69, 'primary_element_symbol' : 'C', 'primary_element' : 6 , 'id': 48593485}
    response = client.delete('/molecules/48593485')
    assert response.status_code == 404