from flask import Blueprint, request, jsonify
from app.services.indicator_service import IndicatorService
from flask_jwt_extended import jwt_required

indicators_bp = Blueprint('indicators', __name__)

@indicators_bp.route('/indicators', methods=['POST'])
def create_indicator():
    try:
        json_data = request.get_json()
        created_indicator = IndicatorService.create_indicator(json_data)
        return jsonify(created_indicator), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@indicators_bp.route('/indicators', methods=['GET'])
def get_indicators():
    try:
        indicators = IndicatorService.get_all_indicators()
        return jsonify(indicators), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@indicators_bp.route('/indicators/<int:id>', methods=['GET'])
def get_indicator(id):
    try:
        indicator = IndicatorService.get_indicator(id)
        if not indicator:
            return jsonify({'error': 'Indicador no encontrado'}), 404
        return jsonify(indicator), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@indicators_bp.route('/indicators/<int:id>', methods=['PUT'])
def update_indicator(id):
    try:
        json_data = request.get_json()
        updated_indicator = IndicatorService.update_indicator(id, json_data)
        if not updated_indicator:
            return jsonify({'error': 'Indicador no encontrado'}), 404
        return jsonify(updated_indicator), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@indicators_bp.route('/indicators/<int:id>', methods=['DELETE'])
def delete_indicator(id):
    try:
        success = IndicatorService.delete_indicator(id)
        if not success:
            return jsonify({'error': 'Indicador no encontrado'}), 404
        return jsonify({'message': 'Indicador eliminado correctamente'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500