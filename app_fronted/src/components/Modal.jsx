import React from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';

const Modal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full relative">
        <button
          onClick={onClose}
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
            <Link
              to="/configuracion"
              className="bg-gradient-to-r from-azulmio to-moradomio text-white font-semibold py-2 px-4 rounded-md text-center hover:brightness-110 transition shadow-lg"
            >
              Configurar perfil
            </Link>
            <button
              onClick={onClose}
              className="border border-azulmio text-azulmio font-semibold py-2 px-4 rounded-md hover:bg-azulmio hover:text-white transition"
            >
              Explorar aplicación
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal; 