import os
import asyncio
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from xhtml2pdf import pisa

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger("CVAgent")

# Cargar variables de entorno
load_dotenv()

# Configuración centralizada
CONFIG = {
    "deepseek_model": {
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
    },
    "output_dir": os.path.join(os.getcwd(), "cvGenerados"),  # Directorio actual
    "output_file": "cv.pdf",
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

# Ejemplo de CV para guiar la generación
EJEMPLO_CV = """
Nombre completo: Juan Pérez
Edad: 28 años
Género: Masculino
Tipo de discapacidad: Auditiva
Ubicación: Bogotá, Colombia
Correo electrónico: juanperez@email.com
Teléfono: +57 300 123 4567

Perfil profesional:
Soy una persona proactiva, responsable y con gran capacidad de adaptación. Me especializo en atención al cliente y tengo experiencia trabajando en entornos inclusivos.

Formación académica:
- Técnico en Sistemas - SENA - 2022
- Bachiller Académico - Colegio Distrital San Martín - 2018

Experiencia laboral:
- Asistente de soporte técnico - Empresa XYZ - 2022-2023
  - Atención a usuarios con problemas técnicos
  - Mantenimiento básico de equipos
- Cajero - Supermercado ABC - 2019-2021
  - Manejo de caja y atención al cliente
  - Control de inventario básico

Habilidades:
- Dominio básico de herramientas ofimáticas
- Comunicación escrita clara
- Trabajo en equipo

Idiomas:
- Español (nativo)
- Lengua de señas colombiana (LSC) - intermedio
"""

# Plantilla HTML para el CV
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículum Vitae - {nombre}</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f6f8; color: #333; line-height: 1.6; }}
        .container {{ width: 210mm; min-height: 297mm; margin: 0 auto; display: flex; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .left-column {{ width: 35%; background: linear-gradient(135deg, #153C62 0%, #1E5689 100%); color: white; padding: 30px; }}
        .right-column {{ width: 65%; background-color: white; padding: 40px; }}
        h1 {{ font-size: 36px; margin: 0 0 10px; color: #153C62; font-weight: 700; }}
        h2 {{ font-size: 20px; color: #153C62; border-bottom: 2px solid #153C62; padding-bottom: 8px; margin: 30px 0 15px; text-transform: uppercase; letter-spacing: 1px; }}
        .left-column h2 {{ color: white; border-bottom: 2px solid rgba(255,255,255,0.3); }}
        .section {{ margin-bottom: 25px; }}
        .info-label {{ font-weight: 600; display: inline-block; width: 80px; }}
        .contact-item {{ display: flex; align-items: center; margin-bottom: 10px; font-size: 14px; }}
        ul {{ padding-left: 20px; margin: 10px 0; }}
        ul li {{ margin-bottom: 8px; font-size: 14px; }}
        .left-column ul li {{ list-style-type: none; padding-left: 20px; position: relative; }}
        .left-column ul li:before {{ content: '✓'; position: absolute; left: 0; color: #ffffff; }}
        .education-item p {{ margin: 5px 0; }}
        .job-title {{ font-weight: 600; font-size: 16px; margin-bottom: 5px; }}
        .job-period {{ font-style: italic; color: #666; font-size: 14px; margin-bottom: 10px; }}
        @media print {{ body {{ background: none; }} .container {{ box-shadow: none; }} }}
        @media screen and (max-width: 768px) {{ .container {{ flex-direction: column; width: 100%; }} .left-column, .right-column {{ width: 100%; padding: 20px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="left-column">
            <h2>Contacto</h2>
            <div class="contact-item"><p><span class="info-label">Email:</span> {email}</p></div>
            <div class="contact-item"><p><span class="info-label">Tel:</span> {telefono}</p></div>
            <h2>Habilidades</h2>
            <ul>{habilidades}</ul>
            <h2>Educación</h2>
            <div class="education-item">{educacion}</div>
        </div>
        <div class="right-column">
            <h1>{nombre}</h1>
            <h2>{titulo}</h2>
            <div class="section">
                <h2>Acerca de mí</h2>
                <p>{perfil}</p>
            </div>
            <div class="section">
                <h2>Experiencia Laboral</h2>
                {experiencia}
            </div>
            <div class="section">
                <h2>Información Adicional</h2>
                <p>{adicional}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

@tool
async def estractor_datos(text: str) -> str:
    """Extrae datos clave de un texto para crear un CV en formato JSON.
    
    Args:
        text (str): Texto con información personal.
    
    Returns:
        str: Datos extraídos en JSON o mensaje de error.
    """
    logger.info("Agente Extractor: Iniciando extracción de datos")
    prompt = SystemMessage(content="""Extrae información relevante para un CV del texto proporcionado. Devuelve un JSON con las claves: nombre, edad, genero, discapacidad, estudios, experiencia, habilidades, idiomas, ubicacion, contacto (correo y teléfono). Usa null para datos ausentes. Ignora contenido irrelevante y no inventes datos.

    Ejemplo de salida:
    ```json
    {
        "nombre": "Juan Pérez",
        "edad": 28,
        "genero": "Masculino",
        "discapacidad": "Auditiva",
        "estudios": ["Técnico en Sistemas - SENA - 2022"],
        "experiencia": ["Asistente de soporte técnico - Empresa XYZ - 2022-2023"],
        "habilidades": ["Herramientas ofimáticas", "Trabajo en equipo"],
        "idiomas": ["Español (nativo)", "Lengua de señas (intermedio)"],
        "ubicacion": "Bogotá, Colombia",
        "contacto": {"correo": "juanperez@email.com", "telefono": "+57 300 123 4567"}
    }
    ```""")
    
    response = await llm.ainvoke([prompt, HumanMessage(content=text)])
    datos = response.content
    logger.info(f"Agente Extractor: Datos extraídos: {datos}")
    
    try:
        json.loads(datos)  # Validar JSON
    except json.JSONDecodeError:
        logger.error("Agente Extractor: Formato JSON inválido")
        return await terminar_conversacion()
    
    validacion = await validar_datos(datos)
    if "Sí" in validacion:
        cv_text = await crear_cv(datos)
        return cv_text
    return await terminar_conversacion()

@tool
async def validar_datos(datos: str) -> str:
    """Valida si los datos extraídos contienen los campos obligatorios.
    
    Args:
        datos (str): Datos en formato JSON.
    
    Returns:
        str: 'Sí' si válidos, 'No' si faltan campos.
    """
    logger.info("Agente Validador: Iniciando validación de datos")
    prompt = SystemMessage(content="""Valida si el JSON contiene los campos obligatorios: 'nombre', 'contacto.correo', 'discapacidad'. Responde solo con 'Sí' si todos están presentes o 'No' si falta alguno.""")
    response = await llm.ainvoke([prompt, HumanMessage(content=datos)])
    logger.info(f"Agente Validador: Resultado: {response.content}")
    return response.content

@tool
async def terminar_conversacion() -> str:
    """Termina la conversación si los datos son insuficientes.
    
    Returns:
        str: Mensaje de error.
    """
    logger.info("Agente Terminador: Finalizando conversación por datos insuficientes")
    return "Hace falta enviar más datos, reintentar."

async def crear_cv(datos: str) -> str:
    """Crea un CV en texto a partir de datos extraídos.
    
    Args:
        datos (str): Datos en formato JSON.
    
    Returns:
        str: Texto del CV generado.
    """
    logger.info("Agente Creador CV: Iniciando generación de CV")
    prompt = SystemMessage(content=f"""Genera un CV profesional en texto basado en el JSON proporcionado. Usa un formato claro y estructurado similar al ejemplo:

    {EJEMPLO_CV}

    Organiza las secciones: Perfil profesional, Formación académica, Experiencia laboral, Habilidades, Idiomas. Usa lenguaje formal.""")
    
    response = await llm.ainvoke([prompt, HumanMessage(content=datos)])
    logger.info(f"Agente Creador CV: CV generado: {response.content}")
    return response.content

async def generar_html_cv(cv_texto: str) -> str:
    """Genera un documento HTML para el CV.
    
    Args:
        cv_texto (str): Texto del CV.
    
    Returns:
        str: Documento HTML.
    """
    logger.info("Agente HTML: Iniciando generación de HTML")
    prompt = SystemMessage(content=f"""Convierte el texto del CV en un documento HTML usando la plantilla proporcionada. Reemplaza los placeholders con los datos del CV, manteniendo la estructura y estilos exactos.

    Plantilla:
    {HTML_TEMPLATE}

    Devuelve solo el HTML resultante.""")
    
    response = await llm.ainvoke([prompt, HumanMessage(content=cv_texto)])
    logger.info("Agente HTML: HTML generado")
    return response.content

async def creador_pdf(input_text: str) -> Dict[str, Any]:
    """Crea un archivo PDF con un CV a partir de datos proporcionados.
    
    Args:
        input_text (str): Texto con información personal.
    
    Returns:
        Dict[str, Any]: Estado y mensaje del proceso.
    """
    try:
        logger.info("Agente Orquestador: Iniciando procesamiento de CV")
        # Verificar API key
        if not CONFIG["deepseek_model"]["api_key"]:
            logger.error("Agente Orquestador: DEEPSEEK_API_KEY no configurada")
            return {"status": "error", "message": "DEEPSEEK_API_KEY no configurada en .env"}

        # Crear agente
        agente = create_react_agent(
            orquestador,
            tools=[estractor_datos],
            prompt=SystemMessage(content="""Analiza si el texto contiene datos personales para un CV (nombre, experiencia, habilidades, etc.). Usa la herramienta estractor_datos si es así. Si no, responde: 'Por favor, proporciona datos personales para crear tu CV.'"""),
        )
        
        # Procesar input
        async for step in agente.astream({"messages": HumanMessage(content=input_text)}, stream_mode="values"):
            result = step["messages"][-1].content
            logger.info(f"Agente Orquestador: Mensaje procesado: {result}")
            if "Por favor, proporciona datos personales" in result:
                logger.error("Agente Orquestador: Input inválido")
                return {"status": "error", "message": result}
            if result != input_text:
                cv_texto = result
                break
        else:
            logger.error("Agente Orquestador: No se generó CV válido")
            return {"status": "error", "message": "No se generó un CV válido."}
        
        # Generar HTML
        cv_html = await generar_html_cv(cv_texto)
        
        # Asegurar directorio
        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        output_path = os.path.join(CONFIG["output_dir"], CONFIG["output_file"])
        
        # Guardar HTML temporal
        temp_html_path = os.path.join(CONFIG["output_dir"], "temp_cv.html")
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(cv_html)
        logger.info(f"Agente Orquestador: HTML guardado en {temp_html_path}")
        
        # Generar PDF
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(cv_html, dest=pdf_file, encoding="utf-8")
        
        if pisa_status.err:
            logger.error(f"Agente Orquestador: Error al generar PDF: {pisa_status.err}")
            return {"status": "error", "message": f"Error al generar PDF: {pisa_status.err}"}
        
        logger.info(f"Agente Orquestador: PDF generado en {output_path}")
        return {"status": "success", "message": f"PDF generado en: {output_path}"}
    
    except Exception as e:
        logger.error(f"Agente Orquestador: Error general: {str(e)}")
        return {"status": "error", "message": f"Error: {str(e)}"}

if __name__ == "__main__":
    input_text = "Hola, me llamo Juan Pérez, tengo 28 años y una discapacidad auditiva. Actualmente vivo en Bogotá y estoy buscando oportunidades laborales inclusivas. Mi correo es j@uni.co y tengo experiencia como auxiliar administrativo. También hablo español y algo de lengua de señas colombiana."
    result = asyncio.run(creador_pdf(input_text))
    print(result["message"])