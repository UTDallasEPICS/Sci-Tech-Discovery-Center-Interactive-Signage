import customtkinter as ctk
from customtkinter import filedialog
import os
from typing import Optional, Callable, Dict


class TagModal(ctk.CTkToplevel):
    """Modal for creating or editing an NFC tag with multi-language video support."""

    LANGUAGES = [
        ("en", "English"),
        ("es", "Spanish"),
        ("te", "Telugu"),
    ]

    def __init__(self, master, uid: str, existing_data: Optional[dict] = None,
                 on_save: Optional[Callable[[str, str, Dict[str, str]], None]] = None, **kwargs):
        super().__init__(master, **kwargs)

        self.geometry("500x520")
        self.title("New Tag Detected" if existing_data is None else f"Edit Tag: {uid}")

        self.transient(master)
        self.grab_set()

        self.uid = uid
        self.existing_data = existing_data
        self.on_save = on_save
        # Track selected file paths per language
        self.selected_videos: Dict[str, Optional[str]] = {}
        self.path_entries: Dict[str, ctk.CTkEntry] = {}

        if existing_data and existing_data.get("path"):
            for lang, rel_path in existing_data["path"].items():
                self.selected_videos[lang] = rel_path

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(self, text=f"Configure Tag", font=ctk.CTkFont(family="League Spartan", size=22, weight="bold"))
        header.pack(pady=(15, 5), padx=20)

        uid_label = ctk.CTkLabel(self, text=f"UID: {self.uid}", font=ctk.CTkFont(family="Open Sans Light", size=12), text_color="gray")
        uid_label.pack(pady=(0, 10))

        # Name Input
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(name_frame, text="Exhibit Name:", font=ctk.CTkFont(family="League Spartan", size=14)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="e.g. heart, brain, lungs", font=ctk.CTkFont(family="Open Sans Light", size=13))
        self.name_entry.pack(fill="x", pady=(3, 0))

        if self.existing_data:
            self.name_entry.insert(0, self.existing_data.get("name", ""))

        # Video Pickers — one per language
        videos_label = ctk.CTkLabel(self, text="Videos by Language:", font=ctk.CTkFont(family="League Spartan", size=14))
        videos_label.pack(anchor="w", padx=20, pady=(10, 3))

        for lang_code, lang_name in self.LANGUAGES:
            self._build_video_picker(lang_code, lang_name)

        # Save Button
        save_btn = ctk.CTkButton(self, text="Save Exhibit", font=ctk.CTkFont(family="League Spartan", size=16, weight="bold"), command=self._handle_save)
        save_btn.pack(pady=20)

    def _build_video_picker(self, lang_code: str, lang_name: str):
        """Build a single row: label + path display + browse button."""
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=3)

        ctk.CTkLabel(row, text=f"  {lang_name} ({lang_code}):", font=ctk.CTkFont(family="Open Sans Light", size=13), width=130, anchor="w").pack(side="left")

        path_entry = ctk.CTkEntry(row, state="disabled", font=ctk.CTkFont(family="Open Sans Light", size=11))
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.path_entries[lang_code] = path_entry

        # Show existing path if present
        existing_path = self.selected_videos.get(lang_code)
        if existing_path:
            self._update_path_display(lang_code, existing_path)

        browse_btn = ctk.CTkButton(row, text="Browse", width=60, font=ctk.CTkFont(family="League Spartan", size=12, weight="bold"),
                                   command=lambda lc=lang_code: self._browse_file(lc))
        browse_btn.pack(side="right")

    def _browse_file(self, lang_code: str):
        file_path = filedialog.askopenfilename(
            title=f"Select {lang_code.upper()} Video",
            filetypes=[("Video Files", "*.mp4")]
        )
        if file_path:
            self.selected_videos[lang_code] = file_path
            self._update_path_display(lang_code, file_path)

    def _update_path_display(self, lang_code: str, path: str):
        entry = self.path_entries[lang_code]
        entry.configure(state="normal")
        entry.delete(0, 'end')
        entry.insert(0, os.path.basename(path))
        entry.configure(state="disabled")

    def _handle_save(self):
        name = self.name_entry.get().strip().lower().replace(" ", "_")
        if not name:
            return

        # Require at least English video
        if not self.selected_videos.get("en"):
            return

        if self.on_save:
            self.on_save(self.uid, name, self.selected_videos)

        self.destroy()
