from flask import Blueprint, request, jsonify
from app.schemas.user_schema import UserSchema
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        created_user = UserService.create_user(data)
        return jsonify(created_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserService.get_user(user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        data = request.get_json()
        updated_user = UserService.update_user(user_id, data)
        if not updated_user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        success = UserService.delete_user(user_id)
        if not success:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({'message': 'Usuario eliminado correctamente'}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    try:
        users = UserService.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500