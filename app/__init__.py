from flask import Flask, render_template
from flask_cors import CORS
from app.config import config
from app.extensions import db, ma, login_manager, jwt
import os

def create_app(config_name='development'):
    # Determinar la configuración a utilizar
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Crear la aplicación Flask
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    
    # Configurar la clave secreta si no está definida en la configuración
    if not app.config['SECRET_KEY']:
        # Cargar la clave secreta desde una variable de entorno
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    if not app.config['JWT_SECRET_KEY']:
        # Cargar la clave secreta JWT desde una variable de entorno   
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Importar y registrar blueprints con prefijos usando la función existente
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Registrar manejadores de errores personalizados
    register_error_handlers(app)
    
    # Registrar comandos personalizados
    register_commands(app)
    
    return app

def register_commands(app):
    @app.cli.command('list-routes')
    def list_routes():
        """Listar todas las rutas registradas en la aplicación."""
        print("Rutas registradas:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")

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