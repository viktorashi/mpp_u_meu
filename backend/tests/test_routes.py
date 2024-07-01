import pytest
import json
import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def inject_config(pytestconfig):
    # Example: Accessing a pytest option named 'debug'
    debug_mode = pytestconfig.getoption('debug')
    # You can also access other configuration options here if needed

def test_create(client):
    # Test functions as previously defined...
    data = {'id': '1', 'name': 'Test User'}
    response = client.post('/create', json=data)
    assert response.status_code == 201

def test_read(client):
    # Test functions as previously defined...
    response = client.get('/read/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == '1'

    response = client.get('/read/999')
    assert response.status_code == 404

def test_update(client):
    # Test functions as previously defined...
    data = {'name': 'Updated User'}
    response = client.put('/update/1', json=data)
    assert response.status_code == 200

    response = client.get('/read/1')
    data = json.loads(response.data)
    assert data['name'] == 'Updated User'

    data = {'name': 'Updated User'}
    response = client.put('/update/999', json=data)
    assert response.status_code == 404

def test_delete(client):
    # Test functions as previously defined...
    response = client.delete('/delete/1')
    assert response.status_code == 200

    response = client.get('/read/1')
    assert response.status_code == 404

    response = client.delete('/delete/999')
    assert response.status_code == 404