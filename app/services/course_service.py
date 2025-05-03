from app.models.course import Course
from app.schemas.course_schema import CourseSchema
from app.extensions import db

class CourseService:
    @staticmethod
    def create_course(data):
        """Crea un nuevo curso"""
        try:
            course = Course()
            course.Titulo = data.get('Titulo')
            course.Descripcion = data.get('Descripcion')  # Será encriptado automáticamente
            course.Accesibilidad = data.get('Accesibilidad')
            course.URLContenido = data.get('URLContenido')  # Será encriptado automáticamente
            
            db.session.add(course)
            db.session.commit()
            
            course_schema = CourseSchema()
            return course_schema.dump(course)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_courses():
        """Obtiene todos los cursos"""
        courses = Course.query.all()
        course_schema = CourseSchema(many=True)
        return course_schema.dump(courses)

    @staticmethod
    def get_course(course_id):
        """Obtiene un curso por su ID"""
        course = Course.query.get(course_id)
        if not course:
            return None
            
        course_schema = CourseSchema()
        return course_schema.dump(course)

    @staticmethod
    def update_course(course_id, data):
        """Actualiza un curso existente"""
        course = Course.query.get(course_id)
        if not course:
            return None
            
        try:
            if 'Titulo' in data:
                course.Titulo = data.get('Titulo')
            if 'Descripcion' in data:
                course.Descripcion = data.get('Descripcion')  # Será encriptado automáticamente
            if 'Accesibilidad' in data:
                course.Accesibilidad = data.get('Accesibilidad')
            if 'URLContenido' in data:
                course.URLContenido = data.get('URLContenido')  # Será encriptado automáticamente
                
            db.session.commit()
            
            course_schema = CourseSchema()
            return course_schema.dump(course)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_course(course_id):
        """Elimina un curso por su ID"""
        course = Course.query.get(course_id)
        if not course:
            return False
            
        try:
            db.session.delete(course)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e