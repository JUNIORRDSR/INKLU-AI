from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_tavily import TavilySearch

memory = MemorySaver()
model = ChatDeepSeek(model="deepseek-chat")
search = TavilySearch(max_results=5)

@tool
def conversador(texto: str) -> str:
    """
    Función que permite mantener una conversación con el usuario sobre cualquier tema.
    
    Args:
        texto (str): El texto o pregunta del usuario.
    
    Returns:
        str: La respuesta del asistente.
    """
    messages = [
        (
            "system",
            "Eres un asistente amigable y conversacional que responde de manera informativa, útil y educada a cualquier consulta del usuario. Mantén un tono cordial y proporciona respuestas detalladas cuando sea apropiado."
        ),
        ("human", texto),
    ]
    
    ai_msg = llm_conversador.invoke(messages)
    return ai_msg

@tool
def buscador(consulta: str) -> str:
    """
    Función que busca información en la web sobre la consulta del usuario.
    
    Args:
        consulta (str): La consulta de búsqueda del usuario.
    
    Returns:
        str: Resultados de la búsqueda web.
    """
    # Usamos TavilySearch que ya está importado
    search_results = search.invoke(consulta)
    
    # Formateamos los resultados para hacer una respuesta más coherente
    messages = [
        (
            "system",
            "Eres un asistente de investigación que sintetiza información de búsquedas web. Resume los resultados de manera clara y concisa."
        ),
        ("human", f"Aquí están los resultados de búsqueda para '{consulta}': {search_results}. Por favor, resume esta información de manera útil."),
    ]
    
    ai_msg = llm_buscador.invoke(messages)
    return ai_msg

llm_controler = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

llm_buscador = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)

llm_conversador = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek"
)


tool = [conversador, buscador]

# Define un mensaje de sistema específico para el controlador
system_message = SystemMessage("""Eres un asistente útil que tiene acceso a las siguientes herramientas:
- coversador: para mantener conversaciones
- buscador: para busar información en la web

Si el usuario solicita una tarea que no puede realizarse con estas herramientas, 
debes responder claramente: "Lo siento, no tengo una herramienta para realizar esa tarea específica. 
Solo puedo ayudarte con traducciones o reescritura de textos en diferentes estilos." y terminar la conversación.

Utiliza las herramientas disponibles cuando sea apropiado.
""")

# Modifica la creación del agente para incluir el mensaje del sistema
agente_controlador = create_react_agent(
    llm_controler,
    tool,
    prompt=system_message  # Añade el mensaje del sistema
)

async def procesar_solicitud(mensaje: str) -> dict:
    """
    Procesa la solicitud del usuario y devuelve una respuesta del agente de forma asíncrona.
    
    Args:
        mensaje (str): El mensaje del usuario a procesar.
        
    Returns:
        Dict[str, Any]: Un diccionario con la respuesta del agente.
    """
    try:
        # Asegúrate de convertir el input a un objeto HumanMessage
        input_message = [HumanMessage(content=mensaje)]
        
        # Variable para almacenar la respuesta final
        final_response = None
        
        # Invocar al agente para obtener la respuesta de forma asíncrona
        response = await agente_controlador.ainvoke({"messages": input_message})
        
        # Extraer el contenido de la respuesta
        if response and "messages" in response and response["messages"]:
            final_content = response["messages"][-1].content
            final_response = {
                "status": "success",
                "message": final_content,
                "input": mensaje
            }
        else:
            # Si no hay respuesta adecuada, crear una respuesta genérica
            final_response = {
                "status": "success",
                "message": "He recibido tu mensaje pero no pude procesar una respuesta específica. ¿Podrías formular la pregunta de otra manera?",
                "input": mensaje
            }
        
        return final_response
        
    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return {
            "status": "error",
            "message": f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}",
            "error_details": str(e),
            "input": mensaje
        }