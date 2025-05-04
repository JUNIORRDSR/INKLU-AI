from app.extensions import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.encryption import encrypt_data, decrypt_data

class Indicator(db.Model):
    __tablename__ = 'Indicadores'

    IdIndicador = db.Column(db.Integer, primary_key=True)
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.IdUsuario'), nullable=True)
    Tipo = db.Column(db.String(100))
    _Valor = db.Column('Valor', db.String(255))  # Cambiado a string para permitir encriptación
    FechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Propiedad híbrida para el valor (encriptado)
    @hybrid_property
    def Valor(self):
        return float(decrypt_data(self._Valor)) if self._Valor else 0
    
    @Valor.setter
    def Valor(self, value):
        self._Valor = encrypt_data(str(value)) if value is not None else None

    def __repr__(self):
        return f'<Indicator {self.Tipo}: {self.Valor}>'