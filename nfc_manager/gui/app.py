import customtkinter as ctk
from PIL import Image
from typing import Optional, Dict
from data.manager import DataManager
from nfc_reader.base import BaseNFCReader
from nfc_reader.mock_reader import MockNFCReader
from .views import ManageTagsView
from .modals import TagModal
import os


class App(ctk.CTk):
    def __init__(self, data_manager: DataManager, nfc_reader: BaseNFCReader):
        super().__init__()

        self.data_manager = data_manager
        self.nfc_reader = nfc_reader

        # Setup Window
        self.title("NFC Tag Manager")
        self.geometry("850x650")
        ctk.set_appearance_mode("System")

        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Navigation sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#73008f")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Load and place the logo
        logo_path = os.path.join(os.path.dirname(__file__), 'logo_small.png')
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(light_image=Image.open(logo_path),
                                    dark_image=Image.open(logo_path),
                                    size=(120, 120))
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="", image=logo_img)
            self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        else:
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Tag Manager", font=ctk.CTkFont(family="League Spartan", size=24, weight="bold"), text_color="#ffffff")
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Reader: Connected",
                                        font=ctk.CTkFont(family="Open Sans Light", size=14, weight="bold"),
                                        text_color="#fffd24")
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Create views
        self.manage_view = ManageTagsView(
            self,
            data_manager=self.data_manager,
            on_edit_callback=self.open_tag_modal
        )
        self.manage_view.grid(row=0, column=1, sticky="nsew")

        # Mock Testing Controls (only if using MockNFCReader)
        if isinstance(self.nfc_reader, MockNFCReader):
            mock_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
            mock_frame.grid(row=5, column=0, padx=20, pady=20, sticky="s")
            ctk.CTkLabel(mock_frame, text="Dev: Simulate Scan", text_color="#ffffff", font=ctk.CTkFont(family="League Spartan", size=14)).pack(pady=5)

            self.mock_uid_entry = ctk.CTkEntry(mock_frame, placeholder_text="Enter UID...", font=ctk.CTkFont(family="Open Sans Light", size=13),
                                               fg_color="#ffffff", text_color="#000000")
            self.mock_uid_entry.pack(padx=10, pady=5)
            self.mock_uid_entry.insert(0, "1212866967841409")

            ctk.CTkButton(mock_frame, text="Simulate", command=self._simulate_scan, font=ctk.CTkFont(family="League Spartan", size=14, weight="bold")).pack(padx=10, pady=10)

        # Hook up NFC callback
        self.nfc_reader.set_callback(self.on_tag_scanned)

    def _simulate_scan(self):
        uid = self.mock_uid_entry.get().strip()
        if uid:
            self.nfc_reader.simulate_scan(uid)

    def open_tag_modal(self, tag_data: dict = None, uid: str = None):
        """Open the add/edit tag modal."""
        if tag_data:
            target_uid = tag_data.get('uid')
            existing_data = tag_data
        else:
            target_uid = uid
            existing_data = self.data_manager.get_tag(uid)

        def _open():
            modal = TagModal(
                self,
                uid=target_uid,
                existing_data=existing_data,
                on_save=self.save_tag_handler
            )
            modal.focus()

        self.after(0, _open)

    def on_tag_scanned(self, uid: str):
        """Triggered via NFC reader thread when a tap happens."""
        self.open_tag_modal(uid=uid)

    def save_tag_handler(self, uid: str, name: str, video_paths: Dict[str, str]):
        """Called by the modal when the user saves exhibit data."""
        existing = self.data_manager.get_tag(uid)

        try:
            if existing:
                self.data_manager.update_tag(uid, name, video_paths)
            else:
                self.data_manager.add_tag(uid, name, video_paths)
        except Exception as e:
            print(f"Error saving data: {e}")

        self.manage_view.refresh_list()
