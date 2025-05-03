from app import create_app, db
from app.models.job import Job
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

def test_create_job(client):
    response = client.post('/jobs', json={
        'titulo': 'Desarrollador Backend',
        'descripcion': 'Buscamos un desarrollador backend con experiencia en Python.',
        'requisitos': 'Experiencia en Flask y SQLAlchemy.',
        'id_empresa': 1
    })
    assert response.status_code == 201
    assert response.json['titulo'] == 'Desarrollador Backend'

def test_get_jobs(client):
    response = client.get('/jobs')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_job(client):
    response = client.post('/jobs', json={
        'titulo': 'Desarrollador Frontend',
        'descripcion': 'Buscamos un desarrollador frontend con experiencia en React.',
        'requisitos': 'Experiencia en JavaScript y CSS.',
        'id_empresa': 1
    })
    job_id = response.json['id_vacante']
    
    response = client.put(f'/jobs/{job_id}', json={
        'titulo': 'Desarrollador Frontend Senior',
        'descripcion': 'Buscamos un desarrollador frontend senior con experiencia en React.',
        'requisitos': 'Experiencia en JavaScript, CSS y gestión de proyectos.',
        'id_empresa': 1
    })
    assert response.status_code == 200
    assert response.json['titulo'] == 'Desarrollador Frontend Senior'

def test_delete_job(client):
    response = client.post('/jobs', json={
        'titulo': 'Desarrollador Full Stack',
        'descripcion': 'Buscamos un desarrollador full stack con experiencia en MERN.',
        'requisitos': 'Experiencia en MongoDB, Express, React y Node.js.',
        'id_empresa': 1
    })
    job_id = response.json['id_vacante']
    
    response = client.delete(f'/jobs/{job_id}')
    assert response.status_code == 204

    response = client.get(f'/jobs/{job_id}')
    assert response.status_code == 404