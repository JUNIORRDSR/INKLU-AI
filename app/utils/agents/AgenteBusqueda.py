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
    query: str = Field(..., description="Consulta de búsqueda")
    location: str | None = Field(None, description="Ubicación")
    disability_type: str | None = Field(None, description="Tipo de discapacidad")
    job_sector: str | None = Field(None, description="Sector laboral")

@tool
async def google_search_empleos(params: BusquedaParams) -> Dict[str, Any]:
    """Busca empleos inclusivos en la web usando Google Custom Search."""
    logger.info(f"Tool GoogleSearch: Iniciando con parámetros: {params}")
    
    base_url = "https://www.googleapis.com/customsearch/v1"

    # Construir una consulta más completa
    modified_query = params.query
    
    if params.location:
        modified_query += f" en {params.location}"
    
    if params.disability_type:
        modified_query += f" para personas con discapacidad {params.disability_type}"
    else:
        modified_query += " para personas con discapacidad"
        
    if params.job_sector:
        modified_query += f" sector {params.job_sector}"
        
    modified_query += " empleo inclusivo"

    logger.info(f"Tool GoogleSearch: Consulta modificada: {modified_query}")

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

    search_params = {
        "q": modified_query,
        "key": CONFIG["google"]["api_key"],
        "cx": CONFIG["google"]["cse_id"],
        "num": 8,  # Aumentado para tener más resultados
        "safe": "active",
    }

    try:
        logger.info(f"Tool GoogleSearch: Enviando solicitud con parámetros: {search_params}")
        response = requests.get(base_url, params=search_params, timeout=15)
        
        logger.info(f"Tool GoogleSearch: Respuesta status={response.status_code}")
        if response.status_code != 200:
            logger.error(f"Tool GoogleSearch: Error de Google: {response.text}")
            
        response.raise_for_status()
        data = response.json()

        if "items" not in data or not data["items"]:
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
                    "- Usa términos como 'empleo inclusivo' + ubicación.\n"
                    "- Busca por programas de inclusión laboral en tu zona.\n"
                    "- Visita portales especializados como Incluyeme.com"
                ),
            }

        results = ["| **Título** | **Enlace** | **Descripción** |"]
        results.append("|------------|------------|-----------------|")
        
        for item in data["items"]:
            title = item.get("title", "Sin título").replace("|", "-")
            link = item.get("link", "No disponible")
            snippet = item.get("snippet", "Sin descripción").replace("|", "-").replace("\n", " ")
            if len(snippet) > 100:
                snippet = snippet[:100] + "..."
            results.append(f"| {title} | [Ver]({link}) | {snippet} |")
        
        # Agregar información adicional relevante
        results.append("")
        results.append("### Recursos adicionales para búsqueda de empleo inclusivo:")
        
        if params.location and "colombia" in params.location.lower():
            results.append("- [Servicio Público de Empleo](https://www.serviciodeempleo.gov.co/) - Portal oficial de empleo")
            results.append("- [SENA](https://www.sena.edu.co/) - Formación y empleo")
            results.append("- [Pacto de Productividad](https://www.pactodeproductividad.com/) - Inclusión laboral")
        
        results.append("- [Incluyeme](https://www.incluyeme.com/) - Portal especializado en empleos para personas con discapacidad")
        
        logger.info("Tool GoogleSearch: Resultados obtenidos exitosamente")
        return {
            "status": "success",
            "message": "\n".join(results),
            "tips": (
                "- Revisa las fechas de publicación de las ofertas.\n"
                "- Contacta directamente a las empresas que muestran interés en inclusión.\n"
                "- Considera enviar tu CV a fundaciones especializadas en inclusión laboral.\n"
                "- Actualiza tu perfil en LinkedIn mencionando tus habilidades específicas."
            ),
        }

    except requests.RequestException as e:
        logger.error(f"Tool GoogleSearch: Error en Google: {str(e)}")
        return {
            "status": "error",
            "message": f"No se pudo conectar con Google: {str(e)}.",
            "tips": (
                "- Verifica tu conexión a internet.\n"
                "- Intenta nuevamente más tarde.\n"
                "- Como alternativa, visita directamente portales de empleo inclusivo."
            ),
        }

# Configurar agente con solo Google Search
tools = [google_search_empleos]
agent = create_react_agent(
    orquestador,
    tools,
    prompt=SystemMessage(content="""Eres un asistente especializado en buscar empleos inclusivos para personas con discapacidad.

Instrucciones:
1. Analiza la consulta para identificar:
   - Tipo de discapacidad (física, visual, auditiva, etc.).
   - Ubicación (país, ciudad).
   - Sector laboral (si se menciona).
   - Palabras clave relevantes.

2. Usa **google_search_empleos** para buscar información:
   - Incluye la consulta principal como query.
   - Especifica la ubicación como location.
   - Indica el tipo de discapacidad en disability_type.
   - Añade el sector laboral en job_sector si corresponde.

3. Presenta los resultados de forma clara:
   - Muestra las opciones en formato tabla.
   - Proporciona enlaces útiles.
   - Sugiere recursos adicionales relevantes.

4. Si la búsqueda no produce resultados:
   - Ofrece alternativas y consejos prácticos.
   - Menciona portales específicos para empleo inclusivo.
   - Sugiere organizaciones que apoyan la inclusión laboral.
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
                "message": "No se encontraron resultados para tu búsqueda.",
                "tips": (
                    "- Usa términos más específicos.\n"
                    "- Intenta con diferentes ubicaciones.\n"
                    "- Visita directamente portales especializados en inclusión laboral."
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
                    "- Verifica que las claves de API estén configuradas correctamente.\n"
                    "- Usa portales como Computrabajo o LinkedIn con filtros específicos."
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
                "- Revisa programas de inclusión en empresas como Bancolombia, Grupo Éxito o Sodexo.\n"
                "- Actualiza tu CV destacando tus habilidades específicas."
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

def test_google_search():
    """Prueba directa de Google Search API para verificar su funcionamiento."""
    print("=== PRUEBA DE GOOGLE SEARCH API ===")
    
    params = {
        "q": "empleos discapacidad Colombia",
        "key": CONFIG["google"]["api_key"],
        "cx": CONFIG["google"]["cse_id"],
        "num": 2,
    }
    
    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", 
                               params=params, 
                               timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Respuesta: {response.text[:300]}...")
        
        if response.status_code == 200:
            data = response.json()
            if "items" in data and data["items"]:
                print("\nResultados encontrados:")
                for i, item in enumerate(data["items"], 1):
                    print(f"{i}. {item.get('title')} - {item.get('link')}")
            else:
                print("\nNo se encontraron resultados")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Descomentar para probar directamente Google Search API
    # test_google_search()
    
    consulta = input("Introduce tu búsqueda de empleo: ")
    if not consulta:
        consulta = "Empleos inclusivos en Colombia para discapacidad física"
    result = asyncio.run(buscar_oportunidades(consulta))
    print(f"🔎 Resultado:\n{result['message']}\n\n💡 Consejos:\n{result['tips']}\n\n—")