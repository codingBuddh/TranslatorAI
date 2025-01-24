import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const translateText = async (text, targetLanguages) => {
  try {
    const response = await api.post('/api/v1/translate', {
      text,
      target_languages: targetLanguages,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Translation failed');
  }
};

export default api; 