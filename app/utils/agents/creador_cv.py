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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("cv_agent.log")]
)
logger = logging.getLogger("CVAgent")

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
    "output_dir": os.path.join(os.getcwd(), "cvGenerados"),
    "output_file": "cv.pdf",
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

# Plantilla HTML para el CV
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
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
async def estractor_datos(text: str) -> Dict[str, Any]:
    """Extrae datos clave de un texto para crear un CV."""
    logger.info("Tool Extractor: Iniciando")
    prompt = SystemMessage(content="""Extrae información para un CV en JSON con las claves: nombre, edad, genero, discapacidad, estudios, experiencia, habilidades, idiomas, ubicacion, contacto (correo, telefono). Usa null para datos ausentes.

Ejemplo:
```json
{
    "nombre": "Juan Pérez",
    "edad": 28,
    "genero": "Masculino",
    "discapacidad": "Auditiva",
    "estudios": ["Técnico en Sistemas - SENA - 2022"],
    "experiencia": ["Asistente de soporte - Empresa XYZ - 2022-2023"],
    "habilidades": ["Ofimática", "Trabajo en equipo"],
    "idiomas": ["Español (nativo)"],
    "ubicacion": "Bogotá, Colombia",
    "contacto": {"correo": "juanperez@email.com", "telefono": "+57 300 123 4567"}
}
```""")
    try:
        response = await llm.ainvoke([prompt, HumanMessage(content=text)])
        datos = response.content
        logger.info(f"Tool Extractor: Datos extraídos: {datos}")
        try:
            return json.loads(datos)
        except json.JSONDecodeError:
            logger.error("Tool Extractor: Formato JSON inválido")
            return {
                "status": "error",
                "message": "Datos extraídos no válidos. Por favor, proporciona más información.",
            }
    except Exception as e:
        logger.error(f"Tool Extractor: Error: {str(e)}")
        return {
            "status": "error",
            "message": "Error al extraer datos. Intenta de nuevo.",
        }

@tool
async def validar_datos(datos: Dict[str, Any]) -> Dict[str, Any]:
    """Valida si los datos contienen campos obligatorios."""
    logger.info("Tool Validador: Iniciando")
    required = ["nombre", "discapacidad", "contacto"]
    missing = [field for field in required if field not in datos or datos[field] is None]
    if missing or not datos.get("contacto", {}).get("correo"):
        logger.warning(f"Tool Validador: Faltan campos: {missing}")
        return {
            "status": "error",
            "message": "Faltan datos obligatorios: nombre, discapacidad, correo.",
            "tips": (
                "- Incluye nombre completo, tipo de discapacidad y correo.\n"
                "- Ejemplo: 'Juan Pérez, discapacidad visual, juan@email.com'."
            ),
        }
    logger.info("Tool Validador: Datos válidos")
    return {"status": "success", "message": "Datos válidos"}

async def crear_cv(datos: Dict[str, Any]) -> str:
    """Crea un CV en texto a partir de datos."""
    logger.info("Function CrearCV: Iniciando")
    cv_lines = []
    cv_lines.append(f"**Nombre**: {datos.get('nombre', 'No especificado')}")
    cv_lines.append(f"**Ubicación**: {datos.get('ubicacion', 'No especificada')}")
    cv_lines.append(f"**Discapacidad**: {datos.get('discapacidad', 'No especificada')}")
    cv_lines.append(f"**Contacto**: {datos.get('contacto', {}).get('correo', 'No especificado')}")
    if datos.get("telefono"):
        cv_lines.append(f"**Teléfono**: {datos.get('contacto', {}).get('telefono', 'No especificado')}")
    cv_lines.append("\n**Perfil profesional**")
    cv_lines.append(datos.get("perfil", "Profesional comprometido con experiencia en entornos inclusivos."))
    if datos.get("estudios"):
        cv_lines.append("\n**Formación académica**")
        for estudio in datos["estudios"]:
            cv_lines.append(f"- {estudio}")
    if datos.get("experiencia"):
        cv_lines.append("\n**Experiencia laboral**")
        for exp in datos["experiencia"]:
            cv_lines.append(f"- {exp}")
    if datos.get("habilidades"):
        cv_lines.append("\n**Habilidades**")
        for habilidad in datos["habilidades"]:
            cv_lines.append(f"- {habilidad}")
    if datos.get("idiomas"):
        cv_lines.append("\n**Idiomas**")
        for idioma in datos["idiomas"]:
            cv_lines.append(f"- {idioma}")
    return "\n".join(cv_lines)

