import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Box, 
  MenuItem, 
  CircularProgress, 
  Alert, 
  Snackbar,
  Paper,
  Typography
} from '@mui/material';
import { translateText } from '../services/api';

const LANGUAGES = [
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'ru', name: 'Russian' },
  { code: 'zh', name: 'Chinese' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ko', name: 'Korean' },
  { code: 'ar', name: 'Arabic' }
];

function TranslationForm() {
  const [text, setText] = useState('');
  const [targetLanguages, setTargetLanguages] = useState(['es']);
  const [translations, setTranslations] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter text to translate');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await translateText(text, targetLanguages);
      setTranslations(response.translations);
      setSuccess(true);
    } catch (err) {
      setError(err.message);
      setTranslations({});
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Text Translation
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          multiline
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          label="Text to translate"
          margin="normal"
          disabled={loading}
          error={!text.trim() && error}
          helperText={!text.trim() && error ? 'This field is required' : ''}
        />
        
        <TextField
          select
          fullWidth
          multiple
          value={targetLanguages}
          onChange={(e) => setTargetLanguages(e.target.value)}
          label="Target Languages"
          margin="normal"
          disabled={loading}
        >
          {LANGUAGES.map((lang) => (
            <MenuItem key={lang.code} value={lang.code}>
              {lang.name}
            </MenuItem>
          ))}
        </TextField>

        <Button 
          variant="contained" 
          type="submit"
          disabled={loading || !text.trim()}
          sx={{ mt: 2 }}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Translate'}
        </Button>

        {Object.entries(translations).map(([lang, translation]) => (
          <Paper key={lang} elevation={1} sx={{ mt: 2, p: 2 }}>
            <Typography variant="subtitle2" color="textSecondary" gutterBottom>
              {LANGUAGES.find(l => l.code === lang)?.name}
              {translation.source_language && ` (from ${translation.source_language})`}
            </Typography>
            <Typography>
              {translation.text || translation.error}
            </Typography>
          </Paper>
        ))}

        <Snackbar 
          open={error !== null} 
          autoHideDuration={6000} 
          onClose={() => setError(null)}
        >
          <Alert severity="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        </Snackbar>

        <Snackbar 
          open={success} 
          autoHideDuration={6000} 
          onClose={() => setSuccess(false)}
        >
          <Alert severity="success" onClose={() => setSuccess(false)}>
            Translation completed successfully!
          </Alert>
        </Snackbar>
      </Box>
    </Paper>
  );
}

export default TranslationForm; 