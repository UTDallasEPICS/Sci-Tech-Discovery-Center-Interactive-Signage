import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function VideoScreen() {
  const [videoData, setVideoData] = useState(null);
  const navigate = useNavigate();

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
    <div className="w-full h-screen flex items-center justify-center bg-black">
      <video
        src={videoData.video_path}
        controls
        muted
        autoPlay
        onEnded={handleVideoEnd}
        playsInline
        className="w-full h-full rounded-2xl shadow-lg object-cover"
      />
    </div>
  );
}
