import os
import json

default = "en"


def _load_json(path):
    """Load and return a JSON file, or None if missing/invalid."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def getpath(binary_id: str, lang: str = default) -> dict:
    """
    Looks up artifact by ID and returns a URL path for the video.
    Checks exhibits.json (managed by NFC Manager) first, then falls back
    to testdata.json (placeholder content).
    Returns {'name': ..., 'video_path': '/artifacts/...'} or {'error': ...}.
    """
    base_dir = os.path.dirname(__file__)
    exhibits_path = os.path.join(base_dir, "exhibits.json")
    testdata_path = os.path.join(base_dir, "testdata.json")

    # Load exhibits first, then testdata as fallback. Merge both lists.
    all_items = []
    for path in (exhibits_path, testdata_path):
        items = _load_json(path)
        if items:
            all_items.extend(items)

    if not all_items:
        return {"error": "No data files found"}

    for item in all_items:
        if item.get("id") == binary_id:
            name_val = item.get("name")
            path_dict = item.get("path", {})
            relative_path = path_dict.get(lang, path_dict.get("en"))

            if not relative_path:
                return {"error": f"No video path found for artifact '{name_val}'"}

            # Return a URL path the browser can fetch, not a filesystem path.
            # Django serves /artifacts/ from the project-root artifacts/ directory.
            video_path = "/" + relative_path
            return {"name": name_val, "video_path": video_path}

    return {"error": "ID match not found"}
