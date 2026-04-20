import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional


class DataManager:
    """Manages NFC tag data and writes exhibits directly to the signage project."""

    def __init__(self, config_path: str = "config.json"):
        self.base_dir = Path(os.path.dirname(os.path.abspath(config_path)) if config_path != "config.json" else ".")

        # Load config
        config = self._load_config(config_path)
        signage_rel = config.get("signage_project_path", "../Sci-Tech-Discovery-Center-Interactive-Signage")
        self.languages = config.get("languages", ["en", "es", "te"])

        # Resolve signage project paths
        self.signage_root = (self.base_dir / signage_rel).resolve()
        self.artifacts_dir = self.signage_root / "artifacts"
        self.exhibits_file = self.signage_root / "interactive-signage-backend" / "polls" / "exhibits.json"

        # Ensure artifacts directory exists
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

        # Initialize exhibits.json if it doesn't exist
        if not self.exhibits_file.exists():
            self._save_exhibits([])

    def _load_config(self, config_path: str) -> dict:
        """Load config.json."""
        path = Path(config_path)
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def _load_exhibits(self) -> List[dict]:
        """Load exhibits data from the signage project's exhibits.json."""
        if not self.exhibits_file.exists():
            return []
        try:
            with open(self.exhibits_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_exhibits(self, data: List[dict]):
        """Save exhibits data to the signage project's exhibits.json."""
        self.exhibits_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.exhibits_file, 'w') as f:
            json.dump(data, f, indent=4)

    def _copy_video(self, name: str, lang: str, source_path: str) -> str:
        """Copy a video file into the signage artifacts directory.
        Returns the relative path used in exhibits.json (e.g. 'artifacts/heart/en.mp4').
        """
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Video file not found: {source_path}")

        dest_dir = self.artifacts_dir / name
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / f"{lang}.mp4"
        shutil.copy2(source, dest_file)

        return f"artifacts/{name}/{lang}.mp4"

    def _delete_artifact_dir(self, name: str):
        """Remove an artifact's video directory."""
        artifact_dir = self.artifacts_dir / name
        if artifact_dir.exists():
            shutil.rmtree(artifact_dir)

    def get_all_tags(self) -> List[dict]:
        """Return all exhibits as a list of dicts with uid included."""
        exhibits = self._load_exhibits()
        result = []
        for item in exhibits:
            tag = {
                "uid": item["id"],
                "name": item["name"],
                "path": item.get("path", {}),
            }
            result.append(tag)
        return result

    def get_tag(self, uid: str) -> Optional[dict]:
        """Get a single exhibit by UID."""
        exhibits = self._load_exhibits()
        for item in exhibits:
            if item.get("id") == uid:
                return {
                    "uid": item["id"],
                    "name": item["name"],
                    "path": item.get("path", {}),
                }
        return None

    def add_tag(self, uid: str, name: str, video_paths: Dict[str, str]) -> dict:
        """Add a new exhibit.

        Args:
            uid: NFC tag decimal ID string
            name: Exhibit/artifact name (used as folder name, e.g. 'heart')
            video_paths: Dict mapping language codes to source file paths,
                         e.g. {'en': '/path/to/en.mp4', 'es': '/path/to/es.mp4'}
        """
        exhibits = self._load_exhibits()

        # Check for duplicate UID
        for item in exhibits:
            if item.get("id") == uid:
                raise ValueError(f"Tag {uid} already exists.")

        # Copy videos and build path dict
        path_dict = {}
        for lang, source in video_paths.items():
            if source:
                path_dict[lang] = self._copy_video(name, lang, source)

        exhibit = {
            "id": uid,
            "name": name,
            "path": path_dict,
        }
        exhibits.append(exhibit)
        self._save_exhibits(exhibits)

        return {"uid": uid, "name": name, "path": path_dict}

    def update_tag(self, uid: str, name: str, video_paths: Optional[Dict[str, str]] = None) -> dict:
        """Update an existing exhibit.

        Args:
            uid: NFC tag decimal ID string
            name: New exhibit name
            video_paths: Optional dict of language → source file path.
                         Only languages with non-None values are updated.
        """
        exhibits = self._load_exhibits()

        target = None
        for item in exhibits:
            if item.get("id") == uid:
                target = item
                break

        if target is None:
            raise KeyError(f"Tag {uid} not found.")

        old_name = target["name"]
        path_dict = target.get("path", {})

        # If name changed, move the artifact directory
        if name != old_name:
            old_dir = self.artifacts_dir / old_name
            new_dir = self.artifacts_dir / name
            if old_dir.exists():
                old_dir.rename(new_dir)
            # Update all path references
            path_dict = {lang: f"artifacts/{name}/{lang}.mp4" for lang, p in path_dict.items()}

        # Copy any new video files
        if video_paths:
            for lang, source in video_paths.items():
                if source and not source.startswith("artifacts/"):
                    # It's a new file to copy (not an existing relative path)
                    path_dict[lang] = self._copy_video(name, lang, source)

        target["name"] = name
        target["path"] = path_dict
        self._save_exhibits(exhibits)

        return {"uid": uid, "name": name, "path": path_dict}

    def delete_tag(self, uid: str):
        """Delete an exhibit and its video files."""
        exhibits = self._load_exhibits()
        new_exhibits = []
        deleted_name = None

        for item in exhibits:
            if item.get("id") == uid:
                deleted_name = item.get("name")
            else:
                new_exhibits.append(item)

        if deleted_name:
            self._delete_artifact_dir(deleted_name)

        self._save_exhibits(new_exhibits)
