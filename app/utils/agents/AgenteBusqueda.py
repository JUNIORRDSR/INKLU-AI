import os
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field
from dotenv import load_dotenv
import requests
import os
from typing import List, Optional
import json

# Cargar variables de entorno
load_dotenv()

# 1. Configuración de modelos
llm_orquestador = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# 2. Herramientas 
class BusquedaParams(BaseModel):
    board_tokens: List[str] = Field(..., description="Subdominios de empresas ej: airbnb, google, microsoft")
    keywords: List[str] = Field(default=["discapacidad"], description="Palabras clave de búsqueda")
    location_filter: Optional[str] = Field(None, description="Filtro de ubicación (ej: Colombia, España)")

@tool
def buscar_empleos(params: BusquedaParams) -> str:
    """Busca empleos para personas con discapacidad en boards de empresas específicas"""
    # Verificar que los board_tokens son realmente empresas y no ubicaciones
    empresas_sugeridas = ["bancolombia", "grupoexito", "ecopetrol", "nutresa", "falabella", 
                       "microsoft", "google", "ibm", "siemens", "unilever", "johnson", "colsubsidio"]
    
    # Si los tokens parecen ubicaciones y no empresas, sugerir empresas
    es_ubicacion = False
    ubicaciones = ["colombia", "bogota", "medellin", "cali", "barranquilla", "cartagena"]
    
    if all(board.lower() in ubicaciones for board in params.board_tokens):
        es_ubicacion = True
        
    results = []
    
    # Si parece que se ingresó una ubicación en lugar de empresa
    if es_ubicacion:
        results.append(f"⚠️ Parece que has ingresado una ubicación ({', '.join(params.board_tokens)}) " 
                     f"en lugar de nombres de empresas.")
        results.append("🔍 Aquí hay algunas empresas con programas de inclusión laboral que podrías considerar:")
        
        for empresa in empresas_sugeridas[:5]:
            keywords_query = " ".join(params.keywords)
            location_text = f" en {params.location_filter}" if params.location_filter else ""
            results.append(f"- {empresa.title()}: Oportunidades para personas con {keywords_query}{location_text}")
            
        results.append("\n💡 Para una búsqueda más específica, intenta con nombres de empresas como: " + 
                     ", ".join(empresa.title() for empresa in empresas_sugeridas[5:]))
    else:
        # Proceder con la búsqueda normal
        for board in params.board_tokens:
            keywords_query = " ".join(params.keywords)
            location_text = f" en {params.location_filter}" if params.location_filter else ""
            
            # Simulación de resultados de búsqueda de empleo
            results.append(f"🏢 {board.title()}")
            results.append(f"  - Vacante: Analista administrativo para personas con {keywords_query}")
            results.append(f"  - Ubicación: {params.location_filter if params.location_filter else 'Remoto'}")
            results.append(f"  - Descripción: Posición inclusiva que valora la diversidad y proporciona adaptaciones necesarias")
            results.append("")
    
    return "\n".join(results)

@tool
def google_search_empleos(query: str) -> str:
    """Realiza búsqueda de empleos para personas con discapacidad en la web usando la API de Google"""
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    # Modificar la consulta para enfocarse en empleos para personas con discapacidad
    modified_query = f"{query} empleo discapacidad inclusivo"
    
    # Verificar que las claves de API estén configuradas
    google_api_key = "AIzaSyA0-lCzH3pPTsDzlsmcl6UdGrvEh83dtfE"
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not google_api_key or not google_cse_id:
        return """API no configurada correctamente. Por favor verifica:
1. Que existe un archivo .env en la misma carpeta que el script
2. Que contenga las claves GOOGLE_API_KEY y GOOGLE_CSE_ID válidas
3. Ejemplo de formato en .env:
   GOOGLE_API_KEY=AIzaSyB1234example5678
   GOOGLE_CSE_ID=123456789abcdef"""
    
    params = {
        "q": modified_query,
        "key": google_api_key,
        "cx": google_cse_id,
        "num": 5
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                results = []
                for item in data["items"]:
                    results.append({
                        "title": item.get("title", "Sin título"),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "Sin descripción")
                    })
                return json.dumps(results, ensure_ascii=False)
            else:
                return "No se encontraron resultados"
        else:
            error_data = {}
            try:
                error_data = response.json()
            except:
                pass
                
            error_message = f"Error en la API: {response.status_code}"
            if error_data and "error" in error_data:
                error_message += f"\nDetalle: {error_data['error'].get('message', 'No hay detalles')}"
            
            # Simulación de resultados para desarrollo/pruebas cuando hay error en la API
            return """En caso de error con la API de Google, aquí hay algunos recursos recomendados para buscar empleo:
            
1. Portales de empleo especializados en Colombia:
   - Incluyeme.com: https://www.incluyeme.com/colombia/
   - Pacto de Productividad: https://www.pactodeproductividad.com/
   - ServicioPublicoDeEmpleo: https://www.serviciodeempleo.gov.co/

2. Empresas con programas de inclusión en Colombia:
   - Grupo Éxito
   - Bancolombia
   - Falabella
   - Fundación Corona
   
3. Organizaciones y fundaciones:
   - Fundación Saldarriaga Concha
   - Best Buddies Colombia
   - SENA - Programas de inclusión laboral"""
        
    except Exception as e:
        return f"Error en la búsqueda: {str(e)}\n\nPor favor verifica tu conexión a internet y las claves API"

