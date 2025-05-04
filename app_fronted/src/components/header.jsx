import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bars3Icon, XMarkIcon, UserCircleIcon, MoonIcon, SunIcon } from '@heroicons/react/24/outline';

const Header = ({ darkMode, toggleDarkMode }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
    if (isProfileMenuOpen) setIsProfileMenuOpen(false);
  };

  const toggleProfileMenu = () => {
    setIsProfileMenuOpen(!isProfileMenuOpen);
    if (isMenuOpen) setIsMenuOpen(false);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  // Cerrar menús al cambiar de ruta
  useEffect(() => {
    setIsMenuOpen(false);
    setIsProfileMenuOpen(false);
  }, [location]);

  return (
    <header className={`${darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-800'} shadow-md fixed w-full top-0 z-40 transition-colors duration-300`}>
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        {/* Logo */}
        <Link to="/inicio" className="flex items-center">
          <img src={darkMode ? "/inklurosa.png" : "/inklufnd.png"} alt="InKlúIA Logo" className="h-10 mr-2" />
          <span className="text-xl font-bold">
            <span className="bg-gradient-to-r from-azulmio to-moradomio text-transparent bg-clip-text">InKlú-IA</span>
          </span>
        </Link>

        {/* Navegación escritorio */}
        <nav className="hidden md:flex space-x-6">
          <Link 
            to="/inicio" 
            className={`font-medium ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-moradomio'} transition-colors ${isActive('/inicio') ? 'border-b-2 border-moradomio text-moradomio' : ''}`}
          >
            Inicio
          </Link>
          <Link 
            to="/chat" 
            className={`font-medium ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-moradomio'} transition-colors ${isActive('/chat') ? 'border-b-2 border-moradomio text-moradomio' : ''}`}
          >
            Chat con Inklú
          </Link>
          <Link 
            to="/preparacion" 
            className={`font-medium ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-moradomio'} transition-colors ${isActive('/preparacion') ? 'border-b-2 border-moradomio text-moradomio' : ''}`}
          >
            Preparación
          </Link>
        </nav>

        {/* Botones de acción (incluido el modo oscuro) */}
        <div className="hidden md:flex items-center space-x-4">
          {/* Botón de modo oscuro */}
          <button 
            onClick={toggleDarkMode} 
            className={`p-2 rounded-full ${darkMode ? 'bg-gray-700 text-yellow-300 hover:bg-gray-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-colors`}
            aria-label={darkMode ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
          >
            {darkMode ? (
              <SunIcon className="h-5 w-5" />
            ) : (
              <MoonIcon className="h-5 w-5" />
            )}
          </button>

          {/* Perfil de usuario */}
          <div className="relative group">
            <button className={`flex items-center space-x-1 p-2 rounded-full ${darkMode ? 'bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white' : 'bg-gray-100 hover:bg-gray-200 text-gray-600 hover:text-gray-800'}`}>
              <UserCircleIcon className="h-7 w-7" />
            </button>
            <div className={`absolute right-0 mt-2 w-60 ${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-md shadow-lg overflow-hidden z-20 hidden group-hover:block transition-all duration-300 origin-top-right`}>
              <div className="py-2">
                <div className={`px-4 py-3 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
                  <p className={`text-sm font-medium ${darkMode ? 'text-white' : 'text-gray-800'}`}>María González</p>
                  <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>maria.gonzalez@email.com</p>
                </div>
                <Link to="/configuracion" className={`flex items-center px-4 py-3 text-sm ${darkMode ? 'text-gray-300 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-100'}`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Configuración de perfil
                </Link>
                <hr className={`my-1 ${darkMode ? 'border-gray-700' : 'border-gray-200'}`} />
                <button className={`flex items-center w-full text-left px-4 py-3 text-sm text-red-600 hover:${darkMode ? 'bg-gray-700' : 'bg-red-50'}`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Cerrar Sesión
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Botón móvil y modo oscuro móvil */}
        <div className="md:hidden flex items-center space-x-2">
          <button 
            onClick={toggleDarkMode} 
            className={`p-2 rounded-full ${darkMode ? 'bg-gray-700 text-yellow-300' : 'bg-gray-100 text-gray-700'} transition-colors`}
            aria-label={darkMode ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
          >
            {darkMode ? (
              <SunIcon className="h-5 w-5" />
            ) : (
              <MoonIcon className="h-5 w-5" />
            )}
          </button>
          
          {/* Perfil en móvil */}
          <div className="relative">
            <button 
              onClick={toggleProfileMenu}
              className={`p-2 rounded-full ${darkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600'}`}
            >
              <UserCircleIcon className="h-5 w-5" />
            </button>
          </div>
          
          <button 
            onClick={toggleMenu}
            aria-label="Menú principal"
            className={`${darkMode ? 'text-white' : 'text-gray-600'} focus:outline-none`}
          >
            {isMenuOpen ? (
              <XMarkIcon className="h-7 w-7" />
            ) : (
              <Bars3Icon className="h-7 w-7" />
            )}
          </button>
        </div>
      </div>

      {/* Menú móvil */}
      {isMenuOpen && (
        <div className={`md:hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link 
              to="/inicio"
              className={`block px-3 py-2 rounded-md text-base font-medium ${
                isActive('/inicio') 
                  ? 'bg-moradomio text-white' 
                  : darkMode ? 'text-gray-300 hover:bg-gray-700 hover:text-white' : 'text-gray-700 hover:bg-gray-100'
              }`}
              onClick={toggleMenu}
            >
              Inicio
            </Link>
            <Link 
              to="/chat"
              className={`block px-3 py-2 rounded-md text-base font-medium ${
                isActive('/chat') 
                  ? 'bg-moradomio text-white' 
                  : darkMode ? 'text-gray-300 hover:bg-gray-700 hover:text-white' : 'text-gray-700 hover:bg-gray-100'
              }`}
              onClick={toggleMenu}
            >
              Chat con Inklú
            </Link>
            <Link 
              to="/preparacion"
              className={`block px-3 py-2 rounded-md text-base font-medium ${
                isActive('/preparacion') 
                  ? 'bg-moradomio text-white' 
                  : darkMode ? 'text-gray-300 hover:bg-gray-700 hover:text-white' : 'text-gray-700 hover:bg-gray-100'
              }`}
              onClick={toggleMenu}
            >
              Preparación
            </Link>
            <hr className={`my-2 ${darkMode ? 'border-gray-700' : 'border-gray-200'}`} />
            <button 
              className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-600 hover:bg-red-50"
              onClick={toggleMenu}
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      )}

      {/* Menú de perfil móvil */}
      {isProfileMenuOpen && (
        <div className={`md:hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
          <div className="px-2 pt-2 pb-3 space-y-1">
            <div className={`px-3 py-2 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
              <p className={`text-base font-medium ${darkMode ? 'text-white' : 'text-gray-800'}`}>María González</p>
              <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>maria.gonzalez@email.com</p>
            </div>
            <Link 
              to="/configuracion"
              className={`flex items-center px-3 py-2 rounded-md text-base font-medium ${darkMode ? 'text-gray-300 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-100'}`}
              onClick={toggleProfileMenu}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Configuración de perfil
            </Link>
            <hr className={`my-2 ${darkMode ? 'border-gray-700' : 'border-gray-200'}`} />
            <button 
              className={`flex items-center w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-600 hover:${darkMode ? 'bg-gray-700' : 'bg-red-50'}`}
              onClick={toggleProfileMenu}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header; 