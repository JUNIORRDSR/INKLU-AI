import os
import json
import requests
from datetime import datetime

# Claves API
GOOGLE_API_KEY = "AIzaSyAOTe90o1H7mJAS5Yp5bqWWe7fprpMbw0A"
GOOGLE_CSE_ID = "20376f21087844b39"
DEEPSEEK_API_KEY = "sk-298c3047ada34bcfa3e7a1a3ad387d3a"

def buscar_en_google(query, num=10):
    """
    Realiza una búsqueda en Google usando la API de Custom Search
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
        'num': num
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levantará una excepción si hay un error HTTP
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error en la búsqueda de Google: {response.status_code}")
        print(f"Respuesta de error: {response.text}")
        return None

def analizar_con_deepseek_api(resultados_busqueda):
    """
    Utiliza la API de DeepSeek para analizar los resultados mediante solicitud HTTP directa
    """
    if not resultados_busqueda or 'items' not in resultados_busqueda:
        return {"error": "No se encontraron resultados para analizar"}
    
    # Preparar datos para enviar a DeepSeek
    enlaces = []
    for item in resultados_busqueda.get('items', []):
        enlaces.append({
            'titulo': item.get('title', ''),
            'enlace': item.get('link', ''),
            'fragmento': item.get('snippet', '')
        })
    
    # Prepara el prompt para DeepSeek
    prompt = f"""
    Analiza los siguientes resultados de búsqueda sobre ofertas de trabajo para personas con discapacidad:
    
    {json.dumps(enlaces, indent=2, ensure_ascii=False)}
    
    1. Identifica qué ofertas son específicamente para personas con discapacidad
    2. Extrae información relevante: puesto, empresa, ubicación, requisitos, tipo de discapacidad aceptada (si se menciona)
    3. Clasifica las ofertas por tipo de trabajo y nivel de experiencia requerido
    4. Proporciona recomendaciones sobre qué ofertas parecen más inclusivas y accesibles
    
    Devuelve la información estructurada en formato JSON.
    """
    
    # URL de la API de DeepSeek
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # Cabeceras para la solicitud
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    # Datos de la solicitud
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres un asistente especializado en analizar ofertas de empleo para personas con discapacidad."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Procesar la respuesta
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return json.loads(result["choices"][0]["message"]["content"])
        else:
            return {"error": "No se recibió una respuesta válida de DeepSeek"}
            
    except Exception as e:
        print(f"Error al analizar con DeepSeek API: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Respuesta de error: {e.response.text}")
        return {"error": f"Error al analizar con DeepSeek API: {str(e)}"}

def main(Consulta: str) -> str: 
    # Crear diferentes consultas para encontrar trabajos para personas con discapacidad
    
    consultas = [
        Consulta,
    ]

    todos_resultados = []
    resultados_analizados = {}
    
    for consulta in consultas:
        print(f"Buscando: '{consulta}'...")
        resultados_google = buscar_en_google(consulta)
        
        if resultados_google:
            todos_resultados.append({
                "consulta": consulta,
                "resultados": resultados_google
            })
            
            print("Analizando resultados con DeepSeek API...")
            analisis = analizar_con_deepseek_api(resultados_google)
            resultados_analizados[consulta] = analisis
    
    # Guardar resultados
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    resultado_final = {
        "fecha_busqueda": fecha_actual,
        "resultados_crudos": todos_resultados,
        "analisis_ia": resultados_analizados
    }
    
    with open("trabajos_discapacidad.json", "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)
    
    print("Resultados guardados en trabajos_discapacidad.json")
    print(json.dumps(resultado_final, ensure_ascii=False))

if __name__ == "__main__":
    main('Buscar trabajos para personas con discapacidad')