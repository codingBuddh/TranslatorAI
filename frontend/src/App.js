import React from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { Container } from '@mui/material';
import Header from './components/Header';
import TranslationForm from './components/TranslationForm';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    }
  }
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <TranslationForm />
      </Container>
    </ThemeProvider>
  );
}

export default App; 