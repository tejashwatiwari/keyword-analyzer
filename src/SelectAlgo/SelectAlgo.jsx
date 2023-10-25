import React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function SelectAlgo() {
    const [age, setAge] = React.useState('');
    const handleChange = (event) => {
        setAge(event.target.value);
      };

  return (
    <div>
    <Box sx={{ minWidth: 120 }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Choose Algorithm</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={age}
          label="Choose Algorithm"
          onChange={handleChange}
        >
          <MenuItem value={10}>Rabin-Karp</MenuItem>
          <MenuItem value={20}>Suffix Tree</MenuItem>
          <MenuItem value={30}>Suffix Array</MenuItem>
          <MenuItem value={40}>Naive-String Matching</MenuItem>
          <MenuItem value={50}>KMP Algorithm</MenuItem>
        </Select>
      </FormControl>
    </Box>
    </div>
  );
}

export default SelectAlgo
