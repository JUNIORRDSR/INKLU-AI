import os
import asyncio
import json
import logging
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger("JobSearchAgent")

# Cargar variables de entorno
load_dotenv()

# Configuración centralizada
CONFIG = {
    "deepseek_model": {
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
    },
    "adzuna": {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_APP_KEY"),
    },
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "cse_id": os.getenv("GOOGLE_CSE_ID"),
    },
}

# Inicializar modelo DeepSeek
llm = ChatDeepSeek(
    model=CONFIG["deepseek_model"]["model"],
    api_key=CONFIG["deepseek_model"]["api_key"],
)
orquestador = ChatDeepSeek(
    model=CONFIG["deepseek_model"]["model"],
    api_key=CONFIG["deepseek_model"]["api_key"],
)

# Modelo para parámetros de búsqueda
class BusquedaParams(BaseModel):
    keywords: List[str] = Field(default=["discapacidad"], description="Palabras clave de búsqueda")
    location: Optional[str] = Field(None, description="Ubicación (ej: Colombia, Bogotá)")
    companies: Optional[List[str]] = Field(None, description="Empresas específicas (ej: Bancolombia, Google)")

@tool
async def buscar_empleos(params: BusquedaParams) -> str:
    """Busca empleos inclusivos usando la API de Adzuna.

    Args:
        params (BusquedaParams): Parámetros de búsqueda.

    Returns:
        str: Resultados de empleos en formato texto.
    """
    logger.info("Agente BuscarEmpleos: Iniciando búsqueda en Adzuna")
    base_url = "https://api.adzuna.com/v1/api/jobs"

    # Verificar configuración de Adzuna
    if not CONFIG["adzuna"]["app_id"] or not CONFIG["adzuna"]["app_key"]:
        logger.error("Agente BuscarEmpleos: Claves de Adzuna no configuradas")
        return """⚠️ API de Adzuna no configurada. Agrega en .env:
ADZUNA_APP_ID=tu_id
ADZUNA_APP_KEY=tu_clave
Consulta https://developer.adzuna.com/ para obtener claves."""

    # Construir consulta
    query = " ".join(params.keywords) + " inclusivo"
    if params.companies:
        query += " " + " ".join(params.companies)

    # Parámetros de la API
    api_params = {
        "app_id": CONFIG["adzuna"]["app_id"],
        "app_key": CONFIG["adzuna"]["app_key"],
        "what": query,
        "results_per_page": 5,
    }
    if params.location:
        api_params["where"] = params.location

    try:
        response = requests.get(f"{base_url}/search/1", params=api_params)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            logger.info("Agente BuscarEmpleos: No se encontraron empleos")
            return "No se encontraron empleos. Intenta con otras palabras clave o ubicación."

        results = []
        for job in data["results"]:
            title = job.get("title", "Sin título")
            company = job.get("company", {}).get("display_name", "Desconocida")
            location = job.get("location", {}).get("display_name", "No especificada")
            description = job.get("description", "Sin descripción")[:200] + "..."
            url = job.get("redirect_url", "")

            results.append(f"🏢 {company}")
            results.append(f"  - Vacante: {title}")
            results.append(f"  - Ubicación: {location}")
            results.append(f"  - Descripción: {description}")
            results.append(f"  - Enlace: {url}")
            results.append("")

        logger.info("Agente BuscarEmpleos: Empleos encontrados")
        return "\n".join(results)

    except requests.RequestException as e:
        logger.error(f"Agente BuscarEmpleos: Error en API Adzuna: {str(e)}")
        return f"Error en la búsqueda: {str(e)}\n\nSugerencia: Intenta con otra ubicación o palabras clave."

