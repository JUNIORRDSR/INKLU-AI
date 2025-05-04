from flask import Blueprint, request, jsonify
from app.services.disability_type_service import DisabilityTypeService
from flask_jwt_extended import jwt_required

disabilities_bp = Blueprint('disabilities', __name__)

@disabilities_bp.route('/disabilities', methods=['POST'])
@jwt_required()
def create_disability_type():
    try:
        json_data = request.get_json()
        created_disability_type = DisabilityTypeService.create_disability_type(json_data)
        return jsonify(created_disability_type), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@disabilities_bp.route('/disabilities', methods=['GET'])
def get_disability_types():
    try:
        disability_types = DisabilityTypeService.get_all_disability_types()
        return jsonify(disability_types), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@disabilities_bp.route('/disabilities/<int:id>', methods=['GET'])
def get_disability_type(id):
    try:
        disability_type = DisabilityTypeService.get_disability_type(id)
        if not disability_type:
            return jsonify({"error": "Tipo de discapacidad no encontrado"}), 404
        return jsonify(disability_type), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@disabilities_bp.route('/disabilities/<int:id>', methods=['PUT'])
@jwt_required()
def update_disability_type(id):
    try:
        json_data = request.get_json()
        updated_disability_type = DisabilityTypeService.update_disability_type(id, json_data)
        if not updated_disability_type:
            return jsonify({"error": "Tipo de discapacidad no encontrado"}), 404
        return jsonify(updated_disability_type), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@disabilities_bp.route('/disabilities/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_disability_type(id):
    try:
        success = DisabilityTypeService.delete_disability_type(id)
        if not success:
            return jsonify({"error": "Tipo de discapacidad no encontrado"}), 404
        return jsonify({"message": "Tipo de discapacidad eliminado correctamente"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500