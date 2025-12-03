from django.shortcuts import render
from django.http import JsonResponse
from .getpath import getpath
import time

BUTTON_RECEIVED_ONCE = False # Flag to track if a button has been received
ID_RECEIVED_ONCE = False     # Flag to track if a denary ID has been received 
CURRENT_DEN_ID = None   # Placeholder for the current denary ID
CURRENT_BUTTON = None   # Placeholder for the current button state
SCREEN_TO = "splash-screen" # Placeholder for the next screen to display
LAST_BUTTON_TIME = None # Placeholder for the last button press time
TIMEOUT_SECONDS = 8000     # Timeout duration in seconds




#Function to return True if elapsed time >= TIMEOUT_SECONDS
def is_lang_timed_out():
    if LAST_BUTTON_TIME is None:
        return True  # No button ever pressed → use default
    return (time.time() - LAST_BUTTON_TIME) >= TIMEOUT_SECONDS


#Endpoint to show info based on current denary ID and button
def showinfo(request):
    global CURRENT_DEN_ID, CURRENT_BUTTON, ID_RECEIVED_ONCE, BUTTON_RECEIVED_ONCE, SCREEN_TO

    # Ensure the flow is valid
    if not ID_RECEIVED_ONCE:
        return JsonResponse({"error": "No denary ID received yet"}, status=400)

    if is_lang_timed_out() and not BUTTON_RECEIVED_ONCE:
        CURRENT_BUTTON = "en"  # Default to English if timed out without button press
        BUTTON_RECEIVED_ONCE = True

    if (not BUTTON_RECEIVED_ONCE) and (not CURRENT_BUTTON):
        return JsonResponse({"error": "No button press received yet"}, status=400)

    
    data = getpath(CURRENT_DEN_ID, CURRENT_BUTTON)



    status = 404 if "error" in data else 200
    return JsonResponse(data, status=status)


            
#Endpoint to receive and set denary ID
def receive_den_id(request):

    global ID_RECEIVED_ONCE, CURRENT_DEN_ID, LAST_BUTTON_TIME, SCREEN_TO
    denary_id = None

    if ID_RECEIVED_ONCE :
        return JsonResponse({"error": f"ID {CURRENT_DEN_ID} already received. No more requests till reset"}, status=200)
    #HTTP endpoint: /polls/api/set-id/?id=<id>

    denary_id = request.GET.get("id")

    #Reads `id` from query params and sets it as the current denary ID.
    #Returns 400 if id is missing, otherwise 200 with a success message.
    #not needed since it is certain that the id is being received from the scanner
    if not denary_id:
        return JsonResponse({"error": "Missing id parameter"}, status=400)

    #make dedicated function to validate id.   
    data = getpath(denary_id)

    if "Error" in data:
        #decide what to add for the placeholder
        return JsonResponse({"error: placeholder"}, status=404)


    CURRENT_DEN_ID = denary_id 

    LAST_BUTTON_TIME = time.time()

    ID_RECEIVED_ONCE = True

    SCREEN_TO = "language-screen"


    return JsonResponse({"OK": f"Successful. ID set to {CURRENT_DEN_ID}"}, 
    status=200)


#Endpoint to receive button press
def receive_button(request):
    #HTTP endpoint: /polls/api/button-press/
    #Handles button press events from the frontend.
    #Currently a placeholder that always returns success.
    global BUTTON_RECEIVED_ONCE, CURRENT_BUTTON, ID_RECEIVED_ONCE, LAST_BUTTON_TIME, SCREEN_TO
    
    button = None

    #example request: /api/button-press/?button=a

    #id checks:-
    #RETURN 400 if no ID is received(sequential flow broken)
    if not ID_RECEIVED_ONCE:
        return JsonResponse({"error": "No denary ID received yet. Cannot process button press."},
        status=400)
    

    if is_lang_timed_out():
        return JsonResponse(
            {"error": "Language selection timeout"},
            status=408
        )

    #RETURN 200 if button already received once
    if BUTTON_RECEIVED_ONCE:
        return JsonResponse({"error": f"Button {CURRENT_BUTTON} already received. No more requests till reset"}, status=200)


    #grab button 
    button = request.GET.get("button")


    #RETURN 400 if no parameter
    if not button:
        return JsonResponse({"error": "Missing button parameter"}, status=400)


    
    #RETURN 400 if invalid parameter
    if button not in ["a", "b", "c"]:
        return JsonResponse({"error": "Invalid button parameter"}, status=400)
    
    #button mapping
    match (button):
        case "a":
            button = "en"
            pass
        case "b":
            button = "es"
            pass
        case "c":
            button = "te"
            pass


    #STORE button and set flag
    CURRENT_BUTTON = button

    BUTTON_RECEIVED_ONCE = True

    LAST_BUTTON_TIME = time.time()

    SCREEN_TO = "video-screen"
    

    return JsonResponse({"OK": f"Button press validated and stored. Language set to {CURRENT_BUTTON}"},
    status=200)



#Endpoint to reset all globals
def restartflag(request):
    global BUTTON_RECEIVED_ONCE, ID_RECEIVED_ONCE, CURRENT_BUTTON, CURRENT_DEN_ID, LAST_BUTTON_TIME, SCREEN_TO


    #RESET all globals to initial state when cycle is complete
    BUTTON_RECEIVED_ONCE = False
    ID_RECEIVED_ONCE = False
    CURRENT_DEN_ID = None 
    CURRENT_BUTTON = None 
    LAST_BUTTON_TIME = None
    SCREEN_TO = "splash-screen"

    return JsonResponse({"OK": "Flags reset successfully"}, status=200)
