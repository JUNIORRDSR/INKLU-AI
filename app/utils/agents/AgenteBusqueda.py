import os
import asyncio
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("job_search.log")]
)
logger = logging.getLogger("JobSearchAgent")

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
    temperature=CONFIG["deepseek_model"]["temperature"],
    max_tokens=CONFIG["deepseek_model"]["max_tokens"],
)
orquestador = ChatDeepSeek(
    model=CONFIG["deepseek_model"]["model"],
    api_key=CONFIG["deepseek_model"]["api_key"],
    temperature=CONFIG["deepseek_model"]["temperature"],
    max_tokens=CONFIG["deepseek_model"]["max_tokens"],
)

# Modelo para parámetros de búsqueda
class BusquedaParams(BaseModel):
    keywords: list[str] = Field(default=["discapacidad"], description="Palabras clave")
    location: str | None = Field(None, description="Ubicación")
    companies: list[str] | None = Field(None, description="Empresas específicas")

@tool
async def buscar_empleos(params: BusquedaParams) -> Dict[str, Any]:
    """Busca empleos inclusivos usando Adzuna."""
    logger.info("Tool BuscarEmpleos: Iniciando")
    base_url = "https://api.adzuna.com/v1/api/jobs"

    if not CONFIG["adzuna"]["app_id"] or not CONFIG["adzuna"]["app_key"]:
        logger.error("Tool BuscarEmpleos: Claves de Adzuna no configuradas")
        return {
            "status": "error",
            "message": (
                "⚠️ API de Adzuna no configurada. Agrega en .env:\n"
                "- ADZUNA_APP_ID=tu_id\n"
                "- ADZUNA_APP_KEY=tu_clave\n"
                "Consulta https://developer.adzuna.com/"
            ),
            "tips": (
                "- Regístrate en Adzuna para obtener claves.\n"
                "- Usa portales alternativos como Computrabajo."
            ),
        }

    query = " ".join(params.keywords) + " inclusivo"
    if params.companies:
        query += " " + " ".join(params.companies)

    api_params = {
        "app_id": CONFIG["adzuna"]["app_id"],
        "app_key": CONFIG["adzuna"]["app_key"],
        "what": query,
        "results_per_page": 5,
    }
    if params.location:
        api_params["where"] = params.location

    try:
        response = requests.get(f"{base_url}/search/1", params=api_params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            logger.info("Tool BuscarEmpleos: No se encontraron empleos")
            return {
                "status": "success",
                "message": (
                    "| **Vacante** | **Empresa** | **Ubicación** | **Enlace** |\n"
                    "|-------------|-------------|---------------|------------|\n"
                    "| No se encontraron empleos | - | - | - |\n\n"
                    "Intenta con otras palabras clave o ubicación."
                ),
                "tips": (
                    "- Especifica el tipo de discapacidad (ej. visual).\n"
                    "- Prueba ubicaciones más amplias (ej. Colombia)."
                ),
            }

        results = ["| **Vacante** | **Empresa** | **Ubicación** | **Enlace** |"]
        results.append("|-------------|-------------|---------------|------------|")
        for job in data["results"]:
            title = job.get("title", "Sin título")
            company = job.get("company", {}).get("display_name", "Desconocida")
            location = job.get("location", {}).get("display_name", "No especificada")
            url = job.get("redirect_url", "No disponible")
            results.append(f"| {title} | {company} | {location} | [Aplicar]({url}) |")
        results.append("")
        results.append("**Nota**: Verifica la accesibilidad de cada vacante.")

        logger.info("Tool BuscarEmpleos: Empleos encontrados")
        return {
            "status": "success",
            "message": "\n".join(results),
            "tips": (
                "- Contacta a la empresa para confirmar accesibilidad.\n"
                "- Usa INCI (https://www.inci.gov.co/) para más opciones."
            ),
        }

    except requests.RequestException as e:
        logger.error(f"Tool BuscarEmpleos: Error en Adzuna: {str(e)}")
        return {
            "status": "error",
            "message": f"No se pudo conectar con Adzuna: {str(e)}.",
            "tips": (
                "- Revisa tu conexión a internet.\n"
                "- Usa portales como Magneto o Incluyeme."
            ),
        }

@tool
async def google_search_empleos(query: str) -> Dict[str, Any]:
    """Busca empleos inclusivos en la web usando Google Custom Search."""
    logger.info("Tool GoogleSearch: Iniciando")
    base_url = "https://www.googleapis.com/customsearch/v1"

    modified_query = f"{query} empleo discapacidad inclusivo"

    if not CONFIG["google"]["api_key"] or not CONFIG["google"]["cse_id"]:
        logger.error("Tool GoogleSearch: Claves de Google no configuradas")
        return {
            "status": "error",
            "message": (
                "⚠️ API de Google no configurada. Agrega en .env:\n"
                "- GOOGLE_API_KEY=tu_clave\n"
                "- GOOGLE_CSE_ID=tu_id\n"
                "Consulta https://developers.google.com/custom-search/v1/introduction"
            ),
            "tips": (
                "- Visita Incluyeme: https://www.incluyeme.com/colombia/\n"
                "- Usa Servicio Público de Empleo: https://www.serviciodeempleo.gov.co/"
            ),
        }

    params = {
        "q": modified_query,
        "key": CONFIG["google"]["api_key"],
        "cx": CONFIG["google"]["cse_id"],
        "num": 5,
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "items" not in data:
            logger.info("Tool GoogleSearch: No se encontraron resultados")
            return {
                "status": "success",
                "message": (
                    "| **Título** | **Enlace** | **Descripción** |\n"
                    "|------------|------------|-----------------|\n"
                    "| No se encontraron resultados | - | - |\n\n"
                    "Intenta con una consulta más específica."
                ),
                "tips": (
                    "- Usa términos como 'empleo inclusivo Barranquilla'.\n"
                    "- Explora fundaciones como Saldarriaga Concha."
                ),
            }

        results = ["| **Título** | **Enlace** | **Descripción** |"]
        results.append("|------------|------------|-----------------|")
        for item in data["items"]:
            title = item.get("title", "Sin título")
            link = item.get("link", "No disponible")
            snippet = item.get("snippet", "Sin descripción")[:100] + "..."
            results.append(f"| {title} | [Ver]({link}) | {snippet} |")
        results.append("")
        results.append("**Nota**: Revisa cada enlace para confirmar relevancia.")

        logger.info("Tool GoogleSearch: Resultados obtenidos")
        return {
            "status": "success",
            "message": "\n".join(results),
            "tips": (
                "- Verifica la fecha de publicación de los enlaces.\n"
                "- Contacta fundaciones para apoyo adicional."
            ),
        }

    except requests.RequestException as e:
        logger.error(f"Tool GoogleSearch: Error en Google: {str(e)}")
        return {
            "status": "error",
            "message": f"No se pudo conectar con Google: {str(e)}.",
            "tips": (
                "- Revisa tu conexión a internet.\n"
                "- Usa Incluyeme o Servicio Público de Empleo."
            ),
        }

# Configurar agente
tools = [buscar_empleos, google_search_empleos]
agent = create_react_agent(
    orquestador,
    tools,
    prompt=SystemMessage(content="""Eres un asistente especializado en buscar empleos inclusivos.

Instrucciones:
1. Analiza la consulta para identificar:
   - Tipo de discapacidad (física, visual, etc.).
   - Ubicación (país, ciudad).
   - Empresas específicas (si se mencionan).
   - Palabras clave (sector, tipo de trabajo).

2. Usa **buscar_empleos** para Adzuna:
   - Incluye discapacidad y palabras clave en keywords.
   - Usa la ubicación como location.
   - Incluye empresas en companies si se mencionan.

3. Usa **google_search_empleos** para resultados web.

4. Combina resultados:
   - Prioriza empleos inclusivos de Adzuna.
   - Complementa con enlaces web relevantes.
   - Formatea en una tabla markdown.

5. Si ambas APIs fallan, proporciona recursos alternativos.
"""),
)

async def buscar_oportunidades(consulta: str) -> Dict[str, Any]:
    """Busca oportunidades laborales inclusivas."""
    logger.info(f"Agente Orquestador: Iniciando búsqueda para: {consulta}")
    try:
        if not CONFIG["deepseek_model"]["api_key"]:
            logger.error("Agente Orquestador: DEEPSEEK_API_KEY no configurada")
            return {
                "status": "error",
                "message": "DEEPSEEK_API_KEY no configurada en .env.",
                "tips": (
                    "- Configura DEEPSEEK_API_KEY en .env.\n"
                    "- Consulta https://deepseek.com/ para obtener una clave."
                ),
            }

        message = HumanMessage(content=consulta)
        results = []

        async for step in agent.astream({"messages": message}, stream_mode="values"):
            result = step["messages"][-1].content
            logger.info(f"Agente Orquestador: Resultado parcial: {result}")
            if result != consulta:
                try:
                    parsed = json.loads(result)
                    if isinstance(parsed, dict):
                        results.append(parsed)
                    else:
                        results.append({"status": "success", "message": result})
                except json.JSONDecodeError:
                    results.append({"status": "success", "message": result})

        if not results:
            logger.error("Agente Orquestador: No se obtuvieron resultados")
            return {
                "status": "error",
                "message": "No se encontraron resultados.",
                "tips": (
                    "- Usa términos más específicos (ej. 'empleo visual Barranquilla').\n"
                    "- Visita INCI: https://www.inci.gov.co/inclusion-laboral"
                ),
            }

        # Combinar resultados
        combined_message = []
        for result in results:
            if result["status"] == "success":
                combined_message.append(result["message"])
        if not combined_message:
            return {
                "status": "error",
                "message": "No se encontraron resultados válidos.",
                "tips": (
                    "- Revisa la conexión a internet.\n"
                    "- Usa portales como Computrabajo o Magneto."
                ),
            }

        final_message = "\n\n".join(combined_message)
        logger.info("Agente Orquestador: Búsqueda completada")
        return {
            "status": "success",
            "message": final_message,
            "tips": (
                "- Contacta fundaciones como Saldarriaga Concha o Best Buddies.\n"
                "- Usa portales como Incluyeme.com o Servicio Público de Empleo.\n"
                "- Revisa programas de inclusión en empresas como Bancolombia."
            ),
        }

    except Exception as e:
        logger.error(f"Agente Orquestador: Error: {str(e)}")
        return {
            "status": "error",
            "message": "Error interno, vuelve a intentarlo más tarde.",
            "tips": (
                "- Verifica tu conexión o claves API.\n"
                "- Intenta con una consulta más específica."
            ),
        }

if __name__ == "__main__":
    consulta = input("Introduce tu búsqueda de empleo: ")
    if not consulta:
        consulta = "Empleos inclusivos en Colombia para discapacidad física"
    result = asyncio.run(buscar_oportunidades(consulta))
    print(f"🔎 Resultado:\n{result['message']}\n\n💡 Consejos:\n{result['tips']}\n\n—")