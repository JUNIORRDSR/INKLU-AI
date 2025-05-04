from flask import Blueprint, request, jsonify
from app.services.application_service import ApplicationService
from flask_jwt_extended import jwt_required, get_jwt_identity

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/applications', methods=['POST'])
@jwt_required()
def create_application():
    try:
        json_data = request.get_json()
        # Opcionalmente podemos asignar el usuario actual automáticamente
        # json_data['IdUsuario'] = get_jwt_identity()
        application = ApplicationService.create_application(json_data)
        return jsonify(application), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@applications_bp.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    try:
        application = ApplicationService.get_application(application_id)
        if not application:
            return jsonify({"error": "Postulación no encontrada"}), 404
        return jsonify(application), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@applications_bp.route('/applications/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_application(application_id):
    try:
        json_data = request.get_json()
        updated_application = ApplicationService.update_application(application_id, json_data)
        if not updated_application:
            return jsonify({"error": "Postulación no encontrada"}), 404
        return jsonify(updated_application), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@applications_bp.route('/applications/<int:application_id>', methods=['DELETE'])
@jwt_required()
def delete_application(application_id):
    try:
        success = ApplicationService.delete_application(application_id)
        if not success:
            return jsonify({"error": "Postulación no encontrada"}), 404
        return jsonify({"message": "Postulación eliminada correctamente"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@applications_bp.route('/applications/user/<int:user_id>', methods=['GET'])
def get_user_applications(user_id):
    try:
        applications = ApplicationService.get_applications_by_user(user_id)
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@applications_bp.route('/applications/job/<int:job_id>', methods=['GET'])
def get_job_applications(job_id):
    try:
        applications = ApplicationService.get_applications_by_job(job_id)
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500