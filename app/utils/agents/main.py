import os
import asyncio
import logging
import re
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from .creador_cv import creador_pdf
from .AgenteBusqueda import buscar_oportunidades

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("orquestador.log")]
)
logger = logging.getLogger("SuperOrquestador")

# Cargar variables de entorno
load_dotenv()

# Configuración centralizada
CONFIG = {
    "deepseek_model": {
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "temperature": 0.7,
        "max_tokens": 1000,
    },
}

# Inicializar modelo DeepSeek
llm = ChatDeepSeek(
    model=CONFIG["deepseek_model"]["model"],
    api_key=CONFIG["deepseek_model"]["api_key"],
    temperature=CONFIG["deepseek_model"]["temperature"],
    max_tokens=CONFIG["deepseek_model"]["max_tokens"],
)

# Herramientas
@tool
async def generar_cv(input_text: str) -> Dict[str, Any]:
    """Genera un CV en PDF a partir de datos personales."""
    logger.info("Herramienta GenerarCV: Iniciando")
    result = await creador_pdf(input_text)
    logger.info(f"Herramienta GenerarCV: Resultado: {result}")
    return result

@tool
async def buscar_empleos(consulta: str) -> Dict[str, Any]:
    """Busca oportunidades laborales inclusivas."""
    logger.info("Herramienta BuscarEmpleos: Iniciando")
    result = await buscar_oportunidades(consulta)
    logger.info(f"Herramienta BuscarEmpleos: Resultado: {result}")
    return result

# Configurar agente orquestador
tools = [generar_cv, buscar_empleos]
react_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SystemMessage(content="""Eres SuperOrquestador V2. Analiza el mensaje y elige una herramienta:

- **generar_cv**: Si el mensaje contiene datos personales (nombre, habilidades, experiencia, educación, correo, discapacidad).
- **buscar_empleos**: Si el mensaje menciona búsqueda de trabajo, oportunidades laborales, o recomendaciones de empleo.

Si no encaja, responde exactamente:
"Lo siento, en este momento no tengo acceso a esa función. Solo puedo ayudarte a crear tu hoja de vida o a buscar oportunidades laborales. ¡Gracias por entender!"

No generes respuestas personalizadas fuera de estas funciones."""),
)

def clean_input(input_text: str) -> str:
    """Limpia el texto de entrada eliminando saludos y frases conversacionales."""
    logger.info(f"Orquestador: Limpiando entrada: {input_text}")
    greetings = [
        r"\b(hola|buenos días|buenas tardes|buenas noches|¿cómo estás\??)\b",
        r"\b(hi|hello|good morning|good afternoon|good evening|how are you\??)\b",
    ]
    cleaned_text = input_text
    for pattern in greetings:
        cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    logger.info(f"Orquestador: Texto limpio: {cleaned_text}")
    return cleaned_text

