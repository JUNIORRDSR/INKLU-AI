from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import pdfkit
load_dotenv()

ll_deepseek = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
)   

llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

orquestador = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# Herramienta del orquestador
@tool
def estractor_datos(text: str) -> str:
    """
    Funcion para extraer datos claves de un texto que sirvan para armar hojas de vida, la respuesta funciona tanto en json.
    Args:
        text (str): El texto del que se extraeran los datos."""
    response = llm.invoke([
        SystemMessage(content="""Eres un asistente especializado en extraer información personal relevante del texto proporcionado por el usuario. Tu única tarea es identificar y extraer los siguientes datos, si están presentes:

        Nombre completo

        Edad

        Género

        Tipo de discapacidad

        Nivel de estudios o formación académica

        Experiencia laboral

        Habilidades

        Idiomas

        Ubicación (ciudad o país)

        Información de contacto (correo, teléfono, etc.)

        La información puede estar escrita en lenguaje natural, informal o en frases cotidianas. Ignora cualquier otro contenido que no sea relevante para la creación de una hoja de vida. Si no se menciona un dato específico, no lo inventes ni lo asumas.

        Devuelve los datos extraídos en un formato de texto estructurado (str).

        No hagas preguntas ni continúes la conversación. Solo responde con los datos extraídos."""),
        HumanMessage(content=text)
    ])
    datos_extraidos = response.content
    print(datos_extraidos)
    resultado_validacion = validar_datos.invoke(datos_extraidos)
    print(f"Resultado de la validacion: {resultado_validacion}")
    desicion = llm.invoke([
        SystemMessage(content="Sintesiza la respuesta de la validacion y si es positiva respone solo con un ""Si"", si no es positiva responde solo con un ""No"""),
        HumanMessage(content=resultado_validacion.content)
    ])
    if desicion.content == "**Sí**" or desicion.content == "Si" or desicion.content == "Sí" or desicion.content == "si" or desicion.content == "Sí.":
        print("Los datos son validos, se procede a crear el CV")
        resultado = crear_cv(datos_extraidos)
        return resultado.content
    elif desicion.content == "No" or desicion.content == "no" or desicion.content == "NO" or desicion.content == "**No**":
        print("Los datos no son validos")
        resultado = terminar_conversacion.invoke()
        print(f"Resultado de la validacion: {resultado}")
        return resultado.content
    return resultado_validacion.content
# Herramienta de un operador
@tool
def validar_datos(datos: str) -> str:
    """
    Funcion para validar si estan completos 
los datos minimos? los datos extraidos de un texto, como minimo para realizar la validacion correctamente necesito que se encuentren campos como "Nombre", "Correo", "Discapacidad".
    Args:
        datos (str): El texto que contiene los datos extraidos."""
    response = llm.invoke([
        SystemMessage(content="Eres un asistente que valida los datos extraidos de un texto y responde si o no dependiendo si los datos OBLIGATORIOS se necesita validación estricta (que incluyan por lo menos los 3 campos obligatoriamente) corresponden a Nombre, Correo y Discapacidad."),
        HumanMessage(content=datos)
    ])
    print(f"Respuesta de la validacion: {response}")
    return response

@tool
def terminar_conversacion() -> str:
    """
    Funcion para terminar la conversacion."""
    response = llm.invoke(
        SystemMessage(content="Eres un asistente que termina la conversacion y dice que `Hace falta enviar mas datos, reintentar`")
    )
    return response.content

def desicion_datos_minimos(datos: str) -> str:
    """
    Funcion para validar si estan completos los datos minimos? Necesito que en base a la respuesta del modelo anterior generes una desicion para ver que tool ejecutar en funcion de las disponibles y la respuesta.
    Args:
        datos (str): El texto que contiene los datos extraidos."""
    agent = create_react_agent(
        llm,
        tools=[],
        prompt=SystemMessage(content="Eres un asistente que en base a las respuestas del sitema escoge la tool adecuada para realizar su trabajo."),
    )
    response = agent.invoke()
    return response.content

def crear_cv(datos: str) -> str:
    """
    Funcion para crear un CV a partir de los datos extraidos."""
    response = llm.invoke([
        SystemMessage(content="A partir de los siguientes datos personales, genera una hoja de vida clara, profesional y bien estructurada. Sigue el formato de ejemplo que se presenta más abajo, asegurándote de organizar correctamente las secciones, usar un lenguaje formal y destacar los puntos fuertes del perfil." \
        "El resultado final debe estar listo para usarse como una hoja de vida en texto, con una presentación ordenada y profesional." \
        f"Ejemplo: {ejemplo_cv}"),
        HumanMessage(content=datos)
    ])
    print(f"Respuesta de la creacion del CV: {response}")
    global cv 
    cv = response.content
    print(f"CV generado: {cv}")
    return response.content

