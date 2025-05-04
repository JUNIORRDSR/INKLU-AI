from app import create_app, db
from app.models.user import User
import pytest

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user(client):
    response = client.post('/users', json={
        'NombreCompleto': 'Test User',
        'Correo': 'testuser@example.com',
        'Contrasena': 'password123',
        'Rol': 'Talento'
    })
    assert response.status_code == 201
    assert response.json['Correo'] == 'testuser@example.com'

def test_get_user(client):
    client.post('/users', json={
        'NombreCompleto': 'Test User',
        'Correo': 'testuser@example.com',
        'Contrasena': 'password123',
        'Rol': 'Talento'
    })
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json['NombreCompleto'] == 'Test User'

def test_update_user(client):
    client.post('/users', json={
        'NombreCompleto': 'Test User',
        'Correo': 'testuser@example.com',
        'Contrasena': 'password123',
        'Rol': 'Talento'
    })
    response = client.put('/users/1', json={
        'NombreCompleto': 'Updated User',
        'Correo': 'updateduser@example.com',
        'Contrasena': 'newpassword123',
        'Rol': 'Talento'
    })
    assert response.status_code == 200
    assert response.json['NombreCompleto'] == 'Updated User'

def test_delete_user(client):
    client.post('/users', json={
        'NombreCompleto': 'Test User',
        'Correo': 'testuser@example.com',
        'Contrasena': 'password123',
        'Rol': 'Talento'
    })
    response = client.delete('/users/1')
    assert response.status_code == 204
    response = client.get('/users/1')
    assert response.status_code == 404