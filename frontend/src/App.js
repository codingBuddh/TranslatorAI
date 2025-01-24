import React from 'react';
import './App.css';
import TranslationForm from './components/TranslationForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>TranslatorAI</h1>
      </header>
      <main>
        <TranslationForm />
      </main>
    </div>
  );
}

export default App; 