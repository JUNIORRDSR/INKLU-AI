from app.extensions import db
from datetime import datetime

class Enrollment(db.Model):
    __tablename__ = 'Cursos_Usuarios'

    id_curso = db.Column(db.Integer, db.ForeignKey('Cursos.IdCurso'), primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.IdUsuario'), primary_key=True)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Enrollment Usuario:{self.id_usuario} Curso:{self.id_curso}>'