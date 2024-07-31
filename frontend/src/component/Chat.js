import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Typography, Paper } from "@mui/material";

const Chat = ({id}) => {
  const BASE_URL = process.env.REACT_APP_URL;
  const [messages, setMessages] = useState([
    {
      text: "Connect with the world, one message at a time!",
      type: "receiver",
    },
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const fetchData = async (input) => {
    try {
      const formData = new FormData();
      formData.append("id", id);
      formData.append("prompt",input);
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
      console.log(messages);
      setMessages([...messages, { text: input, type: "sender" },{ text: result.response, type: "receiver" }]);
    } catch (e) {
      setMessages([...messages,  { text: input, type: "sender" },{ text: e.messege, type: "receiver" }]);
      console.log(e.message);
    }
  };
  const handleSend = () => {
    if (input.trim()) {
      console.log(messages)
      fetchData(input);

      setInput("");
    }
  };
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleSend();
    }
  };
  const handleClear = () => {
    setMessages([]);
  };
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  return (
    <Box
      sx={{
        height: "320px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        backgroundColor: "#1d1d1d",
        color: "white",
        padding: 2,
      }}
    >
      <Box sx={{ flexGrow: 1, overflowY: "auto", padding: 1 }}>
        <Typography variant="h6" sx={{ marginBottom: 2 }}>
          Chat
        </Typography>
        <Box>
          {messages.map((message, index) => (
            <Paper
              key={index}
              sx={{
                padding: 1,
                marginBottom: 1,
                backgroundColor: message.type === "sender" ? "#1976d2" : "#333",
                color: "white",
                alignSelf:
                  message.type === "sender" ? "flex-end" : "flex-start",
                maxWidth: "80%",
              }}
            >
              <Typography overflow="hidden" variant="body1">
                {message.text}
              </Typography>
            </Paper>
          ))}
          <div ref={messagesEndRef} />
        </Box>
      </Box>
      <Box sx={{ display: "flex", alignItems: "center", marginTop: 1 }}>
        <TextField
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          variant="outlined"
          size="small"
          // color="black"
          sx={{
            flexGrow: 1,
            mr: 1,
            backgroundColor: "white",
            borderRadius: "2px",
          }}
          InputProps={{
            style: { color: "black" },
          }}
        />
        <Button onClick={handleSend} variant="contained" sx={{ mr: 1 }}>
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default Chat;
