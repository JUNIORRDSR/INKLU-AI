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
    prompt=SystemMessage(content="""Eres un asistente que analiza las entradas del usuario para detectar si contienen información personal útil para construir una hoja de vida o revisa si el usuario necesita buscar informacion sobre ."""),
)

input = "Quiero buscar oportunidades de trabajo en el área de IA. ¿Puedes ayudarme?"
output = react_agent.invoke(input)
print(output)