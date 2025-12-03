import React from "react";
import sampleVideo from "../assets/video.mp4"; 

export default function VideoScreen() {
  return (
    <div className="w-full h-screen flex items-center justify-center bg-black">
      <video
        src={sampleVideo}
        controls
        muted
        autoPlay
        loop
        playsInline
        poster="/src/assets/video-poster.jpg" 
        className="w-full h-full rounded-2xl shadow-lg object-cover"
      />
    </div>
  );
}