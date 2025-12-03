import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LangaugeSelect from './components/langaugeSelect';
import VideoScreen from './components/videoScreen';
import ScanPage from './components/ScanPage';

function App() {
  // State to track which screen to display
  const [view, setView] = useState('welcome');
  
 
  const [eventData, setEventData] = useState(null);

  useEffect(() => {
    // Replace '/api/sse-endpoint' with your actual backend URL
    const eventSource = new EventSource('http://localhost:8000/api/events');

    // listening for messages
    eventSource.onmessage = (event) => {
      console.log("New event received:", event.data);
      
      // Parse data if your server sends JSON
      const parsedData = JSON.parse(event.data);
      setEventData(parsedData);

      // 3. Trigger the screen change
      setView('exploration');
    };


    return () => {
      eventSource.close();
    };
  }, []); 

  // 5. Conditional Rendering
  return (
    <main>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ScanPage/>}/>
          <Route path="/exploration" element={<LangaugeSelect/>}/>
          <Route path="/video" element={<VideoScreen/>}/>
        </Routes>
      </BrowserRouter>
    </main>
  );
}

export default App;