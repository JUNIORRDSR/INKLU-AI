from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.extensions import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

class UserService:
    @staticmethod
    def create_user(data):
        """Crea un nuevo usuario"""
        try:
            user = User()
            user.NombreCompleto = data.get('NombreCompleto')
            user.Correo = data.get('Correo')  # Será encriptado automáticamente
            user.set_password(data.get('Contrasena'))
            user.Rol = data.get('Rol')
            user.IdDiscapacidad = data.get('IdDiscapacidad')
            
            db.session.add(user)
            db.session.commit()
            
            user_schema = UserSchema()
            return user_schema.dump(user)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user(user_id):
        """Obtiene un usuario por su ID"""
        user = User.query.get(user_id)
        if not user:
            return None
            
        user_schema = UserSchema()
        return user_schema.dump(user)

    @staticmethod
    def get_user_by_email(email):
        """Obtiene un usuario por su correo electrónico"""
        users = User.query.all()
        for user in users:
            if user.Correo == email:
                user_schema = UserSchema()
                return user_schema.dump(user)
        return None

    @staticmethod
    def login_user(email, password):
        """Autentica a un usuario y devuelve un token JWT si es exitoso"""
        try:
            user = User.query.filter_by(Correo=email).first()
            if not user:
                return {"error": "Correo no encontrado"}, None
            
            if not check_password_hash(user.Contrasena, password):
                return {"error": "Contraseña incorrecta"}, None
            
            # Crear un token JWT con información del usuario
            access_token = create_access_token(identity=user.id)
            user_schema = UserSchema()
            user_data = user_schema.dump(user)
            return {"message": "Login exitoso", "user": user_data}, access_token
        except Exception as e:
            return {"error": str(e)}, None

    @staticmethod
    def update_user(user_id, data):
        """Actualiza un usuario existente"""
        user = User.query.get(user_id)
        if not user:
            return None
            
        try:
            if 'NombreCompleto' in data:
                user.NombreCompleto = data.get('NombreCompleto')
            if 'Correo' in data:
                user.Correo = data.get('Correo')  # Será encriptado automáticamente
            if 'Contrasena' in data:
                user.set_password(data.get('Contrasena'))
            if 'Rol' in data:
                user.Rol = data.get('Rol')
            if 'IdDiscapacidad' in data:
                user.IdDiscapacidad = data.get('IdDiscapacidad')
                
            db.session.commit()
            
            user_schema = UserSchema()
            return user_schema.dump(user)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario por su ID"""
        user = User.query.get(user_id)
        if not user:
            return False
            
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios"""
        users = User.query.all()
        user_schema = UserSchema(many=True)
        return user_schema.dump(users)