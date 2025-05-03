from app import create_app, db
from app.models.course import Course
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

def test_create_course(client):
    response = client.post('/courses', json={
        'Titulo': 'Curso de Prueba',
        'Descripcion': 'Descripción del curso de prueba',
        'Accesibilidad': 'Alta',
        'URLContenido': 'http://example.com'
    })
    assert response.status_code == 201
    assert response.json['Titulo'] == 'Curso de Prueba'

def test_get_courses(client):
    response = client.get('/courses')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_course(client):
    # Primero, creamos un curso para actualizar
    response = client.post('/courses', json={
        'Titulo': 'Curso de Actualización',
        'Descripcion': 'Descripción del curso a actualizar',
        'Accesibilidad': 'Media',
        'URLContenido': 'http://example.com'
    })
    course_id = response.json['id']

    # Ahora, actualizamos el curso
    response = client.put(f'/courses/{course_id}', json={
        'Titulo': 'Curso Actualizado',
        'Descripcion': 'Descripción del curso actualizado',
        'Accesibilidad': 'Baja',
        'URLContenido': 'http://example.com/updated'
    })
    assert response.status_code == 200
    assert response.json['Titulo'] == 'Curso Actualizado'

def test_delete_course(client):
    # Primero, creamos un curso para eliminar
    response = client.post('/courses', json={
        'Titulo': 'Curso a Eliminar',
        'Descripcion': 'Descripción del curso a eliminar',
        'Accesibilidad': 'Baja',
        'URLContenido': 'http://example.com'
    })
    course_id = response.json['id']

    # Ahora, eliminamos el curso
    response = client.delete(f'/courses/{course_id}')
    assert response.status_code == 204

    # Verificamos que el curso ya no existe
    response = client.get(f'/courses/{course_id}')
    assert response.status_code == 404