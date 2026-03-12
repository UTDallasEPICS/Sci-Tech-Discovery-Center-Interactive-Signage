from django.http import JsonResponse, StreamingHttpResponse
from .getpath import getpath
import json
import queue
import threading

# Global state
BUTTON_RECEIVED_ONCE = False
ID_RECEIVED_ONCE = False
CURRENT_DEN_ID = None
CURRENT_BUTTON = None
TIMEOUT_SECONDS = 15

active_timer = None
_state_lock = threading.Lock()

# --- SSE pub/sub ---
# Each connected client gets its own queue so all clients receive every event.
_subscribers = []
_subscribers_lock = threading.Lock()


def _publish_event(event):
    with _subscribers_lock:
        for q in list(_subscribers):
            q.put(event)


def _subscribe():
    q = queue.Queue()
    with _subscribers_lock:
        _subscribers.append(q)
    return q


def _unsubscribe(q):
    with _subscribers_lock:
        try:
            _subscribers.remove(q)
        except ValueError:
            pass


def _cancel_timer():
    """Cancel the active timer if running. Must be called with _state_lock held."""
    global active_timer
    if active_timer is not None:
        active_timer.cancel()
        active_timer = None


# Timeout handler — fires when no button is pressed within the timeout period.
def trigger_timeout():
    global CURRENT_BUTTON, BUTTON_RECEIVED_ONCE

    with _state_lock:
        # Guard: if a button was already pressed (or state was reset), do nothing.
        if BUTTON_RECEIVED_ONCE or not ID_RECEIVED_ONCE:
            return
        CURRENT_BUTTON = "en"
        BUTTON_RECEIVED_ONCE = True

    _publish_event({"type": "button_press_timeout", "language": "en"})


def showinfo(request):
    with _state_lock:
        if not ID_RECEIVED_ONCE:
            return JsonResponse({"error": "No denary ID received yet"}, status=400)
        if not BUTTON_RECEIVED_ONCE:
            return JsonResponse({"error": "No button press received yet"}, status=400)
        den_id = CURRENT_DEN_ID
        button = CURRENT_BUTTON

    data = getpath(den_id, button)
    status = 404 if "error" in data else 200
    return JsonResponse(data, status=status)


def receive_den_id(request):
    global ID_RECEIVED_ONCE, CURRENT_DEN_ID, active_timer

    with _state_lock:
        if ID_RECEIVED_ONCE:
            return JsonResponse(
                {"error": f"ID {CURRENT_DEN_ID} already received. No more requests till reset"},
                status=200,
            )

    denary_id = request.GET.get("id")
    if not denary_id:
        return JsonResponse({"error": "Missing id parameter"}, status=400)

    data = getpath(denary_id)
    if "error" in data:
        return JsonResponse({"error": "Invalid ID - not found in database"}, status=404)

    with _state_lock:
        CURRENT_DEN_ID = denary_id
        ID_RECEIVED_ONCE = True
        _cancel_timer()
        active_timer = threading.Timer(TIMEOUT_SECONDS, trigger_timeout)
        active_timer.start()

    _publish_event({"type": "scanned_id", "path": data["video_path"]})

    return JsonResponse({"OK": f"Successful. ID set to {CURRENT_DEN_ID}"}, status=200)


def receive_button_press(request):
    global BUTTON_RECEIVED_ONCE, CURRENT_BUTTON

    with _state_lock:
        _cancel_timer()
        if not ID_RECEIVED_ONCE:
            return JsonResponse(
                {"error": "No denary ID received yet. Cannot process button press."}, status=400
            )
        if BUTTON_RECEIVED_ONCE:
            return JsonResponse(
                {"error": f"Button {CURRENT_BUTTON} already received. No more requests till reset"},
                status=200,
            )

    button = request.GET.get("button")
    if not button:
        return JsonResponse({"error": "Missing button parameter"}, status=400)
    if button not in ["a", "b", "c"]:
        return JsonResponse({"error": "Invalid button parameter"}, status=400)

    button_map = {"a": "en", "b": "es", "c": "te"}
    language = button_map[button]

    with _state_lock:
        CURRENT_BUTTON = language
        BUTTON_RECEIVED_ONCE = True

    _publish_event({"type": "button_press", "language": language})

    return JsonResponse(
        {"OK": f"Button press validated and stored. Language set to {language}"}, status=200
    )


def restartflag(request):
    global BUTTON_RECEIVED_ONCE, ID_RECEIVED_ONCE, CURRENT_BUTTON, CURRENT_DEN_ID

    with _state_lock:
        _cancel_timer()
        BUTTON_RECEIVED_ONCE = False
        ID_RECEIVED_ONCE = False
        CURRENT_DEN_ID = None
        CURRENT_BUTTON = None

    return JsonResponse({"OK": "Flags reset successfully"}, status=200)


def sse_events(request):
    client_queue = _subscribe()

    def event_stream():
        try:
            while True:
                try:
                    event = client_queue.get(timeout=30)
                    etype = event.get("type")
                    payload = {k: v for k, v in event.items() if k != "type"}
                    yield f"event: {etype}\ndata: {json.dumps(payload)}\n\n"
                except queue.Empty:
                    yield ": heartbeat\n\n"
        finally:
            _unsubscribe(client_queue)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
