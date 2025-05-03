from app.models.enrollment import Enrollment
from app.schemas.enrollment_schema import EnrollmentSchema
from app.extensions import db

class EnrollmentService:
    @staticmethod
    def create_enrollment(data):
        """Crea una nueva inscripción a curso"""
        try:
            enrollment = Enrollment()
            enrollment.id_curso = data.get('id_curso')
            enrollment.id_usuario = data.get('id_usuario')
            
            db.session.add(enrollment)
            db.session.commit()
            
            enrollment_schema = EnrollmentSchema()
            return enrollment_schema.dump(enrollment)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_enrollment(curso_id, usuario_id):
        """Obtiene una inscripción por sus IDs combinados"""
        enrollment = Enrollment.query.filter_by(
            id_curso=curso_id, 
            id_usuario=usuario_id
        ).first()
        
        if not enrollment:
            return None
            
        enrollment_schema = EnrollmentSchema()
        return enrollment_schema.dump(enrollment)

    @staticmethod
    def delete_enrollment(curso_id, usuario_id):
        """Elimina una inscripción por sus IDs combinados"""
        enrollment = Enrollment.query.filter_by(
            id_curso=curso_id, 
            id_usuario=usuario_id
        ).first()
        
        if not enrollment:
            return False
            
        try:
            db.session.delete(enrollment)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_enrollments_by_user(usuario_id):
        """Obtiene todas las inscripciones de un usuario"""
        enrollments = Enrollment.query.filter_by(id_usuario=usuario_id).all()
        enrollment_schema = EnrollmentSchema(many=True)
        return enrollment_schema.dump(enrollments)
        
    @staticmethod
    def get_enrollments_by_course(curso_id):
        """Obtiene todas las inscripciones para un curso"""
        enrollments = Enrollment.query.filter_by(id_curso=curso_id).all()
        enrollment_schema = EnrollmentSchema(many=True)
        return enrollment_schema.dump(enrollments)

    @staticmethod
    def get_all_enrollments():
        """Obtiene todas las inscripciones"""
        enrollments = Enrollment.query.all()
        enrollment_schema = EnrollmentSchema(many=True)
        return enrollment_schema.dump(enrollments)