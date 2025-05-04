# Importar funciones principales para exponer en la API del paquete
from .AgenteBusqueda import buscar_oportunidades
from .creador_cv import estractor_datos, ll_deepseek, orquestador

# Exportar las funciones principales y clases
__all__ = [
    'buscar_oportunidades',  # Función principal del agente de búsqueda
    'estractor_datos',       # Herramienta para extraer datos de CV
    'll_deepseek',           # Modelo DeepSeek para generación de CV
    'orquestador'            # Modelo orquestador para el flujo de trabajo
]