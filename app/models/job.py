from app.extensions import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.encryption import encrypt_data, decrypt_data

class Job(db.Model):
    __tablename__ = 'Vacantes'

    IdVacante = db.Column(db.Integer, primary_key=True)
    IdEmpresa = db.Column(db.Integer, db.ForeignKey('Usuarios.IdUsuario'), nullable=False)
    Titulo = db.Column(db.String(100), nullable=True)
    _Descripcion = db.Column('Descripcion', db.Text, nullable=True)
    _Requisitos = db.Column('Requisitos', db.Text, nullable=True)
    FechaPublicacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Propiedades híbridas para datos sensibles
    @hybrid_property
    def Descripcion(self):
        if self._Descripcion:
            return decrypt_data(self._Descripcion)
        return None
    
    @Descripcion.setter
    def Descripcion(self, value):
        if value:
            self._Descripcion = encrypt_data(value)
        else:
            self._Descripcion = None
    
    @hybrid_property
    def Requisitos(self):
        if self._Requisitos:
            return decrypt_data(self._Requisitos)
        return None
    
    @Requisitos.setter
    def Requisitos(self, value):
        if value:
            self._Requisitos = encrypt_data(value)
        else:
            self._Requisitos = None

    def __repr__(self):
        return f'<Job {self.Titulo}>'