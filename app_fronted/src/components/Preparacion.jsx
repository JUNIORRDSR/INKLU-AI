import React, { useState } from 'react';
import Header from './header';
import { useTheme } from '../../contexts/ThemeContext';

const Preparacion = () => {
  const { darkMode, toggleDarkMode } = useTheme();
  const [categoriaActiva, setCategoriaActiva] = useState('todos');

  // Recursos simulados para empleo público
  const recursos = [
    {
      id: 1,
      titulo: '¿Qué es una nómina?',
      descripcion: 'Aprende sobre los componentes básicos de una nómina y cómo se calculan los diferentes conceptos.',
      categoria: 'conceptos',
      icono: '📝',
      fecha: '2023-10-15',
    },
    {
      id: 2,
      titulo: 'Tipos de contratos en el sector público',
      descripcion: 'Guía completa sobre los diferentes tipos de contratos en entidades públicas.',
      categoria: 'contratos',
      icono: '📄',
      fecha: '2023-10-20',
    },
    {
      id: 3,
      titulo: 'Cómo preparar una entrevista para empleo público',
      descripcion: 'Consejos y preguntas frecuentes en entrevistas para puestos en el sector público.',
      categoria: 'entrevistas',
      icono: '👥',
      fecha: '2023-10-25',
    },
    {
      id: 4,
      titulo: 'Derechos laborales para personas con discapacidad',
      descripcion: 'Todo lo que necesitas saber sobre tus derechos en el entorno laboral.',
      categoria: 'derechos',
      icono: '⚖️',
      fecha: '2023-11-01',
    },
    {
      id: 5,
      titulo: 'Glosario de términos administrativos',
      descripcion: 'Vocabulario esencial para entender documentos y procesos administrativos.',
      categoria: 'conceptos',
      icono: '📚',
      fecha: '2023-11-05',
    },
    {
      id: 6,
      titulo: 'Procesos de selección en entidades públicas',
      descripcion: 'Etapas y requisitos comunes en los procesos de selección del sector público.',
      categoria: 'entrevistas',
      icono: '🔍',
      fecha: '2023-11-08',
    }
  ];

  // Filtrar recursos por categoría
  const recursosFiltrados = categoriaActiva === 'todos' 
    ? recursos 
    : recursos.filter(recurso => recurso.categoria === categoriaActiva);

  // Categorías para el filtro
  const categorias = [
    { id: 'todos', nombre: 'Todos' },
    { id: 'conceptos', nombre: 'Conceptos básicos' },
    { id: 'contratos', nombre: 'Contratos' },
    { id: 'entrevistas', nombre: 'Entrevistas' },
    { id: 'derechos', nombre: 'Derechos' }
  ];

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} transition-colors duration-300`}>
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <main className="container mx-auto px-4 pt-24 pb-12">
        <div className="mb-8">
          <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-azulmio'} mb-4`}>Preparación para Empleo Público</h1>
          <p className={`text-lg ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Recursos y guías para ayudarte a preparar tus postulaciones y entender mejor el entorno laboral público.
          </p>
        </div>

        {/* Filtros por categoría */}
        <div className="flex flex-wrap gap-2 mb-8">
          {categorias.map(categoria => (
            <button
              key={categoria.id}
              onClick={() => setCategoriaActiva(categoria.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                categoriaActiva === categoria.id
                  ? 'bg-moradomio text-white' 
                  : darkMode 
                    ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {categoria.nombre}
            </button>
          ))}
        </div>

        {/* Lista de recursos */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recursosFiltrados.map(recurso => (
            <div key={recurso.id} className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow`}>
              <div className="p-6">
                <div className="text-4xl mb-4">{recurso.icono}</div>
                <h3 className={`text-xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-2`}>{recurso.titulo}</h3>
                <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mb-4`}>{recurso.descripcion}</p>
                <div className="flex justify-between items-center">
                  <span className={`inline-block ${darkMode ? 'bg-purple-900 text-purple-300' : 'bg-purple-100 text-moradomio'} text-xs px-2 py-1 rounded-full`}>
                    {categorias.find(cat => cat.id === recurso.categoria)?.nombre}
                  </span>
                  <button className={`${darkMode ? 'text-purple-300 hover:text-blue-300' : 'text-moradomio hover:text-azulmio'} font-medium transition-colors`}>
                    Leer más →
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Preparacion; 