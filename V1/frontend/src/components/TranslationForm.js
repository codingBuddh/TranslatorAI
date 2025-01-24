import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Box, 
  CircularProgress, 
  Alert, 
  Snackbar,
  Paper,
  Typography,
  IconButton
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { translateText } from '../services/api';

function TranslationForm() {
  const [text, setText] = useState('');
  const [targetLanguages, setTargetLanguages] = useState(['']);
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

    // Filter out empty language inputs
    const validLanguages = targetLanguages.filter(lang => lang.trim());
    if (validLanguages.length === 0) {
      setError('Please enter at least one target language');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await translateText(text, validLanguages);
      console.log('Translation response:', response);
      if (response && response.translations) {
        setTranslations(response.translations);
        setSuccess(true);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Translation error:', err);
      setError(err.message || 'Translation failed. Please try again.');
      setTranslations({});
    } finally {
      setLoading(false);
    }
  };

  const addLanguageField = () => {
    setTargetLanguages([...targetLanguages, '']);
  };

  const removeLanguageField = (index) => {
    const newLanguages = targetLanguages.filter((_, i) => i !== index);
    setTargetLanguages(newLanguages.length ? newLanguages : ['']);
  };

  const handleLanguageChange = (index, value) => {
    const newLanguages = [...targetLanguages];
    newLanguages[index] = value;
    setTargetLanguages(newLanguages);
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
        
        {/* Language input fields */}
        {targetLanguages.map((lang, index) => (
          <Box key={index} sx={{ display: 'flex', gap: 1, alignItems: 'center', my: 1 }}>
            <TextField
              fullWidth
              value={lang}
              onChange={(e) => handleLanguageChange(index, e.target.value)}
              label={`Target Language ${index + 1}`}
              placeholder="Enter language (e.g., Spanish, French, German)"
              disabled={loading}
            />
            <IconButton 
              onClick={() => removeLanguageField(index)}
              disabled={targetLanguages.length === 1}
              color="error"
            >
              <DeleteIcon />
            </IconButton>
            {index === targetLanguages.length - 1 && (
              <IconButton onClick={addLanguageField} color="primary">
                <AddIcon />
              </IconButton>
            )}
          </Box>
        ))}

        <Button 
          variant="contained" 
          type="submit"
          disabled={loading || !text.trim()}
          sx={{ mt: 2 }}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Translate'}
        </Button>

        {/* Translation Results */}
        {Object.entries(translations).map(([lang, translation]) => (
          <Paper key={lang} elevation={1} sx={{ mt: 2, p: 2 }}>
            <Typography variant="subtitle2" color="textSecondary" gutterBottom>
              Translation to {lang}
              {translation.source_language && ` (from ${translation.source_language})`}
            </Typography>
            <Typography>
              {translation.text || translation.error || 'Translation not available'}
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