# 3. Configurar agente
tools = [buscar_empleos, google_search_empleos]
agent = create_react_agent(
    llm_orquestador,
    tools,
    prompt=SystemMessage(content="""Eres un asistente especializado en buscar empleos para personas con discapacidad.
Tu objetivo es encontrar oportunidades laborales inclusivas y accesibles.

Sigue estos pasos:
1. Cuando recibas una consulta, analiza si menciona empresas específicas:
   - Si menciona empresas (ej: Bancolombia, Exito), usa buscar_empleos con esas empresas
   - Si solo menciona ubicaciones (ej: Colombia), usa buscar_empleos con empresas conocidas por sus programas de inclusión

2. Para la herramienta buscar_empleos:
   - board_tokens debe ser una lista de NOMBRES DE EMPRESAS (no países ni ciudades)
   - keywords debe incluir el tipo de discapacidad mencionada (física, auditiva, etc.)
   - location_filter debe ser el país o ciudad mencionada

3. Luego usa google_search_empleos para ampliar la búsqueda con resultados web
   - Si la API de Google falla, no te preocupes, usa los recursos alternativos proporcionados

4. En tu respuesta final:
   - Organiza los resultados por relevancia
   - Prioriza empleos que mencionan inclusión y accesibilidad
   - Incluye información de contacto cuando esté disponible
   - Proporciona consejos adicionales para la búsqueda de empleo
""")
)

# 4. Función principal para realizar búsquedas

def buscar_oportunidades(consulta):
    """
    Realiza búsquedas de oportunidades laborales para personas con discapacidad utilizando APIs y modelos de IA.

    Esta función coordina el proceso de búsqueda de empleos inclusivos mediante:
    1. Verificación de configuración de APIs necesarias (Google Search y DeepSeek)
    2. Procesamiento de la consulta del usuario a través de un agente de IA
    3. Búsqueda en múltiples fuentes (boards de empresas y resultados web)
    4. Presentación de resultados con formato amigable y emojis

    Args:
        consulta (str): Texto con la consulta del usuario que puede incluir:
            - Tipo de discapacidad
            - Ubicación deseada
            - Empresas específicas
            - Tipo de trabajo o sector

    Raises:
        Exception: Si hay errores de conectividad o problemas con las APIs.
            Se manejan los errores mostrando sugerencias de solución.

    Notas:
        - Opera en modo demostración si las APIs no están configuradas
        - Utiliza emojis para mejorar la legibilidad de los resultados
        - Incluye sugerencias de empresas con programas de inclusión
    """
    print(f"\n🔍 Buscando: {consulta}\n")
    message = HumanMessage(content=consulta)
    
    # Verificar si hay claves de API configuradas
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key or not cse_id or not deepseek_key:
        print("\n⚠️ ADVERTENCIA: Algunas claves API no están configuradas correctamente.")
        print("Por favor crea un archivo .env con las siguientes variables:")
        print("GOOGLE_API_KEY=tu_clave_google_api")
        print("GOOGLE_CSE_ID=tu_id_motor_busqueda")
        print("DEEPSEEK_API_KEY=tu_clave_deepseek_api")
        print("\nEl programa continuará en modo de demostración con resultados simulados.\n")
    
    try:
        for step in agent.stream(
            {"messages": message},
            stream_mode="values",
        ):
            resultado = step["messages"][-1]
            resultado.pretty_print()
    except Exception as e:
        print(f"\n❌ Error durante la búsqueda: {str(e)}")
        print("\nSugerencias para solucionar el problema:")
        print("1. Verifica tu conexión a internet")
        print("2. Comprueba que las API keys sean válidas")
        print("3. Intenta con una búsqueda más específica")
    
    print("\n✅ Búsqueda finalizada\n")

# Ejemplo de uso cuando se ejecuta el script directamente
if __name__ == "__main__":
    print("\n=== AGENTE DE BÚSQUEDA DE EMPLEOS PARA PERSONAS CON DISCAPACIDAD ===\n")
    print("🧠 Desarrollado con LangChain y DeepSeek AI\n")
    
    # Mostrar opciones predefinidas
    print("Opciones de búsqueda:")
    print("1. Empleos inclusivos en Colombia para discapacidad física")
    print("2. Oportunidades laborales para discapacidad auditiva en empresas tecnológicas")
    print("3. Trabajo para personas con discapacidad visual en Bancolombia")
    print("4. Búsqueda personalizada")
    
    opcion = input("\nSelecciona una opción (1-4) o presiona Enter para la opción 1: ")
    
    if not opcion or opcion == "1":
        consulta = "Buscar empleos inclusivos en Colombia para personas con discapacidad física"
    elif opcion == "2":
        consulta = "Buscar oportunidades laborales para personas con discapacidad auditiva en empresas de tecnología"
    elif opcion == "3":
        consulta = "Buscar trabajo para personas con discapacidad visual en Bancolombia"
    elif opcion == "4":
        consulta = input("\nIntroduce tu búsqueda personalizada: ")
        if not consulta:
            consulta = "Buscar empleos inclusivos en Colombia para personas con discapacidad física"
    else:
        print("Opción no válida. Usando la opción 1 por defecto.")
        consulta = "Buscar empleos inclusivos en Colombia para personas con discapacidad física"
    
    buscar_oportunidades(consulta)