import React from 'react';
import {Select, TextField, Stack, Button, FormControl, MenuItem, InputLabel, Box} from '@mui/material';
import './main.css'


export default function Main() {
       

    return (
        <>
        <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">Choose Algorithm</InputLabel>
            <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            // value={age}
            label="Choose Algorithm"
            // onChange={handleChange}
            >
            <MenuItem value={10}>Rabin-Karp</MenuItem>
            <MenuItem value={20}>Suffix Tree</MenuItem>
            <MenuItem value={30}>Suffix Array</MenuItem>
            <MenuItem value={40}>Naive-String Matching</MenuItem>
            <MenuItem value={50}>KMP Algorithm</MenuItem>
            </Select>
        </FormControl>
        </Box>
     
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
   
   
        <Stack spacing={2} direction="row">
            <Button variant="contained">Search</Button>
        </Stack>
        </>
)}