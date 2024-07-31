import React from 'react';
import ReactPlayer from 'react-player';

const VideoPlayer = ({ url }) => {
    console.log(url)
  return (
    <div style={{ position: 'relative', paddingTop: '46.25%' }}>
      <ReactPlayer
        url={url}
        controls
        width="100%"
        height="350px"
        style={{ position: 'absolute', top: '0', left: '0' }}
      />
    </div>
  );
};

export default VideoPlayer;
