import * as React from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
// import TextFieldExample from './TextFields/TextFieldExample';
// import SubmitButton from './Buttons/SubmitButton';
// import SelectAlgo from './SelectAlgo/SelectAlgo';
import Main from './Main'

export default function App() {
  return (
    <Container maxWidth="sm">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          KeywordPulse - Everything you need to rank higher & get more traffic
        </Typography>
        <Main />
        {/* <SelectAlgo />
        <TextFieldExample />
        <SubmitButton /> */}
        </Box>
    </Container>
  );
}
