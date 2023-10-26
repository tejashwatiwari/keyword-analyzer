import React, {useState} from 'react';
import {Select, TextField, Stack, Button, FormControl, MenuItem, InputLabel, Box} from '@mui/material';
import './main.css'


export default function Main() {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedAlgorithm, setSelectedAlgorithm] = useState("rabin"); // Default algorithm is Rabin-Karp
    const [searchResults, setSearchResults] = useState([]);
  
    const handleAlgorithmChange = (event) => {
      setSelectedAlgorithm(event.target.value);
    };
    const handleSearch = () => {
        // Create a data object to send in the POST request
        const data = {
          algorithm: selectedAlgorithm,
          searchTerm: searchTerm,
        };
    
        fetch('/search', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
            .then((response) => response.json())
            .then((data) => {
              setSearchResults(data.keywords);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        };


    return (
        <>
        <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
            <InputLabel id="choose-algorithm">Choose Algorithm</InputLabel>
            <Select
            labelId="choose-algorithm"
            id="simple-select"
            value={selectedAlgorithm}
            label="Choose Algorithm"
            onChange={handleAlgorithmChange}
            >
            <MenuItem value={"rabin"}>Rabin-Karp</MenuItem>
            <MenuItem value={"suffixt"}>Suffix Tree</MenuItem>
            <MenuItem value={"suffixa"}>Suffix Array</MenuItem>
            <MenuItem value={"naive"}>Naive-String Matching</MenuItem>
            <MenuItem value={"kmp"}>KMP Algorithm</MenuItem>
            </Select>
        </FormControl>
        </Box>
     
        <Box
        id="url-box"
        component="form"
        sx={{
          '& > :not(style)': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        <TextField
          id="standard-basic"
          label="Enter URL"
          variant="standard"
          type="url"
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
        />
      </Box>
   
        <Stack spacing={2} direction="row" id ="search-button">
            <Button variant="contained" onClick={handleSearch}>Search</Button>
        </Stack>
        {searchResults.length > 0 && (
        <div>
          <h3>Search Results:</h3>
          <ul>
            {searchResults.map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        </div>
      )}
        </>
)}
