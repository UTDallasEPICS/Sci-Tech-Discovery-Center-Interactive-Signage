import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import LangaugeSelect from './components/languageSelect';
import VideoScreen from './components/videoScreen';
import ScanPage from './components/ScanPage';

function SSEController() {
  const navigate = useNavigate();

  useEffect(() => {
    const eventSource = new EventSource('/api/events/');

    eventSource.addEventListener('scanned_id', (event) => {
      const data = JSON.parse(event.data);
      navigate('/exploration', { state: data });
    });

    eventSource.addEventListener('button_press', (event) => {
      const data = JSON.parse(event.data);
      navigate('/video', { state: { lang: data.language } });
    });

    eventSource.addEventListener('button_press_timeout', (event) => {
      const data = JSON.parse(event.data);
      navigate('/video', { state: { lang: data.language } });
    });

    eventSource.onerror = () => {
      // EventSource auto-reconnects. If the server restarted, navigate home
      // so the user isn't stuck on a stale screen.
      if (window.location.pathname !== '/') {
        navigate('/');
      }
    };

    return () => {
      eventSource.close();
    };
  }, [navigate]);

  return null;
}

function App() {
  return (
    <main>
      <BrowserRouter>
        <SSEController />
        <Routes>
          <Route path="/" element={<ScanPage />} />
          <Route path="/exploration" element={<LangaugeSelect />} />
          <Route path="/video" element={<VideoScreen />} />
        </Routes>
      </BrowserRouter>
    </main>
  );
}

export default App;
