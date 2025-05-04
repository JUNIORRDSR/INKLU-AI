from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.encryption import encrypt_data, decrypt_data

class Course(db.Model):
    __tablename__ = 'Cursos'

    IdCurso = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(100), nullable=False)
    _Descripcion = db.Column('Descripcion', db.Text, nullable=True)
    Accesibilidad = db.Column(db.String(100), nullable=True)
    _URLContenido = db.Column('URLContenido', db.String(255), nullable=True)
    
    # Relaciones
    inscripciones = db.relationship('Enrollment', backref='curso')
    
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
    def URLContenido(self):
        if self._URLContenido:
            return decrypt_data(self._URLContenido)
        return None
    
    @URLContenido.setter
    def URLContenido(self, value):
        if value:
            self._URLContenido = encrypt_data(value)
        else:
            self._URLContenido = None

    def __repr__(self):
        return f'<Course {self.Titulo}>'