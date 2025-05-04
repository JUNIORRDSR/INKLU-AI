from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet, InvalidToken
from base64 import b64encode, b64decode
import hashlib
import logging

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_key():
    """Obtiene la clave de encriptación desde variables de entorno o genera una nueva"""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Generar una clave si no existe
        key = Fernet.generate_key().decode()
        # En producción, guardaríamos esta clave en un lugar seguro
        logger.warning(f"ENCRYPTION_KEY no encontrada. Se generó una nueva clave: {key}")
    return key.encode()

def encrypt_data(data):
    """Encripta datos sensibles"""
    if data is None:
        return None
    
    # Convertir a string si no lo es
    if not isinstance(data, str):
        data = str(data)
    
    try:
        # Versión con prefijo para mejor identificación
        key = get_key()
        f = Fernet(key)
        encrypted = f.encrypt(data.encode()).decode()
        return f"FERNET:{encrypted}"
    except Exception as e:
        logger.error(f"Error al encriptar: {e}")
        # Como fallback, usar una versión simple para no bloquear el desarrollo
        hashed = hashlib.md5(data.encode()).hexdigest()
        return f"MD5:{hashed}"

def decrypt_data(encrypted_data):
    """Desencripta datos según varios formatos posibles"""
    if encrypted_data is None:
        logger.debug("Se intentó desencriptar un valor nulo")
        return None
    
    # Registrar para debugging el valor que se está intentando desencriptar
    logger.debug(f"Intentando desencriptar: {encrypted_data[:10]}...")
    
    # Caso 1: Prefijo FERNET (formato actual)
    if encrypted_data.startswith("FERNET:"):
        try:
            key = get_key()
            f = Fernet(key)
            encrypted_part = encrypted_data[7:]  # Quitar el prefijo "FERNET:"
            decrypted = f.decrypt(encrypted_part.encode()).decode()
            return decrypted
        except InvalidToken:
            logger.error("Token Fernet inválido, posiblemente la clave cambió")
            return f"[Error: token inválido]"
        except Exception as e:
            logger.error(f"Error al desencriptar formato FERNET: {e}")
            return f"[Error: {str(e)[:30]}...]"
    
    # Caso 2: Prefijo MD5 (formato fallback)
    elif encrypted_data.startswith("MD5:"):
        # MD5 es un hash, no se puede desencriptar
        logger.warning("Usando valor hasheado con MD5 (no desencriptable)")
        return f"[Correo protegido: {encrypted_data[4:10]}...]"
    
    # Caso 3: Hash MD5 sin prefijo (versión temporal anterior)
    elif len(encrypted_data) == 32 and all(c in '0123456789abcdef' for c in encrypted_data.lower()):
        logger.warning("Detectado hash MD5 sin prefijo")
        return f"[Correo protegido: {encrypted_data[:6]}...]"
    
    # Caso 4: Valor Fernet sin prefijo (versión anterior)
    else:
        try:
            # Intentar con Fernet directamente
            key = get_key()
            f = Fernet(key)
            decrypted = f.decrypt(encrypted_data.encode()).decode()
            return decrypted
        except Exception as e1:
            # Si falla, intentar con la versión anterior que usaba padding
            try:
                cipher_suite = Fernet(b64encode(get_key()[:32].ljust(32, b'\0')))
                decrypted = cipher_suite.decrypt(encrypted_data.encode()).decode()
                return decrypted
            except Exception as e2:
                logger.error(f"Todos los intentos de desencriptación fallaron: {e1}, {e2}")
                # En último caso, devolver el valor tal cual está en la BD
                return encrypted_data