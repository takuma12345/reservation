import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';  // Remplacez par l'URL de votre API Django

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const getRooms = async () => {
  const response = await api.get('/rooms/');
  return response.data;
};

export const createReservation = async (reservationData) => {
  const response = await api.post('/reservations/', reservationData);
  return response.data;
};

export const login = async (credentials) => {
  const response = await api.post('/auth/login/', credentials);
  return response.data;
};

// Ajoutez d'autres fonctions pour interagir avec votre API