ejemplo_cv = """
Nombre completo: Juan Pérez
Edad: 28 años
Género: Masculino
Tipo de discapacidad: Auditiva
Ubicación: Bogotá, Colombia
Correo electrónico: juanperez@email.com
Teléfono: +57 300 123 4567

Perfil profesional:
Soy una persona proactiva, responsable y con gran capacidad de adaptación. Me especializo en atención al cliente y tengo experiencia trabajando en entornos inclusivos. Busco oportunidades laborales que valoren la diversidad y la inclusión.

Formación académica:

Técnico en Sistemas - SENA - Finalizado en 2022

Bachiller Académico - Colegio Distrital San Martín - 2018

Experiencia laboral:
Asistente de soporte técnico - Empresa XYZ - 2022 a 2023

Atención a usuarios con problemas técnicos

Mantenimiento básico de equipos

Registro y seguimiento de incidentes

Cajero - Supermercado ABC - 2019 a 2021

Manejo de caja y atención al cliente

Control de inventario básico

Trabajo en equipo con personal diverso

Habilidades:

Dominio básico de herramientas ofimáticas

Comunicación escrita clara

Trabajo en equipo

Atención al detalle

Idiomas:

Español (nativo)

Lengua de señas colombiana (LSC) - nivel intermedio"""

cv = ""

agente = create_react_agent(
    orquestador,
    tools=[estractor_datos],
    prompt=SystemMessage(content="""Eres un asistente que analiza las entradas del usuario para detectar si contienen información personal útil para construir una hoja de vida, como nombre, edad, tipo de discapacidad, estudios, experiencia laboral, habilidades o idiomas.

Si el mensaje del usuario incluye datos personales o información relevante sobre su perfil, debes activar la herramienta encargada de extraer estos datos (tool_extractor_de_datos).

Si el mensaje no contiene información personal útil, responde amablemente que solo puedes ayudar cuando el usuario proporcione datos relacionados con su hoja de vida.

No extraigas los datos tú mismo, solo determina si se deben pasar a la herramienta de extracción."""),
)

message = HumanMessage(content="Hola, me llamo Juan Pérez, tengo 28 años y una discapacidad auditiva. Actualmente vivo en Bogotá y estoy buscando oportunidades laborales inclusivas. Mi correo es j@uni.co y tengo experiencia como auxiliar administrativo. También hablo español y algo de lengua de señas colombiana.")

for step in agente.stream(
    {"messages": message},  # Usa el mensaje formateado correctamente
    stream_mode="values",
):
    # Imprime el mensaje completo para depuración   
    step["messages"][-1].pretty_print()

print(f"CV generado: {cv}")
html = """  
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Documento</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>Hola Mundo</h1>
    <p>Este es un ejemplo de contenido HTML válido para convertir a PDF.</p>
</body>
</html>
"""

cv_html = ll_deepseek.invoke([
    SystemMessage(content=f"""Convierte el siguiente texto que contiene información personal para un currículum vitae en un documento HTML con un diseño visual atractivo de dos columnas. La columna izquierda debe contener los datos de contacto, habilidades y educación, y la columna derecha debe contener una breve descripción personal ("Acerca de mí") y la experiencia laboral.

Utiliza estilos CSS modernos y asegúrate de:

Usar tipografía clara como Arial o sans-serif.

Incluir colores similares al ejemplo: tonos azulados y blancos.

Presentar el nombre completo en grande, con la profesión debajo.

Mostrar íconos o separar con líneas cada sección.

No usar imágenes (la IA solo generará HTML).
                  
                  Quiero que generes una cadena de HTML limpia y válida, que pueda convertirse correctamente a PDF con librerías como pdfkit o WeasyPrint.

📌 Requisitos del HTML:

Debe comenzar con <!DOCTYPE html> y tener correctamente estructurados los elementos <html>, <head>, y <body>.

Debe tener codificación UTF-8 (<meta charset="UTF-8">).

Incluye una hoja de estilos básica dentro de <style> en el <head>, sin enlaces externos.

No debe contener rutas a imágenes o recursos externos (como fuentes o scripts remotos).

Todo el contenido debe estar contenido en una sola cadena multilínea de Python, usando triple comillas

No uses caracteres de escape innecesarios (\n, \\, \", etc.). El HTML debe ser copiado tal cual, sin procesar.

El contenido puede ser una estructura de currículum (CV), factura, carta, etc., según el contexto.
                  puedes seguir el siguiente ejemplo de HTML para crear un CV: {html}"""),
    HumanMessage(content=cv)
    ,])
print(f"CV HTML: {cv_html}")
pdfkit.from_string(cv_html, 'cv.pdf')