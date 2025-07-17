import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/users/me'),
  updateProfile: (userData) => api.put('/users/me', userData),
  updatePreferences: (preferences) => api.put('/users/me/preferences', preferences),
};

// Topics API
export const topicsAPI = {
  getTopics: () => api.get('/topics'),
  getTopic: (id) => api.get(`/topics/${id}`),
  createTopic: (topicData) => api.post('/topics', topicData),
  updateTopic: (id, topicData) => api.put(`/topics/${id}`, topicData),
  deleteTopic: (id) => api.delete(`/topics/${id}`),
};

// Learning Paths API
export const learningPathsAPI = {
  getLearningPaths: (topicId) => api.get(`/learning-paths/topic/${topicId}`),
  getLearningPath: (id) => api.get(`/learning-paths/${id}`),
  createLearningPath: (pathData) => api.post('/learning-paths', pathData),
  updateLearningPath: (id, pathData) => api.put(`/learning-paths/${id}`, pathData),
  deleteLearningPath: (id) => api.delete(`/learning-paths/${id}`),
};

// Lessons API
export const lessonsAPI = {
  getLessons: (learningPathId) => api.get(`/lessons/learning-path/${learningPathId}`),
  getLesson: (id) => api.get(`/lessons/${id}`),
  createLesson: (lessonData) => api.post('/lessons', lessonData),
  updateLesson: (id, lessonData) => api.put(`/lessons/${id}`, lessonData),
  deleteLesson: (id) => api.delete(`/lessons/${id}`),
};

// Videos API
export const videosAPI = {
  getVideos: (lessonId) => api.get(`/videos/lesson/${lessonId}`),
  getVideo: (id) => api.get(`/videos/${id}`),
  generateVideo: (lessonId, options = {}) => api.post('/videos/generate', { lesson_id: lessonId, ...options }),
  deleteVideo: (id) => api.delete(`/videos/${id}`),
};

export default api;

