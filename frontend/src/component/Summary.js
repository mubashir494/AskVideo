import React, { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';

const Summary = ({ id }) => {
  const BASE_URL = process.env.REACT_APP_URL;
  const [text,setText] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const formData = new FormData();
        formData.append("id", id);
        formData.append("prompt","Give a Brief Summary");
        const response = await fetch(`${BASE_URL}/chat`, {
          method: "POST",
          body: formData,
          // Adding headers to the request
        });
        console.log(response);
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.message);
        }
        setText(result.response);
      } catch (e) {
        setText(e.messages);
        console.log(e.message);
      }
    };
    fetchData();  
  },[])

  return (
    <Box sx={{ padding: 2, backgroundColor: '#1d1d1d', color: 'white', mt: 1.5 ,overflow:'true'}}>
      <Typography variant="h6">Summary</Typography>
      <Typography variant="body1">{text}</Typography>
    </Box>
  );
};

export default Summary;