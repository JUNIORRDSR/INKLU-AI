from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
import speech_recognition as sr
from dotenv import load_dotenv
import os
load_dotenv()

llm_orquestador = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
)

llm_por_voz = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

llm_respondedor = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

@tool
def audio_texto() -> str:
    """
    Funcion para convertir audio a texto utilizando la tool de SpeechRecognition."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='es-ES')
            print("Texto:", text)
            response = llm_por_voz.invoke([
                SystemMessage(content="Eres un asistente de voz que recibe el audio del usuario en formato de texto y arreglas los posibles errores gramaticales y de sintaxis que se generen en el proceso de conversion."),
                HumanMessage(content=text)
            ])
            response = respondedor(response)
            return response
        except Exception as e:
            return  print("Error:", e)

@tool
def respondedor(text: str) -> str:
    """
    Funcion para responder a un texto utilizando el modelo Gemini.
    Args:
        text (str): El texto al que se respondera."""
    return llm_respondedor.invoke([
        SystemMessage(content="Eres un asistente de voz que responde a las preguntas del usuario."),
        HumanMessage(content=text)
    ])
tool = [audio_texto]
agent = create_react_agent(
    llm_orquestador,
    tool,
    prompt=SystemMessage(content="Eres un asistente de voz que responde a las preguntas del usuario, cuando se te llame tienes que activar el tool de `audio_texto` ."),
)
message = HumanMessage(content="quiero hablar por voz")

for step in agent.stream(
    {"messages": message},  # Usa el mensaje formateado correctamente
    stream_mode="values",
):
    # Imprime el mensaje completo para depuración   
    step["messages"][-1].pretty_print()
