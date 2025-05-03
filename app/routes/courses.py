from flask import Blueprint, request, jsonify
from app.services.course_service import CourseService
from flask_jwt_extended import jwt_required

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    try:
        data = request.get_json()
        new_course = CourseService.create_course(data)
        return jsonify(new_course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses = CourseService.get_all_courses()
        return jsonify(courses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@courses_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        course = CourseService.get_course(course_id)
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        return jsonify(course), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@courses_bp.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    try:
        data = request.get_json()
        updated_course = CourseService.update_course(course_id, data)
        if not updated_course:
            return jsonify({"error": "Curso no encontrado"}), 404
        return jsonify(updated_course), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@courses_bp.route('/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    try:
        success = CourseService.delete_course(course_id)
        if not success:
            return jsonify({"error": "Curso no encontrado"}), 404
        return jsonify({"message": "Curso eliminado correctamente"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500