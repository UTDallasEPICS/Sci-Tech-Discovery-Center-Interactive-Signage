#change id_received_once to false when the reset endpoint is called
#add receive_den_id to urls.py

from django.shortcuts import render
from django.http import JsonResponse
from .getpath import getpath
import time
#from .validID import validID

BUTTON_RECEIVED_ONCE = False
ID_RECEIVED_ONCE = False

CURRENT_DEN_ID = None # Placeholder for the current denary ID
CURRENT_BUTTON = None # Placeholder for the current button state

LAST_BUTTON_TIME = None
TIMEOUT_SECONDS = 8 # Timeout duration in seconds


def is_lang_timed_out():
    """Return True if more than TIMEOUT_SECONDS passed since last button press."""
    if LAST_BUTTON_TIME is None:
        return True  # No button ever pressed → use default
    return (time.time() - LAST_BUTTON_TIME) > TIMEOUT_SECONDS



def showinfo(request):
    global CURRENT_DEN_ID, CURRENT_BUTTON, ID_RECEIVED_ONCE, BUTTON_RECEIVED_ONCE

    # Ensure the flow is valid
    if not ID_RECEIVED_ONCE:
        return JsonResponse({"error": "No denary ID received yet"}, status=400)

    if (not BUTTON_RECEIVED_ONCE) and (not CURRENT_BUTTON):
        return JsonResponse({"error": "No button press received yet"}, status=400)

    # USE THE STORED GLOBAL VALUES
    


    data = getpath(CURRENT_DEN_ID, CURRENT_BUTTON)

    status = 404 if "error" in data else 200
    return JsonResponse(data, status=status)



# getRelativepath   

def receive_den_id(request):

    global ID_RECEIVED_ONCE, CURRENT_DEN_ID
    global LAST_BUTTON_TIME
    denary_id = None

    if ID_RECEIVED_ONCE :
        return JsonResponse({"message": f"ID {CURRENT_DEN_ID} already received. No more requests till reset"}, status=200)
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

    #change screen to splash screen
    LAST_BUTTON_TIME = time.time()

    ID_RECEIVED_ONCE = True


    return JsonResponse({"message": f"Successful. ID set to {CURRENT_DEN_ID}"}, 
    status=200)



def receive_button_press(request):
    #HTTP endpoint: /polls/api/button-press/
    #Handles button press events from the frontend.
    #Currently a placeholder that always returns success.
    global BUTTON_RECEIVED_ONCE, CURRENT_BUTTON, ID_RECEIVED_ONCE, LAST_BUTTON_TIME
    
    button = None

    #example request: /api/button-press/?button=a

    #id checks:-
    #RETURN 400 if no ID is received(sequential flow broken)
    if not ID_RECEIVED_ONCE:
        return JsonResponse({"message": "No denary ID received yet. Cannot process button press."},
        status=400)
    

    if is_lang_timed_out():
        return JsonResponse(
            {"error": "Language selection timeout exceeded. Please scan ID again."},
            status=408
        )

    #DOESNT TAKE OTHER BUTTON PRESSES IF ONE HAS ALREADY BEEN RECEIVED 
    if BUTTON_RECEIVED_ONCE:
        return JsonResponse({"message": f"Button {CURRENT_BUTTON} already received. No more requests till reset"}, status=200)


    #Read and grab button
    button = request.GET.get("button")


    #if button is missing, return 400
    if not button:
        return JsonResponse({"error": "Missing button parameter"}, status=400)


    
    #if invalid button, return 400
    if button not in ["a", "b", "c"]:
        return JsonResponse({"error": "Invalid button parameter"}, status=400)
    
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

     #set global variables

    CURRENT_BUTTON = button
    BUTTON_RECEIVED_ONCE = True
    LAST_BUTTON_TIME = time.time()

    #change screen to lang 

    return JsonResponse({"message": f"Button press validated and stored. Language set to {CURRENT_BUTTON}"},
    status=200)

    #change screen start timer 


 #Reset the flag to allow re-calling receiveBinId
def restartflag(request):
    global BUTTON_RECEIVED_ONCE, ID_RECEIVED_ONCE, CURRENT_BUTTON, CURRENT_DEN_ID, LAST_BUTTON_TIME

    #reinitialize all flags and variables used 
    BUTTON_RECEIVED_ONCE = False
    ID_RECEIVED_ONCE = False
    CURRENT_DEN_ID = None 
    CURRENT_BUTTON = None 
    LAST_BUTTON_TIME = None

    return JsonResponse({"message": "Flags reset successfully"}, status=200)

