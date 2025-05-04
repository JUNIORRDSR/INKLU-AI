import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

export default function Login() {
  const [credentials, setCredentials] = useState({
    Correo: '',
    Contrasena: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const result = await authService.login(credentials);
      console.log('Login exitoso:', result);
      
      // En lugar de redirigir inmediatamente, mostrar el modal
      setShowModal(true);
      setLoading(false);
    } catch (err) {
      console.error('Error en login:', err);
      setError(err.response?.data?.error || 'Error al iniciar sesión');
      setLoading(false);
    }
  };

  // Actualizar la ruta de configuración que actualmente podría estar causando errores
  const handleConfigureProfile = () => {
    setShowModal(false);
    // Verifica si tienes una ruta '/configuracion' definida en App.jsx
    // Si no, actualiza esto a una ruta que exista
    navigate('/dashboard'); // O cualquier ruta válida que tengas
  };

  const handleExploreApp = () => {
    setShowModal(false);
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradiente-animado font-sans">
      <div className="bg-white rounded-2xl shadow-2xl shadow-gray-800/20 flex flex-col md:flex-row w-full max-w-4xl overflow-hidden">
        
        {/* Panel izquierdo */}
        <div className="md:w-1/2 bg-white color-azul p-10 flex flex-col justify-center items-center">
          <img
            src="/inkluazul-remove.png"
            alt="Logo InKlúIA"
            className="w-28 h-28 mb-4 animate-bounce"
          />
          <h2 className="text-4xl font-bold mb-4 leading-tight text-center">
  ¡Bienvenido a <span className="gradiente-texto">InKlú-IA</span>!
</h2>
          <p className="text-md opacity-100 text-center">
            Tu asistente para crear hojas de vida para personas con discapacidad.
          </p>
        </div>

        {/* Panel derecho */}
        <div className="md:w-1/2 p-10 flex flex-col justify-center bg-white">
          <h2 className="text-3xl font-semibold mb-6 color-azul">Iniciar sesión</h2>
          
          {error && (
            <div className="rounded-md bg-red-50 p-4 text-sm text-red-700 mb-4">
              {error}
            </div>
          )}
          
          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <input
              type="email"
              name="Correo"
              placeholder="Correo electrónico"
              value={credentials.Correo}
              onChange={handleChange}
              className="p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio text-azulmio transition-all font-sans"
              required
            />
            <input
              type="password"
              name="Contrasena"
              placeholder="Contraseña"
              value={credentials.Contrasena}
              onChange={handleChange}
              className="p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio text-azulmio transition-all font-sans"
              required
            />
            <button
              type="submit"
              disabled={loading}
              style={{
                background: 'linear-gradient(to right, #002F50, #D508E2)',
                color: 'white',
                padding: '0.75rem 1rem',
                borderRadius: '0.375rem',
                fontWeight: '600',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                transition: 'all 0.3s ease',
                width: '100%'
              }}
              className="hover:shadow-lg transform hover:-translate-y-1 disabled:opacity-70"
            >
              {loading ? 'Iniciando sesión...' : 'Ingresar'}
            </button>
            <p className="text-sm text-center text-gray-600 mt-4 font-sans">
              ¿No tienes cuenta?{' '}
              <Link to="/register" className="text-[#002F50] font-medium hover:underline transition-all">Regístrate</Link>
            </p>
          </form>
        </div>
      </div>

      {/* Modal que aparece después del inicio de sesión */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full relative">
            <button
              onClick={() => setShowModal(false)}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-azulmio mb-4">¡Bienvenido a InKlú-IA!</h2>
              <p className="text-gray-600 mb-6">
                Para mejorar tu experiencia de usuario, configura primero tu perfil. Esto nos ayudará a adaptar la aplicación a tus necesidades y a asegurarnos de que sacas el máximo partido a nuestras funciones.
              </p>
              <div className="flex flex-col gap-3">
                <button
                  onClick={handleConfigureProfile}
                  className="bg-gradient-to-r from-azulmio to-moradomio text-white font-semibold py-2 px-4 rounded-md text-center hover:brightness-110 transition shadow-lg"
                >
                  Configurar perfil
                </button>
                <button
                  onClick={handleExploreApp}
                  className="border border-azulmio text-azulmio font-semibold py-2 px-4 rounded-md hover:bg-azulmio hover:text-white transition"
                >
                  Explorar aplicación
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}