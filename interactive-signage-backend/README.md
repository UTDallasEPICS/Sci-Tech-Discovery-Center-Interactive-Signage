# Interactive Signage Backend

This folder contains the backend server for the Interactive Signage project.

## Overview
The backend handles:
- Serving API endpoints for the frontend
    api/showinfo/?id=<id>&lang=<lang> <- reads `id` and *optional* `lang` from query params and calls getpath().
    api/receive-id/?id=<id> <-to send id from HAL(rfid grabber) to backend
    api/resetinfo/ <- reset flag 
- Managing JSON data storage and retrieval
- Handling business logic for interactive signage
