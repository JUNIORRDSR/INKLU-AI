import os
import asyncio
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from creador_cv import creador_pdf
from AgenteBusqueda import buscar_oportunidades

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger("SuperOrquestador")

# Cargar variables de entorno
load_dotenv()

# Configuración centralizada
CONFIG = {
    "deepseek_model": {
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
    },
}

# Inicializar modelo DeepSeek
llm = ChatDeepSeek(
    model=CONFIG["deepseek_model"]["model"],
    api_key=CONFIG["deepseek_model"]["api_key"],
)

# Herramientas como funciones adaptadas para LangChain
@tool
async def generar_cv(input_text: str) -> Dict[str, Any]:
    """Genera un CV en PDF a partir de datos personales.

    Args:
        input_text (str): Texto con información personal.

    Returns:
        Dict[str, Any]: Resultado del proceso de generación.
    """
    logger.info("Herramienta GenerarCV: Iniciando generación de CV")
    result = await creador_pdf(input_text)
    logger.info(f"Herramienta GenerarCV: Resultado: {result}")
    return result

@tool
async def buscar_empleos(consulta: str) -> Dict[str, Any]:
    """Busca oportunidades laborales inclusivas.

    Args:
        consulta (str): Consulta de búsqueda de empleo.

    Returns:
        Dict[str, Any]: Resultados de la búsqueda.
    """
    logger.info("Herramienta BuscarEmpleos: Iniciando búsqueda de empleos")
    result = await buscar_oportunidades(consulta)
    logger.info(f"Herramienta BuscarEmpleos: Resultado: {result}")
    return result

# Configurar agente orquestador
tools = [generar_cv, buscar_empleos]
react_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SystemMessage(content="""Eres un super orquestador responsable de enrutar las solicitudes del usuario a la herramienta adecuada. Tu única tarea es elegir entre dos herramientas según el contenido del mensaje:

- Herramienta "generar_cv": Úsala si el usuario proporciona información personal para crear una hoja de vida (ej. nombre, habilidades, experiencia laboral, educación, correo, discapacidad).
- Herramienta "buscar_empleos": Úsala si el usuario expresa interés en encontrar trabajo, buscar oportunidades laborales, o solicita recomendaciones de empleo.

📌 Si el mensaje no encaja en ninguna de estas categorías, responde exactamente:
"Lo siento, en este momento no tengo acceso a esa función. Solo puedo ayudarte a crear tu hoja de vida o a buscar oportunidades laborales. ¡Gracias por entender!"

🔒 No generes respuestas personalizadas fuera de estas funciones. Usa solo las herramientas proporcionadas."""),
)

async def procesar_solicitud(input_text: str) -> Dict[str, Any]:
    """Procesa la solicitud del usuario y devuelve el resultado.

    Args:
        input_text (str): Mensaje del usuario.

    Returns:
        Dict[str, Any]: Resultado del procesamiento.
    """
    logger.info(f"Orquestador: Procesando solicitud: {input_text}")
    try:
        # Verificar API key
        if not CONFIG["deepseek_model"]["api_key"]:
            logger.error("Orquestador: DEEPSEEK_API_KEY no configurada")
            return {"status": "error", "message": "DEEPSEEK_API_KEY no configurada en .env"}

        message = HumanMessage(content=input_text)
        result = None

        # Procesar con el agente
        async for step in react_agent.astream({"messages": message}, stream_mode="values"):
            result = step["messages"][-1].content
            logger.info(f"Orquestador: Resultado parcial: {result}")
            if result != input_text:
                break

        if not result:
            logger.error("Orquestador: No se obtuvo resultado válido")
            return {"status": "error", "message": "No se procesó la solicitud correctamente."}

        # Manejar respuesta
        if isinstance(result, str) and "Lo siento, en este momento no tengo acceso" in result:
            return {"status": "error", "message": result}
        
        # Si el resultado es un diccionario (de las herramientas)
        if isinstance(result, dict):
            return result

        # Convertir resultado a diccionario si es necesario
        return {"status": "success", "message": result}

    except Exception as e:
        logger.error(f"Orquestador: Error: {str(e)}")
        return {"status": "error", "message": f"Error: {str(e)}"}

if __name__ == "__main__":
    input_text = input("Escribe tu mensaje (ej. 'Crear CV con nombre Juan Pérez' o 'Buscar empleos en Bogotá'): ")
    if not input_text:
        input_text = "Buscar empleos inclusivos en Colombia para discapacidad física"
    result = asyncio.run(procesar_solicitud(input_text))
    print(f"\n🔍 Resultado:\n{result['message']}")