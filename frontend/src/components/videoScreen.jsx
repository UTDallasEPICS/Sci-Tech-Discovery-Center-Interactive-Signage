<<<<<<< HEAD
import { useEffect, useState } from "react";
=======
import { useEffect, useState, useRef } from "react";
>>>>>>> 41d1071 (Final version from Pi)
import { useNavigate } from "react-router-dom";

export default function VideoScreen() {
  const [videoData, setVideoData] = useState(null);
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const progressRef = useRef(null);

  useEffect(() => {
    fetch("/api/showinfo/", {
      method: "GET",
      cache: "no-store",
      headers: {
        Pragma: "no-cache",
        "Cache-Control": "no-cache",
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          console.error("ShowInfo error:", data.error);
        } else {
          setVideoData(data);
        }
      })
      .catch((err) => console.error("ShowInfo fetch failed:", err.message));
  }, []);

  useEffect (() => {
    const video = videoRef.current;
    const progressBar = progressRef.current;

    if (!video || !progressBar) return;

    const updateProgress = () => {
      const percent = (video.currentTime / video.duration) * 100;
      progressBar.style.width = percent + "%";
    };

    video.addEventListener("timeupdate", updateProgress);

    return () => video.removeEventListener("timeupdate", updateProgress);
  }, [videoData]); // run when videoData is loaded

  const handleVideoEnd = async () => {
    try {
      await fetch("/api/resetinfo/");
    } catch (error) {
      console.error("Error resetting flags:", error);
    }
    navigate("/");
  };

  if (!videoData || !videoData.video_path) {
    return (
      <div className="w-full h-screen bg-black flex items-center justify-center text-white">
        Loading Video...
      </div>
    );
  }

  return (
    <div className="w-full h-screen flex items-center justify-center bg-black overflow-hidden">
      <video
        src={videoData.video_path}
        muted
        autoPlay
        onEnded={handleVideoEnd}
        playsInline
<<<<<<< HEAD
=======
        ref={videoRef}
>>>>>>> 41d1071 (Final version from Pi)
        className="w-full h-full rounded-2xl shadow-lg object-cover"
      />

      <div
        className="absolute z-2 bottom-0 left-0 h-2 bg-[#7651E0] rounded mt-2"
        ref={progressRef}
      ></div>

    </div>
  );
}