async def procesar_solicitud(input_text: str) -> Dict[str, Any]:
    """Procesa la solicitud del usuario siguiendo el flujo de SuperOrquestador V2."""
    logger.info(f"Orquestador: Procesando solicitud: {input_text}")

    # Fase 1: Recepción y limpieza
    cleaned_input = clean_input(input_text)
    if not cleaned_input:
        logger.warning("Orquestador: Entrada vacía después de limpieza")
        return {
            "status": "error",
            "message": "Por favor, proporciona una solicitud válida.",
            "result_formatted": (
                "🔎 Resultado:\n"
                "Por favor, proporciona una solicitud válida.\n\n"
                "—"
            ),
        }

    # Fase 2: Análisis de requerimientos (delegado al agente)

    # Fase 3: Verificación de herramienta
    if not CONFIG["deepseek_model"]["api_key"]:
        logger.error("Orquestador: DEEPSEEK_API_KEY no configurada")
        return {
            "status": "error",
            "message": "DEEPSEEK_API_KEY no configurada en .env.",
            "result_formatted": (
                "🔎 Resultado:\n"
                "Error: DEEPSEEK_API_KEY no configurada en .env.\n\n"
                "—"
            ),
        }

    # Fase 4: Ejecución puntual
    try:
        message = HumanMessage(content=cleaned_input)
        result = None
        async for step in react_agent.astream(
            {"messages": message}, stream_mode="values"
        ):
            result = step["messages"][-1].content
            logger.info(f"Orquestador: Resultado parcial: {result}")
            if result != cleaned_input:
                break

        # Fase 5: Procesamiento de salida
        if not result or result.strip() == "":
            logger.error("Orquestador: Respuesta vacía o no válida")
            if "trabajo" in cleaned_input.lower() and "discapacidad" in cleaned_input.lower():
                result = await _fallback_discapacidad_empleos(cleaned_input)
            else:
                result = {
                    "status": "error",
                    "message": "No se obtuvo información válida. Por favor, intenta de nuevo.",
                }

        # Manejar respuesta del agente
        if isinstance(result, str):
            if "Lo siento, en este momento no tengo acceso" in result:
                logger.info("Orquestador: Solicitud no coincide con herramientas")
                return {
                    "status": "error",
                    "message": result,
                    "result_formatted": (
                        "🔎 Resultado:\n"
                        f"{result}\n\n"
                        "—"
                    ),
                }
            try:
                import json
                parsed_result = json.loads(result)
                if isinstance(parsed_result, dict):
                    result = parsed_result
            except json.JSONDecodeError:
                result = {"status": "success", "message": result}

        if isinstance(result, dict) and "status" in result:
            # Fase 6: Formateo de respuesta final
            status = result["status"]
            message = result["message"]
            tips = result.get("tips", "")
            result_formatted = (
                "🔎 Resultado:\n"
                f"{message}\n\n"
            )
            if tips:
                result_formatted += f"💡 Consejos:\n{tips}\n\n"
            result_formatted += "—"
            return {
                "status": status,
                "message": message,
                "tips": tips,
                "result_formatted": result_formatted,
            }

        logger.warning(f"Orquestador: Resultado inesperado: {result}")
        return {
            "status": "success",
            "message": str(result),
            "result_formatted": (
                "🔎 Resultado:\n"
                f"{str(result)}\n\n"
                "—"
            ),
        }

    except Exception as e:
        logger.error(f"Orquestador: Error interno: {str(e)}")
        if "trabajo" in cleaned_input.lower() and "discapacidad" in cleaned_input.lower():
            result = await _fallback_discapacidad_empleos(cleaned_input)
            return {
                "status": result["status"],
                "message": result["message"],
                "tips": result.get("tips", ""),
                "result_formatted": (
                    "🔎 Resultado:\n"
                    f"{result['message']}\n\n"
                    f"💡 Consejos:\n{result.get('tips', '')}\n\n"
                    "—"
                ),
            }
        return {
            "status": "error",
            "message": "Error interno, vuelve a intentarlo más tarde.",
            "result_formatted": (
                "🔎 Resultado:\n"
                "Error interno, vuelve a intentarlo más tarde.\n\n"
                "—"
            ),
        }

async def _fallback_discapacidad_empleos(consulta: str) -> Dict[str, Any]:
    """Respuesta de respaldo para empleos con discapacidad."""
    logger.info("Orquestador: Usando respuesta de respaldo")
    response = (
        "No se pudo obtener información específica, pero aquí tienes recursos útiles para buscar oportunidades laborales inclusivas en Colombia:\n\n"
        "| **Recurso** | **Descripción** | **Contacto/URL** |\n"
        "|-------------|-----------------|------------------|\n"
        "| **Centro de Oportunidades (Barranquilla)** | Orientación laboral para personas con discapacidad. | inclusionlaboraldiscapacidad@barranquilla.gov.co |\n"
        "| **INCI** | Portal de inclusión laboral y talleres (viernes 1:00-5:00 p.m.). | https://www.inci.gov.co/inclusion-laboral |\n"
        "| **Computrabajo** | Ofertas como auxiliar administrativo (~$1,423,500/mes). | https://www.computrabajo.com.co/ |\n"
        "| **Magneto** | 2,554 cupos, incluyendo asesores comerciales (~$2,400,000-$3,000,000). | https://www.magneto365.com/ |\n\n"
        "**Roles recomendados**: Teleoperador, recepcionista, grabador de datos (usando JAWS/NVDA)."
    )
    tips = (
        "- Contacta al Centro de Oportunidades para orientación personalizada.\n"
        "- Regístrate en INCI para vacantes actualizadas.\n"
        "- Usa filtros de 'inclusión' en portales como Computrabajo."
    )
    if "barranquilla" in consulta.lower():
        response = response.replace("en Colombia", "en Barranquilla")
    return {
        "status": "success",
        "message": response,
        "tips": tips,
    }

if __name__ == "__main__":
    input_text = input("Escribe tu mensaje: ")
    if not input_text:
        input_text = "Buscar empleos inclusivos en Colombia para discapacidad física"
    result = asyncio.run(procesar_solicitud(input_text))
    print(result["result_formatted"])