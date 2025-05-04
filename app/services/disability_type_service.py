from app.models.disability_type import DisabilityType
from app.schemas.disability_type_schema import DisabilityTypeSchema
from app.extensions import db

class DisabilityTypeService:
    @staticmethod
    def create_disability_type(data):
        """Crea un nuevo tipo de discapacidad"""
        try:
            disability_type = DisabilityType()
            disability_type.Nombre = data.get('Nombre')
            disability_type.Descripcion = data.get('Descripcion')
            
            db.session.add(disability_type)
            db.session.commit()
            
            disability_type_schema = DisabilityTypeSchema()
            return disability_type_schema.dump(disability_type)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_disability_type(disability_type_id):
        """Obtiene un tipo de discapacidad por su ID"""
        disability_type = DisabilityType.query.get(disability_type_id)
        if not disability_type:
            return None
            
        disability_type_schema = DisabilityTypeSchema()
        return disability_type_schema.dump(disability_type)

    @staticmethod
    def update_disability_type(disability_type_id, data):
        """Actualiza un tipo de discapacidad existente"""
        disability_type = DisabilityType.query.get(disability_type_id)
        if not disability_type:
            return None
            
        try:
            if 'Nombre' in data:
                disability_type.Nombre = data.get('Nombre')
            if 'Descripcion' in data:
                disability_type.Descripcion = data.get('Descripcion')
                
            db.session.commit()
            
            disability_type_schema = DisabilityTypeSchema()
            return disability_type_schema.dump(disability_type)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_disability_type(disability_type_id):
        """Elimina un tipo de discapacidad por su ID"""
        disability_type = DisabilityType.query.get(disability_type_id)
        if not disability_type:
            return False
            
        try:
            db.session.delete(disability_type)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_disability_types():
        """Obtiene todos los tipos de discapacidad"""
        disability_types = DisabilityType.query.all()
        disability_type_schema = DisabilityTypeSchema(many=True)
        return disability_type_schema.dump(disability_types)

    @staticmethod
    def get_disability_types_by_name(name):
        try:
            # Realizamos una búsqueda case-insensitive que contenga el texto
            # El % funciona como comodín en las consultas SQL LIKE
            disability_types = DisabilityType.query.filter(
                DisabilityType.Nombre.ilike(f'%{name}%')
            ).all()
            
            if not disability_types:
                return []
                
            disability_type_schema = DisabilityTypeSchema(many=True)
            return disability_type_schema.dump(disability_types)
        except Exception as e:
            # Registrar el error pero devolver lista vacía para que la API maneje el error de manera controlada
            print(f"Error al buscar tipos de discapacidad por nombre: {str(e)}")
            return []