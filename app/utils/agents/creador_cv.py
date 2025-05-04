from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from dotenv import load_dotenv
from wkhtmltopdf.main import WKhtmlToPdf
import pdfkit
import os
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


def creador_pdf():
    # Ejecutar la función principal o cualquier otra lógica aquí
    ruta= r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=ruta)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Hojas de vida/cv.pdf")
    
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

    input_text = "Hola, me llamo Juan Pérez, tengo 28 años y una discapacidad auditiva. Actualmente vivo en Bogotá y estoy buscando oportunidades laborales inclusivas. Mi correo es j@uni.co y tengo experiencia como auxiliar administrativo. También hablo español y algo de lengua de señas colombiana."
    ## Ejemplo de datos ideales
    message = HumanMessage(content=input_text)

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
    <title>Currículum Vitae</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f6f8;
            color: #333;
        }
        .container {
            display: flex;
            min-height: 100vh;
        }
        .left-column {
            width: 30%;
            background-color: #153C62;
            color: white;
            padding: 20px;
        }
        .right-column {
            width: 70%;
            padding: 40px;
            background-color: white;
        }
        h1 {
            font-size: 32px;
            margin-bottom: 5px;
        }
        h2 {
            font-size: 18px;
            color: #153C62;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        .section {
            margin-bottom: 20px;
        }
        .info-label {
            font-weight: bold;
        }
        .left-column h2 {
            color: #fff;
            border-color: #fff;
        }
        ul {
            padding-left: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-column">
            <h2>Contacto</h2>
            <p><span class="info-label">Email:</span> zara@mail.com</p>
            <p><span class="info-label">Tel:</span> +57 300 000 0000</p>

            <h2>Habilidades</h2>
            <ul>
                <li>Comunicación</li>
                <li>Trabajo en equipo</li>
                <li>Adaptabilidad</li>
            </ul>

            <h2>Educación</h2>
            <p>Universidad Ejemplo</p>
            <p>Ingeniería de Sistemas</p>
            <p>2018 - 2022</p>
        </div>
        <div class="right-column">
            <h1>Zara Pérez</h1>
            <h2>Desarrolladora Full Stack</h2>

            <div class="section">
                <h2>Acerca de mí</h2>
                <p>Soy una profesional apasionada por la tecnología, con experiencia en el desarrollo de soluciones web y un enfoque orientado al detalle.</p>
            </div>

            <div class="section">
                <h2>Experiencia Laboral</h2>
                <p><strong>Desarrolladora Web - Tech Solutions</strong> (2023 - Presente)</p>
                <ul>
                    <li>Desarrollo de aplicaciones con React y Node.js.</li>
                    <li>Implementación de buenas prácticas de desarrollo.</li>
                </ul>
                <p><strong>Practicante - SoftDev</strong> (2022)</p>
                <ul>
                    <li>Soporte en tareas de backend con Python y Flask.</li>
                </ul>
            </div>

            <div class="section">
                <h2>Información Adicional</h2>
                <p>Disponible para trabajar de forma remota o presencial. Alto nivel de compromiso y ética profesional.</p>
            </div>
        </div>
    </div>
</body>
</html>

    """

    cv_html = ll_deepseek.invoke([
        SystemMessage(content=rf"""Convierte el siguiente texto con información personal en un documento HTML para un currículum vitae con un diseño de dos columnas **y responde únicamente con la cadena HTML**, sin ningún texto adicional.

🔷 Estructura del diseño:
- **Columna izquierda (cinta vertical):** datos de contacto, habilidades y educación.
- **Columna derecha:** nombre completo, breve descripción personal (“Acerca de mí”), experiencia laboral e información adicional útil.

🎨 Estilo visual:
- Tipografía clara (Arial o sans‑serif).
- Paleta de colores basada en azul oscuro (#153C62) y blanco.
- Nombre completo en grande, profesión debajo.
- Separadores limpios (líneas o títulos) para cada sección.
- No incluir imágenes ni recursos externos.

📄 Requisitos técnicos:
- Debe comenzar con `<!DOCTYPE html>` y contener `<html>`, `<head>` y `<body>`.
- Incluir `<meta charset="UTF-8">` en el `<head>`.
- Hoja de estilos dentro de `<style>` en el `<head>`, sin enlaces externos.
- Todo el contenido en una **cadena multilínea de Python** usando triple comillas (`""""""`).
- **No usar** `\n`, `\\`, `\"` u otros caracteres de escape.
- Diseño adaptado a A4/carta y listo para PDF con `pdfkit` o `WeasyPrint`.

Ejemplo de uso:
```python
html = \"\"\"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Currículum</title>
    <style> /* estilos aquí */ </style>
</head>
<body>
    <!-- tu contenido en dos columnas -->
</body>
</html>
\"\"\"

📌 Recuerda:
- No uses rutas externas ni imágenes.
- El diseño debe adaptarse correctamente a formato carta o A4.
- Debes mantener un balance visual entre ambas columnas.

No respondas nada mas aparte del html, Puedes usar el siguiente ejemplo como base para construir la estructura:  
`{html}`
"""),
        HumanMessage(content=cv)
    ])

    # Función para limpiar saltos de línea
    def limpiar_saltos_linea(texto):
        """
        Reemplaza todos los saltos de línea por espacios en blanco
        Args:
            texto (str): Texto a limpiar
        Returns:
            str: Texto sin saltos de línea
        """
        return texto.replace('\n', ' ')

    # Aplicar la limpieza al cv_html
    cv_html = limpiar_saltos_linea(cv_html.content)

    print(f"CV HTML: {cv_html}")
    pdfkit.from_string(cv_html, output_dir, configuration=config)

if __name__ == "__main__":
    creador_pdf()
#     # Ejecutar la función principal o cualquier otra lógica aquí