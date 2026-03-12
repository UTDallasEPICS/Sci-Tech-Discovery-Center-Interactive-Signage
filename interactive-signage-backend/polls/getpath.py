import os
import json

default = "en"


def getpath(binary_id: str, lang: str = default) -> dict:
    """
    Looks up artifact by ID and returns a URL path for the video.
    Returns {'name': ..., 'video_path': '/artifacts/...'} or {'error': ...}.
    """
    json_path = os.path.join(os.path.dirname(__file__), "testdata.json")
    if not os.path.exists(json_path):
        return {"error": "JSON Data file not found"}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        if item.get("id") == binary_id:
            name_val = item.get("name")
            path_dict = item.get("path", {})
            relative_path = path_dict.get(lang, path_dict.get("en"))

            if not relative_path:
                return {"error": f"No video path found for artifact '{name_val}'"}

            # Return a URL path the browser can fetch, not a filesystem path.
            # Django serves /artifacts/ from frontend/dist/artifacts/.
            video_path = "/" + relative_path
            return {"name": name_val, "video_path": video_path}

    return {"error": "ID match not found"}
