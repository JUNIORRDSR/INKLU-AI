from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

load_dotenv()

def get_key():
    """Obtiene la clave de encriptación desde variables de entorno o genera una nueva"""
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Generar una clave si no existe
        key = Fernet.generate_key().decode()
        # En producción, guardaríamos esta clave en un lugar seguro
        print(f"WARNING: ENCRYPTION_KEY no encontrada. Se generó una nueva clave: {key}")
    return key.encode()

def encrypt_data(data):
    """Encripta datos usando Fernet"""
    if data is None:
        return None
    
    cipher_suite = Fernet(b64encode(get_key()[:32].ljust(32, b'\0')))
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data.decode('utf-8')

def decrypt_data(encrypted_data):
    """Desencripta datos usando Fernet"""
    if encrypted_data is None:
        return None
    
    cipher_suite = Fernet(b64encode(get_key()[:32].ljust(32, b'\0')))
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode('utf-8'))
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Error al desencriptar: {e}")
        return None