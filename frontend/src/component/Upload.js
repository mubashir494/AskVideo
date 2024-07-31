import React, { useState } from "react";
import { Box, Button, CircularProgress, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { styled } from "@mui/system";

const UploadBox = styled(Box)(({ theme }) => ({
  border: "2px dashed #aaa",
  borderRadius: "8px",
  padding: "20px",
  textAlign: "center",
  cursor: "pointer",
  transition: "border-color 0.3s",
  "&:hover": {
    borderColor: theme.palette.primary.main,
  },
}));

const Upload = ({ onUpload }) => {
  const BASE_URL = process.env.REACT_APP_URL;
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.message);
      }

      localStorage.setItem("id",result.filename.split(".")[0]);
      window.location.reload();
    } catch (e) {
      setError(e.message)
      console.log(e.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setFile(droppedFile);
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
    >
      {error != "" ? (
        <Typography variant="body1" gutterBottom color={"red"}>
          {error}
        </Typography>
      ) : (
        <></>
      )}

      <UploadBox
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        height="200px"
        width="100%"
        maxWidth="500px"
      >
        {file ? (
          <Typography variant="body1">{file.name}</Typography>
        ) : (
          <Typography variant="body1">
            Drag & drop a file here, or click to select one
          </Typography>
        )}
      </UploadBox>
      <input
        type="file"
        style={{ display: "none" }}
        id="upload-input"
        onChange={handleChange}
      />
      <label htmlFor="upload-input">
        <Button
          variant="contained"
          component="span"
          startIcon={<CloudUploadIcon />}
          sx={{ mt: 2 }}
        >
          Select File
        </Button>
      </label>
      {file && (
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          sx={{ mt: 2 }}
          disabled={uploading}
        >
          {uploading ? <CircularProgress size={24} /> : "Upload"}
        </Button>
      )}
    </Box>
  );
};

export default Upload;
