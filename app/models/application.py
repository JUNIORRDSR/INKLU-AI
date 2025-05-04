from app.extensions import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'Postulaciones'

    IdPostulacion = db.Column(db.Integer, primary_key=True)
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.IdUsuario'), nullable=False)
    IdVacante = db.Column(db.Integer, db.ForeignKey('Vacantes.IdVacante'), nullable=False)
    FechaPostulacion = db.Column(db.DateTime, default=datetime.utcnow)
    Estado = db.Column(db.String(50), default='Pendiente')

    usuario = db.relationship('User', backref='postulaciones')
    vacante = db.relationship('Job', backref='postulaciones')
    
    def __repr__(self):
        return f'<Application {self.IdPostulacion} - Estado: {self.Estado}>'