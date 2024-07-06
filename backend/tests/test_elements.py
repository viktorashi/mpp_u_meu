import json
import sqlite3
from mpp_backend import create_app
import click
from mpp_backend.db import get_db

def test_get_elements(client, app):
    response = client.get('/elements')
    assert response.status_code == 200
    data = json.loads(response.data)
    #get the temp one used for testing gen ca sa nu ia ia care chiar era legit ca inainte
    with app.app_context():
        assert get_db().execute('SELECT * FROM elements').fetchall() == data    

def test_get_element(client):
    response = client.get('/elements/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert data['name'] == "Hydrogen"



def test_update_element(client):
    data= { 'atomic_number' : 6969, 'name': 'mortii masii', 'symbol' : 'H',  'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}

    old_data = { 'atomic_number' : 1, 'name': 'Hydrogen', 'symbol' : 'H',  'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}

    #try updateing an id that doesnt exist
    response = client.put('/elements/999', json=data)
    print (response.data)
    assert response.status_code == 404

    response = client.put('/elements/1', json=data)
    print (response.data)
    assert response.status_code == 200

    response = client.get('/elements/6969')
    data = json.loads(response.data)
    assert data['name'] == 'mortii masii'

    #try updating with invalid data 
    data = {'sa moara':'franta'}

    response = client.put('/elements/6969', json=data)
    assert response.status_code == 403



def test_create_element(client):
    tot_proasta_data = {'atomic_number' : 1, 'symbol' : 'lmao','name': 'mortii masii',  'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}

    data_proasta = {'atomic_number' : 200, 'symbol' : 'H','name': 'mortii masii',  'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}

    good_data = {'atomic_number' : 200, 'symbol' : 'Fnfjen','name': 'mortii masii',  'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}

    #asta nu mere ca e deja unu cu numaru 1
    response = client.post('/elements', json=tot_proasta_data)
    print(response.data)
    assert response.status_code == 409

    #asta nu mere ca nu e unic simbolu
    response = client.post('/elements', json=data_proasta)
    assert response.status_code == 409

    #try submitting invalid data
    data = {'sa moara':'franta'}

    response = client.post('/elements', json=data)
    assert response.status_code == 403

    response = client.post('/elements', json=good_data)
    assert response.status_code == 201

    response = client.get('/elements/200')
    data = json.loads(response.data)
    print(data)
    print(response.status_code)
    assert data['name'] == 'mortii masii'



def test_delete_element(client):
    response = client.delete('/elements/1')
    assert response.status_code == 204

    response = client.get('/elements/1')
    assert response.status_code == 404

    response = client.delete('/elements/1')
    assert response.status_code == 404

    response = client.delete('/elements/999')
    print(response.data)
    assert response.status_code == 404
