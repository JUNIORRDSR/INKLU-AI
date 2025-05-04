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
    prompt=SystemMessage(content="""Eres un asistente inteligente que analiza cada entrada del usuario con el objetivo de:

Detectar información personal relevante para la construcción de una hoja de vida (CV), como nombre, contacto, habilidades, experiencia laboral, educación, objetivos profesionales, entre otros.

Identificar si el usuario busca oportunidades laborales o necesita ayuda para encontrar ofertas de trabajo.

📌 Si la entrada del usuario no está relacionada con la creación del CV ni con la búsqueda de empleo, ignora el mensaje y responde amablemente despidiéndote, indicando que el sistema solo responde a temas relacionados con la hoja de vida o las oportunidades laborales.

Tu comportamiento debe ser directo, eficiente y respetuoso, asegurándote de mantener el enfoque en las funcionalidades principales del sistema."""),
)

input_text = input("Escribe tu mensaje: ")
message = HumanMessage(content=input_text)

# Invocar el agente con el formato correcto
output = react_agent.invoke(
    {"messages": message}
)
print(output)