async def generar_html_cv(cv_texto: str) -> str:
    """Genera HTML para el CV."""
    logger.info("Function HTML: Iniciando")
    try:
        datos = {}
        for line in cv_texto.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip("*- ").lower()
                if key in ["nombre", "ubicacion", "perfil"]:
                    datos[key] = value
        datos["email"] = datos.get("contacto", "No especificado")
        datos["telefono"] = datos.get("telefono", "No especificado")
        datos["habilidades"] = "".join(f"<li>{h}</li>" for h in datos.get("habilidades", ["No especificadas"]).split("- ")[1:])
        datos["educacion"] = datos.get("estudios", "No especificada")
        datos["experiencia"] = datos.get("experiencia", "No especificada")
        datos["adicional"] = datos.get("idiomas", "No especificados")
        datos["titulo"] = "Currículum Vitae"
        return HTML_TEMPLATE.format(**datos)
    except Exception as e:
        logger.error(f"Function HTML: Error: {str(e)}")
        return HTML_TEMPLATE.format(
            nombre="Error",
            email="No disponible",
            telefono="No disponible",
            habilidades="<li>No disponibles</li>",
            educacion="No disponible",
            experiencia="No disponible",
            adicional="No disponible",
            perfil="No disponible",
            titulo="Currículum Vitae"
        )

async def creador_pdf(input_text: str) -> Dict[str, Any]:
    """Crea un PDF con un CV."""
    logger.info("Agente Orquestador: Iniciando")
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

        agente = create_react_agent(
            orquestador,
            tools=[estractor_datos, validar_datos],
            prompt=SystemMessage(content="""Analiza si el texto contiene datos personales para un CV. Usa estractor_datos y validar_datos secuencialmente. Si no hay datos suficientes, responde: 'Por favor, proporciona datos personales para crear tu CV.'"""),
        )

        async for step in agente.astream({"messages": HumanMessage(content=input_text)}, stream_mode="values"):
            result = step["messages"][-1].content
            logger.info(f"Agente Orquestador: Mensaje procesado: {result}")
            if "Por favor, proporciona datos personales" in result:
                return {
                    "status": "error",
                    "message": result,
                    "tips": (
                        "- Incluye nombre, discapacidad, correo, experiencia.\n"
                        "- Ejemplo: 'Juan Pérez, discapacidad visual, juan@email.com, auxiliar administrativo'."
                    ),
                }
            if result != input_text:
                try:
                    datos = json.loads(result)
                except json.JSONDecodeError:
                    datos = {"status": "success", "message": result}
                break
        else:
            return {
                "status": "error",
                "message": "No se generó un CV válido.",
                "tips": (
                    "- Proporciona más datos personales.\n"
                    "- Asegúrate de incluir nombre y correo."
                ),
            }

        if datos["status"] == "error":
            return datos

        cv_texto = await crear_cv(datos)
        cv_html = await generar_html_cv(cv_texto)

        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        output_path = os.path.join(CONFIG["output_dir"], CONFIG["output_file"])

        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(cv_html, dest=pdf_file, encoding="utf-8")

        if pisa_status.err:
            logger.error(f"Agente Orquestador: Error al generar PDF: {pisa_status.err}")
            return {
                "status": "error",
                "message": "Error al generar el PDF.",
                "tips": (
                    "- Verifica el formato de los datos.\n"
                    "- Intenta de nuevo con información completa."
                ),
            }

        logger.info(f"Agente Orquestador: PDF generado en {output_path}")
        return {
            "status": "success",
            "message": f"CV generado en: {output_path}",
            "tips": (
                "- Revisa el PDF para confirmar los datos.\n"
                "- Actualiza tu CV con información reciente."
            ),
        }

    except Exception as e:
        logger.error(f"Agente Orquestador: Error: {str(e)}")
        return {
            "status": "error",
            "message": "Error interno, vuelve a intentarlo más tarde.",
            "tips": (
                "- Verifica la conexión a internet.\n"
                "- Asegúrate de proporcionar datos completos."
            ),
        }

if __name__ == "__main__":
    input_text = "Me llamo Juan Pérez, tengo 28 años, discapacidad auditiva, vivo en Bogotá, correo: juan@email.com, experiencia como auxiliar administrativo."
    result = asyncio.run(creador_pdf(input_text))
    print(f"🔎 Resultado:\n{result['message']}\n\n💡 Consejos:\n{result.get('tips', '')}\n\n—")