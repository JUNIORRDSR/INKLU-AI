import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class Config:
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Configuración de la base de datos para SQL Server utilizando variables de entorno
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{os.environ.get('SQLSERVER_USER')}:{os.environ.get('SQLSERVER_PASSWORD')}@{os.environ.get('SQLSERVER_HOST')}/{os.environ.get('SQLSERVER_DATABASE')}?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave de encriptación para los datos sensibles
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    
    # Clave API para DeepSeek
    API_DEEPSEEK_KEY = os.environ.get('API_DEEPSEEK_KEY')
    
    @staticmethod
    def init_app(app):
        """Inicialización adicional de la aplicación"""
        pass

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False

class TestingConfig(Config):
    """Configuración para entorno de pruebas"""
    TESTING = True
    # Usar una base de datos SQLite en memoria para pruebas
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}