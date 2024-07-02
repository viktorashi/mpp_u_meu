import json
from app import create_app

items = json.load(open('periodic-table.json','r'))


# def test_create(client):
#     # Test functions as previously defined...
#     data = {'id': '1', 'name': 'Test User'}
#     response = client.post('/create', json=data)
#     assert response.status_code == 201



def test_get_items(client):
    response = client.get('/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == items

def test_get_item(client):
    response = client.get('/details/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['number'] == 1

def test_update_item(client):
    data= {'name': 'mortii masii', 'description': 'nuj', 'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}

    #try updateing an id that doesnt exist
    response = client.put('/items/999', json=data)
    assert response.status_code == 404

    response = client.put('/items/1', json=data)
    assert response.status_code == 200

    response = client.get('/details/1')
    data = json.loads(response.data)
    assert data['name'] == 'mortii masii'

    #try updating with invalid data 
    data = {'sa moara':'franta'}

    response = client.put('/items/1', json=data)
    assert response.status_code == 400



def test_create_item(client):
    data = {'name': 'mortii masii', 'description': 'nuj', 'category': 'diatomic nonmetal', 'appearance': 'colorless gas', 'discovered_by': 'Henry Cavendish', 'named_by': 'Antoine Lavoisier', 'phase': 'Gas', 'bohr_model_image': 'https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen_srp_th.png', 'summary': 'Hydrogen is a chemical element with chemical symbol H and atomic number 1. With an atomic weight of 1.00794 u, hydrogen is the lightest element on the periodic table. Its monatomic form (H) is the most abundant chemical substance in the Universe, constituting roughly 75% of all baryonic mass.'}
    response = client.post('/items', json=data)
    assert response.status_code == 201

    #120 ca e fix ultimu dupa ala
    response = client.get('/details/120')
    data = json.loads(response.data)
    assert data['name'] == 'mortii masii'

    #try submitting invalid data
    data = {'sa moara':'franta'}

    response = client.post('/items', json=data)

    assert response.status_code == 400

def test_delete_item(client):
    response = client.delete('/items/1')
    assert response.status_code == 204

    response = client.get('/details/1')
    assert response.status_code == 404

    response = client.delete('/items/999')
    print(response.data)
    assert response.status_code == 404
