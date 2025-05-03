from app.extensions import db

class DisabilityType(db.Model):
    __tablename__ = 'Tipos_Discapacidad'

    IdDiscapacidad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.String(255))
    
    # Relaciones
    usuarios = db.relationship('User', backref='tipo_discapacidad')

    def __repr__(self):
        return f'<DisabilityType {self.Nombre}>'