import React, { useEffect, useState } from "react";
import {
  Container,
  ThemeProvider,
  CssBaseline,
  Typography,
  Button,
  Grid,
  Box,
} from "@mui/material";
import Upload from "./component/Upload";
import Navbar from "./component/Navbar";
import VideoPlayer from "./component/VideoPlayer";
import Transcript from "./component/Transcript";
import Chat from "./component/Chat";
import Summary from "./component/Summary";
import darkTheme from "./theme/darkTheme";

const App = () => {
  const [videoId, setVideoId] = useState(null);

  const handleUpload = (data) => {
    setVideoId(data.videoId);
    localStorage.setItem("id", data.videoId);
  };

  const handleReset = () => {
    setVideoId(null);
    localStorage.removeItem("id");
  };

  useEffect(() => {
    const video_id = localStorage.getItem("id");
    if (video_id != null) {
      setVideoId(video_id);
    }
  }, []);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Navbar />
      {!videoId ? (
        <Container
          maxWidth="sm"
          style={{
            height: "100vh",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            // backgroundColor: 'rgba(0, 0, 0, 0.7)',
            borderRadius: '8px',
          }}
        >
          <Upload onUpload={handleUpload} />
        </Container>
      ) : (
        <Container
          maxWidth="lg"
          style={{
            marginTop: "30px",
            // backgroundColor: 'rgba(0, 0, 0, 0.7)',
            borderRadius: '8px',
            padding: '20px',
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6" sx={{ color: 'white' }}>
              Video Interaction
            </Typography>
            <Button variant="contained" color="secondary" onClick={handleReset}>
              Reset
            </Button>
          </Box>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <VideoPlayer
                url={`${process.env.REACT_APP_URL}/getVideo/${videoId}`}
              />
              <Transcript id={videoId} />
            </Grid>
            <Grid item xs={12} md={4}>
              <Chat id={videoId} />
              <Summary id={videoId} />
            </Grid>
          </Grid>
        </Container>
      )}
    </ThemeProvider>
  );
};

export default App;
