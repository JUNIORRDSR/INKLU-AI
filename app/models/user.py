from app.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.encryption import encrypt_data, decrypt_data

class User(db.Model, UserMixin):
    __tablename__ = 'Usuarios'

    IdUsuario = db.Column(db.Integer, primary_key=True)
    NombreCompleto = db.Column(db.String(100), nullable=False)
    _Correo = db.Column('Correo', db.String(100), unique=True, nullable=False)
    Contrasena = db.Column(db.String(255), nullable=False)
    Rol = db.Column(db.String(50), nullable=False)
    IdDiscapacidad = db.Column(db.Integer, db.ForeignKey('Tipos_Discapacidad.IdDiscapacidad'), nullable=True)
    FechaRegistro = db.Column(db.DateTime, server_default=db.func.now())

    # Relaciones existentes
    indicadores = db.relationship('Indicator', backref='user')
    postulaciones = db.relationship('Application', backref='usuario')
    inscripciones = db.relationship('Enrollment', backref='usuario')
    vacantes = db.relationship('Job', backref='empresa')
    
    # Propiedad híbrida para correo electrónico (encriptado)
    @hybrid_property
    def Correo(self):
        return decrypt_data(self._Correo)
    
    @Correo.setter
    def Correo(self, value):
        self._Correo = encrypt_data(value)
    
    # Métodos para contraseñas (hasheadas)
    def set_password(self, password):
        self.Contrasena = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.Contrasena, password)
    
    # Para Flask-Login
    def get_id(self):
        return str(self.IdUsuario)
    
    @property
    def is_active(self):
        # Define la lógica para determinar si el usuario está activo
        return True
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'<User {self.NombreCompleto}>'

# Esta función es necesaria para cargar usuarios desde la base de datos
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))