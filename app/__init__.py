from flask import Flask, render_template
from flask_cors import CORS
from app.config import config
from app.extensions import db, ma, login_manager, migrate
import os

def create_app(config_name='development'):
    # Determinar la configuración a utilizar
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Crear la aplicación Flask
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configurar CORS para permitir solicitudes del frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    
    # Importar y registrar blueprints con prefijos usando la función existente
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Registrar manejadores de errores personalizados
    register_error_handlers(app)
    
    # Añadir ruta para servir la aplicación React
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        # Si la ruta comienza con 'api', Flask la manejará con las rutas definidas
        if path.startswith('api/'):
            return app.send_static_file('react/index.html')
            
        # Para las solicitudes de archivos estáticos (.js, .css, etc.)
        if '.' in path:
            return app.send_static_file(f'react/{path}')
            
        # Para todas las demás rutas, enviamos el index.html de React
        return app.send_static_file('react/index.html')
    
    # Mostrar rutas registradas en la consola (útil para debug)
    if app.config['DEBUG']:
        print("Rutas registradas:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")
    
    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403