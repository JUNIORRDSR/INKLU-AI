from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user = UserService.create_user(data)
        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Obtener usuario por correo electrónico
        user = UserService.get_user_by_email(data.get('Correo'))
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        # Verificar contraseña
        from app.models.user import User
        db_user = User.query.get(user['IdUsuario'])
        if not db_user or not db_user.check_password(data.get('Contrasena')):
            return jsonify({"error": "Credenciales inválidas"}), 401
            
        # Crear token JWT
        access_token = create_access_token(identity=user['IdUsuario'])
        return jsonify({"token": access_token, "user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = UserService.get_user(user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Con JWT, el logout se maneja del lado del cliente eliminando el token
    return jsonify({"message": "Sesión cerrada correctamente"}), 200