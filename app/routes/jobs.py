from flask import Blueprint, request, jsonify
from app.services.job_service import JobService
from flask_jwt_extended import jwt_required

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    try:
        json_data = request.get_json()
        job = JobService.create_job(json_data)
        return jsonify(job), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = JobService.get_all_jobs()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = JobService.get_job(job_id)
        if not job:
            return jsonify({"error": "Vacante no encontrada"}), 404
        return jsonify(job), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jobs_bp.route('/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    try:
        json_data = request.get_json()
        job = JobService.update_job(job_id, json_data)
        if not job:
            return jsonify({"error": "Vacante no encontrada"}), 404
        return jsonify(job), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    try:
        success = JobService.delete_job(job_id)
        if not success:
            return jsonify({"error": "Vacante no encontrada"}), 404
        return jsonify({"message": "Vacante eliminada correctamente"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500