from flask import Blueprint, request, jsonify
from app.services.enrollment_service import EnrollmentService
from flask_jwt_extended import jwt_required, get_jwt_identity

enrollments_bp = Blueprint('enrollments', __name__)

@enrollments_bp.route('/enrollments', methods=['POST'])
@jwt_required()
def create_enrollment():
    try:
        data = request.get_json()
        # Opcionalmente podemos asignar el usuario actual automáticamente
        # data['id_usuario'] = get_jwt_identity()
        enrollment = EnrollmentService.create_enrollment(data)
        return jsonify(enrollment), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@enrollments_bp.route('/enrollments/course/<int:course_id>/user/<int:user_id>', methods=['GET'])
def get_enrollment(course_id, user_id):
    try:
        enrollment = EnrollmentService.get_enrollment(course_id, user_id)
        if not enrollment:
            return jsonify({"error": "Inscripción no encontrada"}), 404
        return jsonify(enrollment), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrollments_bp.route('/enrollments/course/<int:course_id>/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_enrollment(course_id, user_id):
    try:
        success = EnrollmentService.delete_enrollment(course_id, user_id)
        if not success:
            return jsonify({"error": "Inscripción no encontrada"}), 404
        return jsonify({"message": "Inscripción eliminada correctamente"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrollments_bp.route('/enrollments/user/<int:user_id>', methods=['GET'])
def get_user_enrollments(user_id):
    try:
        enrollments = EnrollmentService.get_enrollments_by_user(user_id)
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrollments_bp.route('/enrollments/course/<int:course_id>', methods=['GET'])
def get_course_enrollments(course_id):
    try:
        enrollments = EnrollmentService.get_enrollments_by_course(course_id)
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrollments_bp.route('/enrollments', methods=['GET'])
@jwt_required()
def get_all_enrollments():
    try:
        enrollments = EnrollmentService.get_all_enrollments()
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500