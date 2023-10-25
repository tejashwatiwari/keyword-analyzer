import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';



const TextFieldExample = () => {
  return (
    <div>
       <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <TextField id="standard-basic" label="Enter URL" variant="standard" type="url" />
    </Box>
    </div>
  )
}

export default TextFieldExample
