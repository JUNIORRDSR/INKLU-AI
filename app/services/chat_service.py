import os
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from app.utils.agents.main import procesar_solicitud, CONFIG

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chat_service.log")
    ]
)
logger = logging.getLogger("ChatService")

class ChatService:
    """Servicio para procesar solicitudes de chat hacia el orquestador de agentes."""

    @staticmethod
    async def process_message(message: str) -> Dict[str, Any]:
        """Procesa un único mensaje y devuelve el resultado.

        Args:
            message (str): Texto del usuario a procesar.

        Returns:
            Dict[str, Any]: Resultado con estado y mensaje.
        """
        logger.info(f"Procesando mensaje: {message[:50]}...")
        try:
            result = await procesar_solicitud(message)
            logger.info(f"Mensaje procesado con éxito: {result.get('status')}")
            return result
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {str(e)}")
            return {"status": "error", "message": f"Error al procesar mensaje: {str(e)}"}

    @staticmethod
    async def process_batch(messages: List[str]) -> List[Dict[str, Any]]:
        """Procesa un lote de mensajes de forma asíncrona.

        Args:
            messages (List[str]): Lista de mensajes a procesar.

        Returns:
            List[Dict[str, Any]]: Lista de resultados.
        """
        logger.info(f"Procesando lote de {len(messages)} mensajes")
        try:
            tasks = [procesar_solicitud(message) for message in messages]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            processed = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error procesando mensaje {i}: {str(result)}")
                    processed.append({
                        "status": "error",
                        "message": f"Error: {str(result)}",
                        "original_message": messages[i]
                    })
                else:
                    processed.append(result)
            return processed
        except Exception as e:
            logger.error(f"Error al procesar lote: {str(e)}")
            return [{"status": "error", "message": f"Error al procesar lote: {str(e)}"}]

    @staticmethod
    async def process_from_file(file_path: str) -> List[Dict[str, Any]]:
        """Procesa mensajes desde un archivo de texto (un mensaje por línea).

        Args:
            file_path (str): Ruta al archivo de texto.

        Returns:
            List[Dict[str, Any]]: Lista de resultados.
        """
        logger.info(f"Leyendo mensajes desde {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]
            return await ChatService.process_batch(messages)
        except Exception as e:
            logger.error(f"Error al procesar archivo: {str(e)}")
            return [{"status": "error", "message": f"Error al procesar archivo: {str(e)}"}]

    @staticmethod
    async def save_results(results: List[Dict[str, Any]], output_path: str) -> Dict[str, Any]:
        """Guarda los resultados en un archivo JSON.

        Args:
            results (List[Dict[str, Any]]): Resultados a guardar.
            output_path (str): Ruta del archivo de salida.

        Returns:
            Dict[str, Any]: Estado del guardado.
        """
        logger.info(f"Guardando resultados en {output_path}")
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info("Resultados guardados con éxito")
            return {"status": "success", "message": f"Resultados guardados en {output_path}"}
        except Exception as e:
            logger.error(f"Error al guardar resultados: {str(e)}")
            return {"status": "error", "message": f"Error al guardar resultados: {str(e)}"}