# INKLU-AI Flask Project

## Nota 
No usar dependecias de python 2

## Descripción
Este proyecto es una aplicación web desarrollada con Flask que implementa un modelo ORM basado en la base de datos `inkludb`. La aplicación está diseñada para gestionar usuarios, tipos de discapacidad, vacantes de empleo, postulaciones, cursos y sus inscripciones, así como indicadores asociados a los usuarios.

## Estructura del Proyecto
La estructura del proyecto es la siguiente:

```
inklu-ai-flask
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── disability_type.py
│   │   ├── job.py
│   │   ├── application.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── indicator.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── disability_type_schema.py
│   │   ├── job_schema.py
│   │   ├── application_schema.py
│   │   ├── course_schema.py
│   │   ├── enrollment_schema.py
│   │   └── indicator_schema.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── disability_type_service.py
│   │   ├── job_service.py
│   │   ├── application_service.py
│   │   ├── course_service.py
│   │   └── indicator_service.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── disabilities.py
│   │   ├── jobs.py
│   │   ├── applications.py
│   │   ├── courses.py
│   │   └── indicators.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── migrations
│   └── README.md
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_jobs.py
│   └── test_courses.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Instalación
1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd inklu-ai-flask
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso
Para ejecutar la aplicación, utiliza el siguiente comando:
```
python run.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT.