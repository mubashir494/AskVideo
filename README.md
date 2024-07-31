# AskVideo ( Video Interaction Application )

## Overview

This project is a video interaction application that allows users to upload a video, interact with it via a chat interface, view the transcript, and see a summary of the video content. The application uses Groq as the inference engine for processing the videos and ChromaDB for storing vectors.

## Features

- **Video Upload**: Users can upload a video file.
- **Video Playback**: The uploaded video can be played back in the browser.
- **Transcription**: The video is transcribed using WhisperX.
- **Chat Interface**: Users can interact with the video content through a chat interface.
- **Summary**: A summary of the video content is displayed.
- **Reset Functionality**: Users can reset the application to upload a new video.

## Technologies Used

- **Frontend**: React, Material-UI
- **Backend**: Node.js, Express
- **Inference Engine**: Groq
- **Vector Storage**: ChromaDB

## Prerequisites

- Node.js
- Yarn or npm
- Groq Inference Engine
- ChromaDB

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/video-interaction-app.git
    cd video-interaction-app
    ```

2. **Install dependencies**:

    ```bash
    yarn install
    ```

    or

    ```bash
    npm install
    ```

3. **Set up the environment variables**:

    Create a `.env` file in the root directory and add the following environment variables:

    ```env
    REACT_APP_URL=http://localhost:5000
    GROQ_API_KEY=your-groq-api-key
    CHROMADB_URI=your-chromadb-uri
    ```

4. **Start the development server**:

    ```bash
    yarn start
    ```

    or

    ```bash
    npm start
    ```

    The application should now be running on `http://localhost:3000`.

## Usage

1. **Upload a Video**: On the home page, click the "Upload" button to upload a video file.
2. **Interact with the Video**:
    - **Playback**: The video will be played back in the browser.
    - **Transcript**: View the transcript of the video below the player.
    - **Chat**: Use the chat interface on the right to interact with the video content.
    - **Summary**: View a summary of the video content below the chat interface.
3. **Reset**: Click the "Reset" button to clear the current video and upload a new one.


