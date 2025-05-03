from app.models.job import Job
from app.schemas.job_schema import JobSchema
from app.extensions import db

class JobService:
    @staticmethod
    def create_job(data):
        """Crea una nueva vacante"""
        try:
            job = Job()
            job.IdEmpresa = data.get('IdEmpresa')
            job.Titulo = data.get('Titulo')
            job.Descripcion = data.get('Descripcion')  # Será encriptado automáticamente
            job.Requisitos = data.get('Requisitos')  # Será encriptado automáticamente
            
            db.session.add(job)
            db.session.commit()
            
            job_schema = JobSchema()
            return job_schema.dump(job)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_job(job_id):
        """Obtiene una vacante por su ID"""
        job = Job.query.get(job_id)
        if not job:
            return None
            
        job_schema = JobSchema()
        return job_schema.dump(job)

    @staticmethod
    def update_job(job_id, data):
        """Actualiza una vacante existente"""
        job = Job.query.get(job_id)
        if not job:
            return None
            
        try:
            if 'IdEmpresa' in data:
                job.IdEmpresa = data.get('IdEmpresa')
            if 'Titulo' in data:
                job.Titulo = data.get('Titulo')
            if 'Descripcion' in data:
                job.Descripcion = data.get('Descripcion')  # Será encriptado automáticamente
            if 'Requisitos' in data:
                job.Requisitos = data.get('Requisitos')  # Será encriptado automáticamente
                
            db.session.commit()
            
            job_schema = JobSchema()
            return job_schema.dump(job)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_job(job_id):
        """Elimina una vacante por su ID"""
        job = Job.query.get(job_id)
        if not job:
            return False
            
        try:
            db.session.delete(job)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_jobs():
        """Obtiene todas las vacantes"""
        jobs = Job.query.all()
        job_schema = JobSchema(many=True)
        return job_schema.dump(jobs)