from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from dotenv import load_dotenv
from AgenteBusqueda import buscar_oportunidades
from creador_cv import crear_cv
import os
load_dotenv()

llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

tool = [buscar_oportunidades, crear_cv]

react_agent = create_react_agent(
    model=llm,
    tools=tool,
    prompt=SystemMessage(content="""Eres un agente central responsable de enrutar correctamente las solicitudes del usuario. Tu única tarea es elegir entre dos herramientas disponibles según el contenido del mensaje del usuario:

Herramienta "Generar CV": Úsala si el usuario proporciona información personal relacionada con la creación de una hoja de vida (nombre, habilidades, experiencia laboral, educación, etc.).

Herramienta "Buscar Oportunidades": Úsala si el usuario manifiesta interés en encontrar trabajo, solicitar recomendaciones de empleo o quiere explorar oportunidades laborales.

📌 Si el mensaje del usuario no encaja en ninguna de estas dos categorías, responde de manera breve y amable diciendo:
"Lo siento, en este momento no tengo acceso a esa función. Solo puedo ayudarte a crear tu hoja de vida o a buscar oportunidades laborales. ¡Gracias por entender!"

🔒 Nunca debes generar respuestas personalizadas fuera de las funciones anteriores."""),
)

input_text = input("Escribe tu mensaje: ")
message = HumanMessage(content=input_text)

# Invocar el agente con el formato correcto
output = react_agent.invoke(
    {"messages": message}
)
try:
    for step in react_agent.stream(
        {"messages": message},
        stream_mode="values",
    ):
        resultado = step["messages"][-1]
        resultado.pretty_print()
except Exception as e:
        print(f"Error: {e}")
        resultado = None