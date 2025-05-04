import React, { useState } from 'react';
import Header from './header';
import { useTheme } from '../../contexts/ThemeContext';
import { XMarkIcon } from '@heroicons/react/24/outline';

const Inicio = () => {
  const { darkMode, toggleDarkMode } = useTheme();
  const [selectedOferta, setSelectedOferta] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // Datos simulados de ofertas de trabajo
  const ofertas = [
    {
      id: 1,
      titulo: 'Analista de Datos',
      empresa: 'DataTech Solutions',
      ubicacion: 'Bogotá, Colombia',
      tipoContrato: 'Tiempo completo',
      descripcion: 'Buscamos analista de datos con experiencia en Python y SQL.',
      fechaPublicacion: '2023-11-10',
      horario: 'Lunes a viernes de 8:00 AM a 5:00 PM',
      salario: '$2.500.000 - $3.500.000 COP',
      discapacidades: ['Visual (baja visión)', 'Auditiva leve'],
      requisitos: [
        'Conocimientos en Python, SQL y herramientas de visualización',
        'Experiencia en análisis de datos',
        'Capacidad para trabajar con equipos multidisciplinarios'
      ],
      beneficios: [
        'Trabajo remoto 3 días a la semana',
        'Software lector de pantalla disponible',
        'Capacitación continua'
      ]
    },
    {
      id: 2,
      titulo: 'Desarrollador Web Frontend',
      empresa: 'Creative Devs',
      ubicacion: 'Medellín, Colombia',
      tipoContrato: 'Remoto',
      descripcion: 'Se necesita desarrollador con conocimientos en React y TailwindCSS.',
      fechaPublicacion: '2023-11-08',
      horario: 'Horario flexible, 40 horas semanales',
      salario: '$3.000.000 - $4.000.000 COP',
      discapacidades: ['Motriz', 'Auditiva'],
      requisitos: [
        'Experiencia en desarrollo con React',
        'Conocimientos de TailwindCSS y diseño responsive',
        'Capacidad para trabajar de forma autónoma'
      ],
      beneficios: [
        '100% remoto',
        'Horario flexible',
        'Equipos ergonómicos proporcionados por la empresa'
      ]
    },
    {
      id: 3,
      titulo: 'Asistente Administrativo',
      empresa: 'Corporación Inclusiva',
      ubicacion: 'Cali, Colombia',
      tipoContrato: 'Tiempo parcial',
      descripcion: 'Oportunidad para personas con discapacidad motriz. Ambiente adaptado.',
      fechaPublicacion: '2023-11-05',
      horario: 'Lunes a viernes de 9:00 AM a 1:00 PM',
      salario: '$1.200.000 - $1.500.000 COP',
      discapacidades: ['Motriz', 'Cognitiva leve'],
      requisitos: [
        'Conocimientos básicos de ofimática',
        'Buenas habilidades de comunicación',
        'No se requiere experiencia previa'
      ],
      beneficios: [
        'Transporte incluido',
        'Ambiente de trabajo adaptado',
        'Posibilidad de crecimiento profesional'
      ]
    }
  ];

  const handleOpenModal = (oferta) => {
    setSelectedOferta(oferta);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  // Modal Component
  const DetallesOfertaModal = () => {
    if (!isModalOpen || !selectedOferta) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto">
        <div className={`${darkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-800'} rounded-lg shadow-xl max-w-3xl w-full relative max-h-screen overflow-y-auto`}>
          <button
            onClick={handleCloseModal}
            className={`absolute top-4 right-4 ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
          <div className="p-6">
            <h2 className={`text-2xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-2`}>
              {selectedOferta.titulo}
            </h2>
            <p className={`${darkMode ? 'text-purple-300' : 'text-moradomio'} font-medium text-lg mb-4`}>
              {selectedOferta.empresa}
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h3 className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'} mb-2`}>Detalles del puesto</h3>
                <ul className="space-y-2">
                  <li className="flex items-start">
                    <span className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} mr-2`}>📍</span>
                    <span>{selectedOferta.ubicacion}</span>
                  </li>
                  <li className="flex items-start">
                    <span className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} mr-2`}>⏰</span>
                    <span>{selectedOferta.horario}</span>
                  </li>
                  <li className="flex items-start">
                    <span className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} mr-2`}>💼</span>
                    <span>{selectedOferta.tipoContrato}</span>
                  </li>
                  <li className="flex items-start">
                    <span className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} mr-2`}>💰</span>
                    <span>{selectedOferta.salario}</span>
                  </li>
                  <li className="flex items-start">
                    <span className={`${darkMode ? 'text-gray-400' : 'text-gray-600'} mr-2`}>📅</span>
                    <span>Publicado: {new Date(selectedOferta.fechaPublicacion).toLocaleDateString()}</span>
                  </li>
                </ul>
              </div>
              
              <div>
                <h3 className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'} mb-2`}>Discapacidades admitidas</h3>
                <div className="flex flex-wrap gap-2 mb-4">
                  {selectedOferta.discapacidades.map((discapacidad, index) => (
                    <span 
                      key={index} 
                      className={`inline-block ${
                        darkMode 
                          ? 'bg-purple-900 text-purple-200' 
                          : 'bg-purple-100 text-purple-800'
                      } text-xs px-2 py-1 rounded-full`}
                    >
                      {discapacidad}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="mb-6">
              <h3 className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'} mb-2`}>Descripción</h3>
              <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>{selectedOferta.descripcion}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h3 className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'} mb-2`}>Requisitos</h3>
                <ul className={`list-disc pl-5 ${darkMode ? 'text-gray-300' : 'text-gray-600'} space-y-1`}>
                  {selectedOferta.requisitos.map((requisito, index) => (
                    <li key={index}>{requisito}</li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h3 className={`font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'} mb-2`}>Beneficios</h3>
                <ul className={`list-disc pl-5 ${darkMode ? 'text-gray-300' : 'text-gray-600'} space-y-1`}>
                  {selectedOferta.beneficios.map((beneficio, index) => (
                    <li key={index}>{beneficio}</li>
                  ))}
                </ul>
              </div>
            </div>
            
            <div className="flex justify-end">
              <button 
                className="bg-gradient-to-r from-azulmio to-moradomio text-white px-6 py-3 rounded-md hover:brightness-110 transition"
              >
                Aplicar a esta oferta
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} transition-colors duration-300`}>
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <main className="container mx-auto px-4 pt-24 pb-12">
        <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-azulmio'} mb-6`}>Ofertas de Trabajo</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ofertas.map((oferta) => (
            <div 
              key={oferta.id} 
              className={`${
                darkMode 
                  ? 'bg-gray-800 hover:bg-gray-700 text-gray-100' 
                  : 'bg-white hover:shadow-lg text-gray-800'
              } rounded-lg shadow-md transition-all p-6`}
            >
              <h2 className={`text-xl font-semibold ${darkMode ? 'text-blue-300' : 'text-azulmio'} mb-2`}>{oferta.titulo}</h2>
              <p className={`${darkMode ? 'text-purple-300' : 'text-moradomio'} font-medium`}>{oferta.empresa}</p>
              <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mb-3`}>{oferta.ubicacion}</p>
              <span className={`inline-block ${
                darkMode 
                  ? 'bg-blue-900 text-blue-200' 
                  : 'bg-blue-100 text-blue-800'
              } text-xs px-2 py-1 rounded-full mb-3`}>
                {oferta.tipoContrato}
              </span>
              <p className={`${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-4`}>{oferta.descripcion}</p>
              <div className="flex justify-between items-center">
                <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  Publicado: {new Date(oferta.fechaPublicacion).toLocaleDateString()}
                </span>
                <button 
                  onClick={() => handleOpenModal(oferta)}
                  className="bg-gradient-to-r from-azulmio to-moradomio text-white px-4 py-2 rounded-md hover:brightness-110 transition"
                >
                  Ver detalles
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Modal de detalles */}
      <DetallesOfertaModal />
    </div>
  );
};

export default Inicio; 