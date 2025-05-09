from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from dotenv import load_dotenv
from xhtml2pdf import pisa
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
    Funcion para extraer datos claves de un texto que sirvan para armar cvGenerados, la respuesta funciona tanto en json.
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
    """
    Crea un archivo PDF con un currículum vitae a partir de datos proporcionados.

    Esta función realiza las siguientes operaciones:
    1. Procesa los datos del usuario mediante un agente conversacional
    2. Extrae información relevante del CV
    3. Genera un documento HTML con diseño responsivo de dos columnas
    4. Convierte el HTML a PDF con xhtml2pdf y lo guarda en la carpeta 'cvGenerados'

    Requisitos:
    - Módulo xhtml2pdf instalado (pip install xhtml2pdf)
    - Acceso a modelos de lenguaje (DeepSeek y Google Gemini)
    - Permisos de escritura en el directorio de salida

    Returns:
        None: La función guarda el PDF directamente en el sistema de archivos

    Raises:
        Exception: Si hay errores en la generación del HTML o conversión a PDF
    """

    # Definir la ruta de salida del PDF
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "doc/cvGenerados")
    output_file = os.path.join(output_dir, "cv.pdf")
    
    # Asegurar que el directorio existe
    os.makedirs(output_dir, exist_ok=True)
    
    ejemplo_cv = """
    # [El mismo contenido de ejemplo_cv que ya tienes]
    """

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
        {"messages": message},
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículum Vitae - Zara Pérez</title>
    <style>
        @page {
            size: A4;
            margin: 0;
        }
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f6f8;
            color: #333;
            line-height: 1.6;
        }
        .container {
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            display: flex;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .left-column {
            width: 35%;
            background: linear-gradient(135deg, #153C62 0%, #1E5689 100%);
            color: white;
            padding: 30px;
            position: relative;
        }
        .right-column {
            width: 65%;
            background-color: white;
            padding: 40px;
        }
        h1 {
            font-size: 36px;
            margin: 0 0 10px;
            color: #153C62;
            font-weight: 700;
        }
        h2 {
            font-size: 20px;
            color: #153C62;
            border-bottom: 2px solid #153C62;
            padding-bottom: 8px;
            margin: 30px 0 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .left-column h2 {
            color: white;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        .section {
            margin-bottom: 25px;
        }
        .info-label {
            font-weight: 600;
            display: inline-block;
            width: 80px;
        }
        .contact-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .contact-item i {
            margin-right: 10px;
            color: #ffffff;
        }
        ul {
            padding-left: 20px;
            margin: 10px 0;
        }
        ul li {
            margin-bottom: 8px;
            font-size: 14px;
        }
        .left-column ul li {
            list-style-type: none;
            position: relative;
            padding-left: 20px;
        }
        .left-column ul li:before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #ffffff;
        }
        .education-item p {
            margin: 5px 0;
        }
        .job-title {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .job-period {
            font-style: italic;
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .profile-photo {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto 20px;
            border: 3px solid white;
            display: none; /* Placeholder for photo */
        }
        .profile-photo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        @media print {
            body {
                background: none;
            }
            .container {
                box-shadow: none;
            }
        }
        @media screen and (max-width: 768px) {
            .container {
                flex-direction: column;
                width: 100%;
            }
            .left-column, .right-column {
                width: 100%;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-column">
            <div class="profile-photo">
                <!-- Placeholder for profile photo -->
                <!-- <img src="profile.jpg" alt="Profile Photo"> -->
            </div>
            <h2>Contacto</h2>
            <div class="contact-item">
                <i class="fas fa-envelope"></i>
                <p><span class="info-label">Email:</span> zara@mail.com</p>
            </div>
            <div class="contact-item">
                <i class="fas fa-phone"></i>
                <p><span class="info-label">Tel:</span> +57 300 000 0000</p>
            </div>

            <h2>Habilidades</h2>
            <ul>
                <li>Comunicación</li>
                <li>Trabajo en equipo</li>
                <li>Adaptabilidad</li>
                <li>Resolución de problemas</li>
            </ul>

            <h2>Educación</h2>
            <div class="education-item">
                <p><strong>Universidad Ejemplo</strong></p>
                <p>Ingeniería de Sistemas</p>
                <p>2018 - 2022</p>
            </div>
        </div>
        <div class="right-column">
            <h1>Zara Pérez</h1>
            <h2>Desarrolladora Full Stack</h2>

            <div class="section">
                <h2>Acerca de mí</h2>
                <p>Soy una profesional apasionada por la tecnología, con experiencia en el desarrollo de soluciones web y un enfoque orientado al detalle. Mi objetivo es crear aplicaciones eficientes y de alta calidad que resuelvan problemas reales.</p>
            </div>

            <div class="section">
                <h2>Experiencia Laboral</h2>
                <div class="job">
                    <p class="job-title">Desarrolladora Web - Tech Solutions</p>
                    <p class="job-period">2023 - Presente</p>
                    <ul>
                        <li>Desarrollo de aplicaciones con React y Node.js, optimizando la experiencia del usuario.</li>
                        <li>Implementación de buenas prácticas de desarrollo y CI/CD.</li>
                        <li>Colaboración con equipos multidisciplinarios para entregar proyectos a tiempo.</li>
                    </ul>
                </div>
                <div class="job">
                    <p class="job-title">Practicante - SoftDev</p>
                    <p class="job-period">2022</p>
                    <ul>
                        <li>Apoyo en el desarrollo de backend con Python y Flask.</li>
                        <li>Participación en la documentación de APIs REST.</li>
                    </ul>
                </div>
            </div>

            <div class="section">
                <h2>Información Adicional</h2>
                <p>Disponible para trabajar de forma remota o presencial. Comprometida con el aprendizaje continuo y la entrega de resultados de alta calidad. Alto nivel de ética profesional.</p>
            </div>
        </div>
    </div>
    <script src="https://kit.fontawesome.com/a076d05399.js"></script>
</body>
</html>
    """

    cv_html = ll_deepseek.invoke([
        SystemMessage(content=rf"""Necesito que repliques EXACTAMENTE la estructura HTML proporcionada a continuación y simplemente reemplaces los datos de ejemplo con los del currículum del usuario.
        
        IMPORTANTE: 
        1. Mantén TODA la estructura HTML, clases, estilos y formato exactamente igual al ejemplo
        2. NO cambies ningún aspecto del diseño o estilo CSS
        3. Solo reemplaza el contenido informativo (nombre, contacto, habilidades, etc.) con los datos del CV
        4. Conserva todos los elementos como iconos, estructura de columnas y secciones

        Aquí está la plantilla HTML que debes usar y solo reemplazar los datos:
        {html}
        
        Por favor, utiliza los datos del CV proporcionado y colócalos en la plantilla HTML anterior, manteniendo EXACTAMENTE la misma estructura, diseño y estilo. Responde únicamente con el HTML resultante, sin ningún texto adicional.
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
    cv_html_limpio = cv_html.content
    
    # Guardar el HTML temporalmente (opcional para inspección)
    temp_html_path = os.path.join(output_dir, "temp_cv.html")
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(cv_html_limpio)
    
    try:
        # Abrir el archivo PDF para escritura en modo binario
        with open(output_file, "wb") as pdf_file:
            # Convertir HTML a PDF directamente
            pisa_status = pisa.CreatePDF(
                cv_html_limpio,               # Contenido HTML
                dest=pdf_file,                # Archivo de salida
                encoding='utf-8'              # Codificación
            )
        
        # Verificar si la conversión fue exitosa
        if pisa_status.err:
            print(f"Error al generar el PDF: {pisa_status.err}")
        else:
            print(f"PDF generado correctamente en: {output_file}")
    
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
    
    finally:
        # Dejar el HTML temporal para inspección (opcional eliminarlo)
        # Si deseas eliminarlo, descomenta la siguiente línea:
        # if os.path.exists(temp_html_path):
        #     os.remove(temp_html_path)
        pass

if __name__ == "__main__":
    
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
    creador_pdf()