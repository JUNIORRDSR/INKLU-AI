import os
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from app.utils.agents.main import procesar_solicitud

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
            # Comprobar si procesar_solicitud es asíncrona o sincrónica
            import inspect
            if inspect.iscoroutinefunction(procesar_solicitud):
                # Si es asíncrona, usar await
                result = await procesar_solicitud(message)
            else:
                # Si es sincrónica, llamarla normalmente
                result = procesar_solicitud(message)
            
            # Verificar si el resultado es None y manejarlo adecuadamente
            if result is None:
                logger.warning("La función procesar_solicitud devolvió None")
                result = {
                    "status": "success",
                    "message": "Lo siento, no pude generar una respuesta. Por favor, intenta con otra pregunta.",
                    "input": message
                }
                
            logger.info(f"Mensaje procesado con éxito: {result}")
            return result
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {str(e)}")
            # Creamos una respuesta predeterminada
            return {
                "status": "error", 
                "message": "Lo siento, tuve problemas procesando tu solicitud. Por favor, intenta con otra pregunta.",
                "error_details": str(e),
                "input": message
            }

    @staticmethod
    async def process_batch(messages: List[str]) -> List[Dict[str, Any]]:
        """Procesa un lote de mensajes de forma asíncrona.

        Args:
            messages (List[str]): Lista de mensajes a procesar.

        Returns:
            List[Dict[str, Any]]: Lista de resultados.
        """
        logger.info(f"Procesando lote de {len(messages)} mensajes")
        
        # Comprobar si procesar_solicitud es asíncrona o sincrónica
        import inspect
        is_async = inspect.iscoroutinefunction(procesar_solicitud)
        
        processed = []
        for i, message in enumerate(messages):
            try:
                # Procesar mensaje según si la función es async o no
                if is_async:
                    result = await procesar_solicitud(message)
                else:
                    result = procesar_solicitud(message)
                
                # Verificar si el resultado es None
                if result is None:
                    logger.warning(f"Mensaje {i}: procesar_solicitud devolvió None")
                    result = {
                        "status": "success",
                        "message": "Lo siento, no pude generar una respuesta para esta consulta.",
                        "input": message
                    }
                
                processed.append(result)
            except Exception as e:
                logger.error(f"Error procesando mensaje {i}: {str(e)}")
                processed.append({
                    "status": "error",
                    "message": "Lo siento, tuve un problema procesando esta solicitud.",
                    "error_details": str(e),
                    "input": message
                })
        
        return processed

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