from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

# Crear el blueprint para las páginas de visualización
viewpages_bp = Blueprint('viewpages', __name__)

# Ruta de inicio - redirecciona a login si no está autenticado o a dashboard si lo está
@viewpages_bp.route('/')
def index():
    """Ruta principal que redirecciona según el estado de autenticación"""
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    return redirect(url_for('viewpages.login'))

# Rutas de autenticación
@viewpages_bp.route('/login')
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    return render_template('login.html')

@viewpages_bp.route('/signup')
def signup():
    """Página de registro de usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    return render_template('signup.html')

@viewpages_bp.route('/reset-password-request')
def reset_password_request():
    """Página para solicitar restablecimiento de contraseña"""
    return render_template('reset-password-request.html')

@viewpages_bp.route('/reset-password/<token>')
def reset_password(token):
    """Página para establecer nueva contraseña"""
    # El token se puede validar en el frontend o backend según tu diseño
    return render_template('reset-password.html')

# Rutas protegidas (requieren autenticación)
@viewpages_bp.route('/dashboard')
def dashboard():
    """Panel de control principal"""
    return render_template('dashboard.html')

@viewpages_bp.route('/chat')
def chat():
    """Página del chat con IA"""
    return render_template('chat.html')
