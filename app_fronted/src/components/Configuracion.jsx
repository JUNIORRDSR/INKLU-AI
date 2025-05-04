import React, { useState } from 'react';
import Header from './header';
import { useTheme } from '../../contexts/ThemeContext';

const Configuracion = () => {
  const { darkMode, toggleDarkMode } = useTheme();
  const [activeTab, setActiveTab] = useState('perfil');
  const [formData, setFormData] = useState({
    // Datos personales
    nombre: 'María',
    apellido: 'González',
    email: 'maria.gonzalez@email.com',
    telefono: '3001234567',
    ciudad: 'Bogotá',
    
    // Perfil profesional
    profesion: 'Diseñadora Gráfica',
    experiencia: '3 años',
    habilidades: 'Illustrator, Photoshop, InDesign, UI/UX',
    
    // Información sobre discapacidad
    tieneDiscapacidad: true,
    tipoDiscapacidad: 'visual',
    gradoDiscapacidad: 'moderado',
    necesidadesEspeciales: 'Software lector de pantalla, documentos con alto contraste',
    
    // Preferencias
    notificacionesEmail: true,
    notificacionesTelefono: false,
    temasOscuro: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Aquí iría la lógica para guardar los cambios en el backend
    alert('Configuración guardada correctamente');
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} transition-colors duration-300`}>
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <main className="container mx-auto px-4 pt-24 pb-12">
        <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-azulmio'} mb-6`}>Configuración</h1>
        
        {/* Tabs de navegación */}
        <div className={`flex border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'} mb-6`}>
          <button
            className={`py-3 px-4 font-medium text-sm border-b-2 ${
              activeTab === 'perfil' 
                ? 'border-moradomio text-moradomio' 
                : `border-transparent ${darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700'}`
            }`}
            onClick={() => setActiveTab('perfil')}
          >
            Perfil Personal
          </button>
          <button
            className={`py-3 px-4 font-medium text-sm border-b-2 ${
              activeTab === 'profesional' 
                ? 'border-moradomio text-moradomio' 
                : `border-transparent ${darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700'}`
            }`}
            onClick={() => setActiveTab('profesional')}
          >
            Perfil Profesional
          </button>
          <button
            className={`py-3 px-4 font-medium text-sm border-b-2 ${
              activeTab === 'accesibilidad' 
                ? 'border-moradomio text-moradomio' 
                : `border-transparent ${darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700'}`
            }`}
            onClick={() => setActiveTab('accesibilidad')}
          >
            Accesibilidad
          </button>
          <button
            className={`py-3 px-4 font-medium text-sm border-b-2 ${
              activeTab === 'preferencias' 
                ? 'border-moradomio text-moradomio' 
                : `border-transparent ${darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700'}`
            }`}
            onClick={() => setActiveTab('preferencias')}
          >
            Preferencias
          </button>
        </div>
        
        {/* Formulario de configuración */}
        <form onSubmit={handleSubmit} className={`${darkMode ? 'bg-gray-800 text-gray-200' : 'bg-white text-gray-700'} rounded-lg shadow-md p-6`}>
          {/* Sección de Perfil Personal */}
          {activeTab === 'perfil' && (
            <div className="space-y-4">
              <h2 className={`text-xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-4`}>Perfil Personal</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Nombre</label>
                  <input
                    type="text"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleChange}
                    className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                  />
                </div>
                
                <div>
                  <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Apellido</label>
                  <input
                    type="text"
                    name="apellido"
                    value={formData.apellido}
                    onChange={handleChange}
                    className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                  />
                </div>
                
                <div>
                  <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                  />
                </div>
                
                <div>
                  <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Teléfono</label>
                  <input
                    type="tel"
                    name="telefono"
                    value={formData.telefono}
                    onChange={handleChange}
                    className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                  />
                </div>
                
                <div>
                  <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Ciudad</label>
                  <input
                    type="text"
                    name="ciudad"
                    value={formData.ciudad}
                    onChange={handleChange}
                    className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                  />
                </div>
              </div>
            </div>
          )}
          
          {/* Sección de Perfil Profesional */}
          {activeTab === 'profesional' && (
            <div className="space-y-4">
              <h2 className={`text-xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-4`}>Perfil Profesional</h2>
              
              <div>
                <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Profesión</label>
                <input
                  type="text"
                  name="profesion"
                  value={formData.profesion}
                  onChange={handleChange}
                  className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                />
              </div>
              
              <div>
                <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Experiencia</label>
                <input
                  type="text"
                  name="experiencia"
                  value={formData.experiencia}
                  onChange={handleChange}
                  className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                />
              </div>
              
              <div>
                <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Habilidades</label>
                <textarea
                  name="habilidades"
                  value={formData.habilidades}
                  onChange={handleChange}
                  rows="3"
                  className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                  placeholder="Separa las habilidades con comas"
                />
              </div>
            </div>
          )}
          
          {/* Sección de Accesibilidad */}
          {activeTab === 'accesibilidad' && (
            <div className="space-y-4">
              <h2 className={`text-xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-4`}>Configuración de Accesibilidad</h2>
              
              <div>
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    name="tieneDiscapacidad"
                    checked={formData.tieneDiscapacidad}
                    onChange={handleChange}
                    className="mt-1 accent-moradomio"
                  />
                  <span className="ml-2">Tengo una discapacidad</span>
                </label>
              </div>
              
              {formData.tieneDiscapacidad && (
                <>
                  <div>
                    <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Tipo de discapacidad</label>
                    <select
                      name="tipoDiscapacidad"
                      value={formData.tipoDiscapacidad}
                      onChange={handleChange}
                      className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                    >
                      <option value="visual">Visual</option>
                      <option value="auditiva">Auditiva</option>
                      <option value="motriz">Motriz</option>
                      <option value="cognitiva">Cognitiva</option>
                      <option value="otra">Otra</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Grado</label>
                    <select
                      name="gradoDiscapacidad"
                      value={formData.gradoDiscapacidad}
                      onChange={handleChange}
                      className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                    >
                      <option value="leve">Leve</option>
                      <option value="moderado">Moderado</option>
                      <option value="severo">Severo</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className={`block ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-2`}>Necesidades especiales o adaptaciones</label>
                    <textarea
                      name="necesidadesEspeciales"
                      value={formData.necesidadesEspeciales}
                      onChange={handleChange}
                      rows="3"
                      className={`w-full p-3 border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'} rounded-md focus:outline-none focus:ring-2 focus:ring-azulmio`}
                      placeholder="Describe tus necesidades específicas..."
                    />
                  </div>
                </>
              )}
            </div>
          )}
          
          {/* Sección de Preferencias */}
          {activeTab === 'preferencias' && (
            <div className="space-y-4">
              <h2 className={`text-xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-4`}>Preferencias</h2>
              
              <div>
                <h3 className={`font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-3`}>Notificaciones</h3>
                
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      name="notificacionesEmail"
                      checked={formData.notificacionesEmail}
                      onChange={handleChange}
                      className="accent-moradomio"
                    />
                    <span className="ml-2">Recibir notificaciones por email</span>
                  </label>
                  
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      name="notificacionesTelefono"
                      checked={formData.notificacionesTelefono}
                      onChange={handleChange}
                      className="accent-moradomio"
                    />
                    <span className="ml-2">Recibir notificaciones por teléfono</span>
                  </label>
                </div>
              </div>
              
              <div>
                <h3 className={`font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-3`}>Apariencia</h3>
                
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="temasOscuro"
                    checked={darkMode}
                    onChange={toggleDarkMode}
                    className="accent-moradomio"
                  />
                  <span className="ml-2">Tema oscuro</span>
                </label>
              </div>
            </div>
          )}
          
          <div className="mt-6 flex justify-end">
            <button
              type="submit"
              className="bg-gradient-to-r from-azulmio to-moradomio text-white font-semibold py-3 px-6 rounded-md hover:brightness-110 transition shadow-lg"
            >
              Guardar Cambios
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default Configuracion; 