import os
import json
from typing import Dict, Any

#PUSH THIS TO GLOBAL SETTINGS STARTUP APPLICATION PROBABLY?

#seperate function for validating id?
default = "en"



'''
Provide langauge : PARAMETERS binary_id (str), lang(str)
Default english  : PARAMETERS binary_id(str) 
RETURNS dictionary containing name and video path
'''
def getpath(binary_id: str, lang: str = default) -> dict:
    
    #Reads JSON from same directory.
    #finds item by id and returns {'name': <name>, 'video_path': <path for lang>}.
    #Defaults to English if language not found.
    
    json_path = os.path.join(os.path.dirname(__file__), "testdata.json")
    if not os.path.exists(json_path):
        return {"error": "JSON Data file not found"}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # traverse through the whole json file to find matching id 
    for item in data:
        if (item.get("id") == binary_id):
    #       
            name_val = item.get("name")
            path_dict = item.get("path", {})
            relative_path = path_dict.get(lang, path_dict.get("en"))
            
            if relative_path:
                # Construct absolute path
                # Structure: ...Root/interactive-signage-backend/polls/getpath.py
                # We need to go up 3 levels where 'artifacts' folder is
                current_dir = os.path.dirname(os.path.abspath(__file__))
                backend_root = os.path.dirname(current_dir)
                repo_root = os.path.dirname(backend_root)
                
                video_path = os.path.join(repo_root, relative_path)
                return {"name": name_val, "video_path": video_path}
            
            return {"name": name_val, "video_path": None}

    #return error if id not found 
    return {"error": "ID match not found"}
