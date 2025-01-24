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
    console.log('Sending request:', { text, target_languages: targetLanguages }); // Debug log
    const response = await api.post('/api/v1/translate', {
      text,
      target_languages: targetLanguages,
    });
    console.log('API response:', response.data); // Debug log
    return response.data;
  } catch (error) {
    console.error('API error:', error.response || error); // Debug log
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Translation failed. Please try again.');
  }
};

export default api; 