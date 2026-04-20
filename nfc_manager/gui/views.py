import customtkinter as ctk
from typing import Callable


class ManageTagsView(ctk.CTkFrame):
    """View to list and manage all existing exhibit tags."""

    def __init__(self, master, data_manager, on_edit_callback: Callable[[dict], None], **kwargs):
        super().__init__(master, **kwargs)
        self.data_manager = data_manager
        self.on_edit_callback = on_edit_callback

        # Header
        self.header_label = ctk.CTkLabel(self, text="Manage Exhibits", font=ctk.CTkFont(family="League Spartan", size=28, weight="bold"))
        self.header_label.pack(pady=(20, 10), padx=20, anchor="w")

        # Scrollable Frame for the list
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_list()

    def refresh_list(self):
        """Re-render the list of tags."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tags = self.data_manager.get_all_tags()

        if not tags:
            empty_label = ctk.CTkLabel(self.scroll_frame, text="No exhibits configured. Scan a tag to add one.",
                                       font=ctk.CTkFont(family="Open Sans Light", size=14), text_color="gray")
            empty_label.pack(pady=40)
            return

        for tag in tags:
            self._create_tag_row(tag)

    def _create_tag_row(self, tag: dict):
        """Create a UI row for a single exhibit tag."""
        row = ctk.CTkFrame(self.scroll_frame)
        row.pack(fill="x", pady=5)

        # Info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        name_label = ctk.CTkLabel(info_frame, text=tag.get('name', 'Unknown'),
                                  font=ctk.CTkFont(family="League Spartan", size=18, weight="bold"))
        name_label.pack(anchor="w")

        uid_label = ctk.CTkLabel(info_frame, text=f"UID: {tag.get('uid')}",
                                 font=ctk.CTkFont(family="Open Sans Light", size=12), text_color="gray")
        uid_label.pack(anchor="w")

        # Show which languages have videos
        path_dict = tag.get("path", {})
        langs = ", ".join(sorted(path_dict.keys())) if path_dict else "none"
        lang_label = ctk.CTkLabel(info_frame, text=f"Videos: {langs}",
                                  font=ctk.CTkFont(family="Open Sans Light", size=12), text_color="gray")
        lang_label.pack(anchor="w")

        # Actions
        edit_btn = ctk.CTkButton(row, text="Edit", width=60,
                                 font=ctk.CTkFont(family="League Spartan", size=14, weight="bold"),
                                 command=lambda t=tag: self.on_edit_callback(t))
        edit_btn.pack(side="right", padx=5)

        delete_btn = ctk.CTkButton(row, text="Delete", width=60,
                                   font=ctk.CTkFont(family="League Spartan", size=14, weight="bold"),
                                   fg_color="#e53935", hover_color="#b71c1c",
                                   command=lambda u=tag['uid']: self._confirm_delete(u))
        delete_btn.pack(side="right", padx=10)

    def _confirm_delete(self, uid: str):
        """Delete tag and refresh list."""
        self.data_manager.delete_tag(uid)
        self.refresh_list()
