import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";

const Transcript = ({ id }) => {
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const BASE_URL = process.env.REACT_APP_URL;

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (text == "") {
          const formData = new FormData();
          formData.append("id", id);
          const response = await fetch(`${BASE_URL}/transcription`, {
            method: "POST",
            body: formData,
            // Adding headers to the request
          });
          console.log(response);
          const result = await response.json();
          if (!response.ok) {
            throw new Error(result.message);
          }
          setText(result.transcript);
        }
      } catch (e) {
        setError(e.message);
        console.log(e.message);
      }
    };
    fetchData();
  }, []);
  return (
    <Box
      sx={{
        padding: 2,
        backgroundColor: "#1d1d1d",
        color: "white",
        marginTop: "10px",
      }}
    >
      <Typography variant="h6">Transcript</Typography>
      {error != "" ? (
        <Typography variant="body1" color="red">
          {error}
        </Typography>
      ) : (
        <Typography variant="body1">{text}</Typography>
      )}
    </Box>
  );
};

export default Transcript;
