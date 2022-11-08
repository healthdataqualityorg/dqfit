import React, { useState, useEffect } from 'react';
import axios from 'axios'
import JSONPretty from 'react-json-pretty';

import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function Home() {

    const [file, setFile] = useState();
    const [results, setResults] = useState();

    const handleSubmit = async (e) => {
        console.log(file)
        const formData = new FormData();
        formData.append("fname", "omglol");
        formData.append("file", file);
        const headers = { "Content-Type": "multipart/form-data" }
        const apiBase = 'http://localhost:5000' // set this in App
        const endpoint = `${apiBase}/cohort-test`
        const response = axios.post(endpoint, formData, headers);
        console.log(response.json)
        setResults(response.json)

    }

    const fileSelectHandler = (e) => {
        const newFile = e.target.files[0]
        // console.log(newFile)
        setFile(newFile)
    }

    return (
        <Container>
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    app.dqfit.org
                </Typography>
            </Box>
            <Button variant="outlined" component="label" style={{ marginTop: 25, marginBottom: 25 }}>
                Select File
                <input
                    onChange={fileSelectHandler}
                    hidden
                    accept="*"
                    multiple
                    type="file"
                />
            </Button>
            {
                file && <Button
                    variant="contained"
                    component="label"
                    onClick={handleSubmit}
                >
                    Submit
                </Button>
            }
            {
                results && <JSONPretty data={results}/>
            }
        </Container>
    )

}