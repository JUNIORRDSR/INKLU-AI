import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/register';
import Chat from './components/Chat';
import './App.css';

// Componente para la página Dashboard
const Dashboard = () => (
  <div className="container mx-auto p-4">
    <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
    <p>¡Bienvenido a INKLU-AI!</p>
  </div>
);

// Versión simplificada de ProtectedRoute para pruebas
const ProtectedRoute = ({ children }) => {
  return children; // Para pruebas: siempre muestra las rutas sin autenticación
};

const XMarkIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" 
       viewBox="0 0 24 24" 
       fill="none" 
       stroke="currentColor" 
       strokeWidth={2} 
       {...props}>
    <path d="M6 18L18 6M6 6l12 12" />
  </svg>
);

function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Rutas de la aplicación */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chat" element={<Chat />} />
        
        {/* Ruta por defecto */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
