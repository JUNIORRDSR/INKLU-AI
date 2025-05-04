import { useState } from 'react';
import axios from 'axios';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

export default async function Register() {
  const [formData, setFormData] = useState({
    Nombre: '',
    Correo: '',
    Contrasena: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/register', formData);
      console.log('Registro exitoso:', response.data);
      navigate('/'); // Redirige al login
    } catch (err) {
      console.error('Error en registro:', err);
      setError(err.response?.data?.error || 'Error al registrar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-8 rounded-lg bg-white p-8 shadow">
        <div>
          <h2 className="text-center text-3xl font-bold text-gray-900">Crea tu cuenta</h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Únete a INKLU para empezar
          </p>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="nombre" className="block text-sm font-medium text-gray-700">
              Nombre completo
            </label>
            <input
              id="nombre"
              name="Nombre"
              type="text"
              required
              value={formData.Nombre}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="correo" className="block text-sm font-medium text-gray-700">
              Correo electrónico
            </label>
            <input
              id="correo"
              name="Correo"
              type="email"
              required
              value={formData.Correo}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="contrasena" className="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <input
              id="contrasena"
              name="Contrasena"
              type="password"
              required
              value={formData.Contrasena}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
            />
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-indigo-300"
            >
              {loading ? 'Registrando...' : 'Registrarse'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  await api.post('/register', {
    Nombre: 'Sara',
    Correo: 'sara@email.com',
    Contrasena: '123456'
  });
}
