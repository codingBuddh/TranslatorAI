import React, { useState } from 'react';
import { TextField, Button, Box, MenuItem } from '@mui/material';

const LANGUAGES = [
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  // Add more languages as needed
];

function TranslationForm() {
  const [text, setText] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('es');
  const [translation, setTranslation] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implement API call
    setTranslation('Translation will appear here...');
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 600, margin: '0 auto', p: 2 }}>
      <TextField
        fullWidth
        multiline
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        label="Text to translate"
        margin="normal"
      />
      
      <TextField
        select
        fullWidth
        value={targetLanguage}
        onChange={(e) => setTargetLanguage(e.target.value)}
        label="Target Language"
        margin="normal"
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
        sx={{ mt: 2 }}
      >
        Translate
      </Button>

      {translation && (
        <TextField
          fullWidth
          multiline
          rows={4}
          value={translation}
          label="Translation"
          margin="normal"
          InputProps={{
            readOnly: true,
          }}
        />
      )}
    </Box>
  );
}

export default TranslationForm; 