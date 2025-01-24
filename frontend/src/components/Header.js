import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';
import TranslateIcon from '@mui/icons-material/Translate';

function Header() {
  return (
    <AppBar position="static">
      <Toolbar>
        <TranslateIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div">
          TranslatorAI
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default Header; 