@tool
async def google_search_empleos(query: str) -> str:
    """Realiza búsqueda de empleos inclusivos en la web usando Google Custom Search.

    Args:
        query (str): Consulta de búsqueda.

    Returns:
        str: Resultados en formato JSON.
    """
    logger.info("Agente GoogleSearch: Iniciando búsqueda en Google")
    base_url = "https://www.googleapis.com/customsearch/v1"

    # Modificar consulta para empleos inclusivos
    modified_query = f"{query} empleo discapacidad inclusivo"

    # Verificar configuración
    if not CONFIG["google"]["api_key"] or not CONFIG["google"]["cse_id"]:
        logger.error("Agente GoogleSearch: Claves de Google no configuradas")
        return """⚠️ API de Google no configurada. Agrega en .env:
GOOGLE_API_KEY=tu_clave
GOOGLE_CSE_ID=tu_id
Consulta https://developers.google.com/custom-search/v1/introduction para obtener claves.

Recursos alternativos:
- Incluyeme: https://www.incluyeme.com/colombia/
- Servicio Público de Empleo: https://www.serviciodeempleo.gov.co/
- Fundación Saldarriaga Concha: https://www.saldarriagaconcha.org/"""

    params = {
        "q": modified_query,
        "key": CONFIG["google"]["api_key"],
        "cx": CONFIG["google"]["cse_id"],
        "num": 5,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" not in data:
            logger.info("Agente GoogleSearch: No se encontraron resultados")
            return "No se encontraron resultados web."

        results = []
        for item in data["items"]:
            results.append({
                "title": item.get("title", "Sin título"),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "Sin descripción"),
            })

        logger.info("Agente GoogleSearch: Resultados web obtenidos")
        return json.dumps(results, ensure_ascii=False, indent=2)

    except requests.RequestException as e:
        logger.error(f"Agente GoogleSearch: Error en API Google: {str(e)}")
        return f"Error en la búsqueda web: {str(e)}\n\nRecursos alternativos: Incluyeme, Servicio Público de Empleo."

# Configurar agente
tools = [buscar_empleos, google_search_empleos]
agent = create_react_agent(
    orquestador,
    tools,
    prompt=SystemMessage(content="""Eres un asistente especializado en buscar empleos inclusivos para personas con discapacidad.

Instrucciones:
1. Analiza la consulta para identificar:
   - Tipo de discapacidad (física, auditiva, visual, etc.)
   - Ubicación (país, ciudad)
   - Empresas específicas (si se mencionan)
   - Palabras clave (sector, tipo de trabajo)

2. Usa la herramienta buscar_empleos para buscar en la API de Adzuna:
   - Incluye el tipo de discapacidad y palabras clave en keywords
   - Usa la ubicación como location
   - Incluye empresas específicas en companies si se mencionan

3. Usa google_search_empleos para complementar con resultados web.

4. En la respuesta final:
   - Organiza los resultados por relevancia
   - Prioriza empleos inclusivos y accesibles
   - Incluye enlaces y descripciones claras
   - Proporciona consejos para la búsqueda (ej. contactar fundaciones, usar portales locales)

5. Si una API falla, usa la otra herramienta o proporciona recursos alternativos.
"""),
)

async def buscar_oportunidades(consulta: str) -> Dict[str, Any]:
    """Busca oportunidades laborales inclusivas.

    Args:
        consulta (str): Consulta del usuario.

    Returns:
        Dict[str, Any]: Resultados y estado.
    """
    logger.info(f"Agente Orquestador: Iniciando búsqueda para: {consulta}")
    try:
        # Verificar claves API
        if not CONFIG["deepseek_model"]["api_key"]:
            logger.error("Agente Orquestador: DEEPSEEK_API_KEY no configurada")
            return {"status": "error", "message": "DEEPSEEK_API_KEY no configurada en .env"}

        message = HumanMessage(content=consulta)
        results = []

        # Ejecutar agente
        async for step in agent.astream({"messages": message}, stream_mode="values"):
            result = step["messages"][-1].content
            logger.info(f"Agente Orquestador: Resultado parcial: {result}")
            if result != consulta:
                results.append(result)

        if not results:
            logger.error("Agente Orquestador: No se obtuvieron resultados")
            return {"status": "error", "message": "No se encontraron resultados."}

        # Combinar resultados
        final_result = "\n\n".join(results)
        logger.info("Agente Orquestador: Búsqueda completada")
        return {
            "status": "success",
            "message": final_result,
            "tips": """Consejos para tu búsqueda:
- Contacta fundaciones como Saldarriaga Concha o Best Buddies.
- Usa portales como Incluyeme.com o Servicio Público de Empleo.
- Revisa programas de inclusión en empresas como Bancolombia o Grupo Éxito."""
        }

    except Exception as e:
        logger.error(f"Agente Orquestador: Error: {str(e)}")
        return {
            "status": "error",
            "message": f"Error durante la búsqueda: {str(e)}",
            "tips": "Verifica tu conexión, claves API, o intenta con una consulta más específica."
        }

if __name__ == "__main__":
    consulta = input("Introduce tu búsqueda de empleo (ej: empleos para discapacidad auditiva en Bogotá): ")
    if not consulta:
        consulta = "Empleos inclusivos en Colombia para discapacidad física"
    result = asyncio.run(buscar_oportunidades(consulta))
    print(f"\n🔍 Resultados:\n{result['message']}\n\n💡 {result['tips']}")