from app.models.application import Application
from app.schemas.application_schema import ApplicationSchema
from app.extensions import db

class ApplicationService:
    @staticmethod
    def create_application(data):
        """Crea una nueva postulación"""
        try:
            application = Application()
            application.IdUsuario = data.get('IdUsuario')
            application.IdVacante = data.get('IdVacante')
            application.Estado = data.get('Estado', 'Pendiente')
            
            db.session.add(application)
            db.session.commit()
            
            application_schema = ApplicationSchema()
            return application_schema.dump(application)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_application(application_id):
        """Obtiene una postulación por su ID"""
        application = Application.query.get(application_id)
        if not application:
            return None
            
        application_schema = ApplicationSchema()
        return application_schema.dump(application)

    @staticmethod
    def update_application(application_id, data):
        """Actualiza una postulación existente"""
        application = Application.query.get(application_id)
        if not application:
            return None
            
        try:
            if 'IdUsuario' in data:
                application.IdUsuario = data.get('IdUsuario')
            if 'IdVacante' in data:
                application.IdVacante = data.get('IdVacante')
            if 'Estado' in data:
                application.Estado = data.get('Estado')
                
            db.session.commit()
            
            application_schema = ApplicationSchema()
            return application_schema.dump(application)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_application(application_id):
        """Elimina una postulación por su ID"""
        application = Application.query.get(application_id)
        if not application:
            return False
            
        try:
            db.session.delete(application)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_applications():
        """Obtiene todas las postulaciones"""
        applications = Application.query.all()
        application_schema = ApplicationSchema(many=True)
        return application_schema.dump(applications)