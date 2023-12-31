import React from 'react';
import {Container,Typography,Box} from '@mui/material';
import Main from './components/dashboard/Main'

export default function App() {
  return (
    <Container maxWidth="sm">
      <Box sx={{ my: 8 }}>
        <Typography variant="h4" fontFamily="Sans-serif" component="h1" gutterBottom >
          KeywordPulse - Everything you need to rank higher & get more traffic
        </Typography>
        <Main />

        </Box>
    </Container>
  );
}
