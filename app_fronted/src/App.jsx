import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { authService } from './services/api';
import Login from './components/Login';
import './App.css';

// Componente para la página Dashboard
const Dashboard = () => (
  <div className="container mx-auto p-4">
    <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
    <p>¡Bienvenido a INKLU-AI!</p>
  </div>
);

// Componente para proteger rutas
const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  
  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (localStorage.getItem('token')) {
          await authService.getCurrentUser();
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Error verificando autenticación:', error);
        setIsAuthenticated(false);
      }
    };
    
    checkAuth();
  }, []);
  
  if (isAuthenticated === null) {
    return <div className="flex h-screen items-center justify-center">Cargando...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;
