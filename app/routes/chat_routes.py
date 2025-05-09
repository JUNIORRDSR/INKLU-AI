from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
import logging
import asyncio
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chat_service.log")
    ]
)
logger = logging.getLogger("ChatAPI")

# Crear Blueprint para rutas de chat
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
async def process_message():
    """
    Procesa un mensaje individual enviado por el usuario.

    Body: { "message": "texto del mensaje" }
    Respuesta:
        - 200: Resultado del procesamiento
        - 400: Error en los datos enviados
        - 500: Error del servidor
    """
    try:
        data = request.get_json()
        message = data.get('message')
        if not message or not isinstance(message, str):
            logger.error("Falta o es inválido el campo 'message'")
            return jsonify({"status": "error", "message": "El campo 'message' es requerido y debe ser una cadena"}), 400

        logger.info(f"Procesando mensaje: {message[:50]}...")
        result = await ChatService.process_message(message)
        logger.info(f"Resultado: {result.get('status')}")
        return jsonify(result), 200 if result["status"] == "success" else 500

    except Exception as e:
        logger.error(f"Error en /chat: {str(e)}")
        return jsonify({"status": "error", "message": f"Error del servidor: {str(e)}"}), 500

@chat_bp.route('/chat/batch', methods=['POST'])
async def process_batch():
    """
    Procesa un lote de mensajes enviados por el usuario.

    Body: { "messages": ["mensaje1", "mensaje2", ...] }
    Respuesta:
        - 200: Lista de resultados
        - 400: Error en los datos enviados
        - 500: Error del servidor
    """
    try:
        data = request.get_json()
        messages = data.get('messages')
        if not messages or not isinstance(messages, list) or not all(isinstance(m, str) for m in messages):
            logger.error("Falta o es inválido el campo 'messages'")
            return jsonify({"status": "error", "message": "El campo 'messages' es requerido y debe ser una lista de cadenas"}), 400

        logger.info(f"Procesando lote de {len(messages)} mensajes")
        results = await ChatService.process_batch(messages)
        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Error en /chat/batch: {str(e)}")
        return jsonify({"status": "error", "message": f"Error del servidor: {str(e)}"}), 500

@chat_bp.route('/chat/file', methods=['POST'])
async def process_file():
    """
    Procesa mensajes desde un archivo de texto subido (un mensaje por línea).

    Form-data: { "file": archivo.txt }
    Respuesta:
        - 200: Lista de resultados
        - 400: Error en el archivo enviado
        - 500: Error del servidor
    """
    try:
        if 'file' not in request.files:
            logger.error("No se proporcionó archivo")
            return jsonify({"status": "error", "message": "Se requiere un archivo"}), 400

        file = request.files['file']
        if not file.filename.endswith('.txt'):
            logger.error("El archivo debe ser .txt")
            return jsonify({"status": "error", "message": "El archivo debe ser de tipo .txt"}), 400

        # Guardar archivo temporalmente
        temp_path = os.path.join("temp", file.filename)
        os.makedirs("temp", exist_ok=True)
        file.save(temp_path)

        logger.info(f"Procesando archivo: {temp_path}")
        results = await ChatService.process_from_file(temp_path)

        # Opcional: Guardar resultados en un archivo JSON
        output_path = os.path.join("temp", f"results_{file.filename}.json")
        save_result = await ChatService.save_results(results, output_path)

        # Limpiar archivo temporal
        try:
            os.remove(temp_path)
        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo temporal: {str(e)}")

        response = {
            "status": "success",
            "results": results,
            "save_result": save_result
        }
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error en /chat/file: {str(e)}")
        return jsonify({"status": "error", "message": f"Error del servidor: {str(e)}"}), 500