import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Instancia axios con configuración básica
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para añadir el token JWT
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Servicios de autenticación
export const authService = {
  login: async (credentials) => {
    const response = await api.post('/login', credentials);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },
  
  register: async (userData) => {
    return await api.post('/register', userData);
  },
  
  logout: () => {
    localStorage.removeItem('token');
  },
  
  getCurrentUser: async () => {
    return await api.get('/me');
  }
};

// Servicios para otros recursos
export const jobsService = {
  getAllJobs: async () => {
    return await api.get('/jobs');
  },
  
  getJob: async (id) => {
    return await api.get(`/jobs/${id}`);
  }
};

export default api;