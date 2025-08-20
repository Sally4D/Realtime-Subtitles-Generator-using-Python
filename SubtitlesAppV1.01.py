import tkinter as tk
from tkinter import font as tkfont
from tkinter import colorchooser, messagebox
import customtkinter as ctk
import soundcard as sc
import vosk
import queue
import threading
import json
import sys
import os
import numpy as np
import collections
import textwrap
import time
import webbrowser
import requests
import zipfile
import subprocess

# --- Constants ---
SETTINGS_FILE = "settings.json"
VOSK_MODELS_URL = "https://alphacephei.com/vosk/models"
DEVELOPER_URL = "https://github.com/sally4d"
LinkedIn_URL = "https://www.linkedin.com/in/oscurprof/"
SUPPORT_URL = "https://oscurprofundo.gumroad.com/l/dmkbes"

# --- Language Model Definitions ---
LANGUAGE_MODELS = {
    "English": "vosk-model-small-en-us-0.15",
    "English Large LGraph (128M)": "vosk-model-en-us-0.22-lgraph",
    "English Large (1.8G)": "vosk-model-en-us-0.22",
    "English Large Gigaspeech (2.3G)": "vosk-model-en-us-0.42-gigaspeech",

    "Indian English Large (1G)": "vosk-model-en-in-0.5",
    "Indian English Small (36M)": "vosk-model-small-en-in-0.4",

    "Chinese Small (42M)": "vosk-model-small-cn-0.22",
    "Chinese Large (1.3G)": "vosk-model-cn-0.22",
    "Chinese MultiCN (1.5G)": "vosk-model-cn-kaldi-multicn-0.15",

    "Russian Large (1.8G)": "vosk-model-ru-0.42",
    "Russian Small (45M)": "vosk-model-small-ru-0.22",
    "Russian Large v0.22 (1.5G)": "vosk-model-ru-0.22",
    "Russian Large v0.10 (2.5G)": "vosk-model-ru-0.10",

    "French Small (41M)": "vosk-model-small-fr-0.22",
    "French Large (1.4G)": "vosk-model-fr-0.22",
    "French PGuyot Small (39M)": "vosk-model-small-fr-pguyot-0.3",
    "French Linto (1.5G)": "vosk-model-fr-0.6-linto-2.2.0",

    "German Large (1.9G)": "vosk-model-de-0.21",
    "German Large Tuda (4.4G)": "vosk-model-de-tuda-0.6-900k",
    "German Zamia Small (49M)": "vosk-model-small-de-zamia-0.3",
    "German Small (45M)": "vosk-model-small-de-0.15",

    "Spanish Small (39M)": "vosk-model-small-es-0.42",
    "Spanish Large (1.4G)": "vosk-model-es-0.42",

    "Portuguese Small (31M)": "vosk-model-small-pt-0.3",
    "Portuguese FalaBrasil (1.6G)": "vosk-model-pt-fb-v0.1.1-20220516_2113",

    "Greek Large (1.1G)": "vosk-model-el-gr-0.7",

    "Turkish Small (35M)": "vosk-model-small-tr-0.3",

    "Vietnamese Small (32M)": "vosk-model-small-vn-0.4",
    "Vietnamese Large (78M)": "vosk-model-vn-0.4",

    "Italian Small (48M)": "vosk-model-small-it-0.22",
    "Italian Large (1.2G)": "vosk-model-it-0.22",

    "Dutch Small (39M)": "vosk-model-small-nl-0.22",
    "Dutch Medium (860M)": "vosk-model-nl-spraakherkenning-0.6",
    "Dutch LGraph (100M)": "vosk-model-nl-spraakherkenning-0.6-lgraph",

    "Catalan Small (42M)": "vosk-model-small-ca-0.4",

    "Arabic MGB2 (318M)": "vosk-model-ar-mgb2-0.4",
    "Arabic Linto (1.3G)": "vosk-model-ar-0.22-linto-1.1.0",
    "Arabic Tunisian Small (158M)": "vosk-model-small-ar-tn-0.1-linto",
    "Arabic Tunisian (517M)": "vosk-model-ar-tn-0.1-linto",

    "Farsi Large (1.6G)": "vosk-model-fa-0.42",
    "Farsi Small (53M)": "vosk-model-small-fa-0.42",
    "Farsi Large v0.5 (1G)": "vosk-model-fa-0.5",
    "Farsi Small v0.5 (60M)": "vosk-model-small-fa-0.5",

    "Filipino Medium (320M)": "vosk-model-tl-ph-generic-0.6",

    "Ukrainian Nano (73M)": "vosk-model-small-uk-v3-nano",
    "Ukrainian Small (133M)": "vosk-model-small-uk-v3-small",
    "Ukrainian Large (343M)": "vosk-model-uk-v3",
    "Ukrainian Large LGraph (325M)": "vosk-model-uk-v3-lgraph",

    "Kazakh Small (42M)": "vosk-model-small-kz-0.15",
    "Kazakh Large (378M)": "vosk-model-kz-0.15",

    "Swedish Small (289M)": "vosk-model-small-sv-rhasspy-0.15",

    "Japanese Small (48M)": "vosk-model-small-ja-0.22",
    "Japanese Large (1G)": "vosk-model-ja-0.22",

    "Esperanto Small (42M)": "vosk-model-small-eo-0.42",

    "Hindi Small (42M)": "vosk-model-small-hi-0.22",
    "Hindi Large (1.5G)": "vosk-model-hi-0.22",

    "Czech Small (44M)": "vosk-model-small-cs-0.4-rhasspy",

    "Polish Small (50M)": "vosk-model-small-pl-0.22",

    "Uzbek Small (49M)": "vosk-model-small-uz-0.22",

    "Korean Small (82M)": "vosk-model-small-ko-0.22",

    "Breton (70M)": "vosk-model-br-0.8",

    "Gujarati Large (700M)": "vosk-model-gu-0.42",
    "Gujarati Small (100M)": "vosk-model-small-gu-0.42",

    "Tajik Large (327M)": "vosk-model-tg-0.22",
    "Tajik Small (50M)": "vosk-model-small-tg-0.22",

    "Telugu Small (58M)": "vosk-model-small-te-0.42",

    "Speaker Identification (13M)": "vosk-model-spk-0.4"
}

# --- Global Queues ---
audio_queue = queue.Queue()
caption_queue = queue.Queue()

# --- Global State ---
last_caption_time = time.time()
stop_threads = threading.Event()


class ToolTip:
    """
    Creates a modern, theme-aware tooltip for a given widget using customtkinter.
    The tooltip appears after a short delay and follows the application's theme.
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        """Schedules the tooltip to appear after a delay."""
        self.schedule()

    def leave(self, event=None):
        """Cancels the scheduled tooltip and hides it if visible."""
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """Schedules `showtip` to be called after 500ms."""
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        """Cancels the scheduled `showtip` call."""
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self):
        """Creates and displays the tooltip window."""
        if self.tooltip_window:
            return

        # Calculate tooltip position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.attributes("-topmost", True)

        # Use CTkLabel for theme-aware styling
        label = ctk.CTkLabel(self.tooltip_window, text=self.text,
                             wraplength=300,
                             justify="left",
                             corner_radius=6)
        label.pack(padx=5, pady=5)

    def hidetip(self):
        """Destroys the tooltip window if it exists."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


class SearchableComboBox(ctk.CTkComboBox):
    """
    A CTkComboBox that filters its values based on user input.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_values = self.cget("values")[:]

        self._entry.bind("<KeyRelease>", self._on_keyrelease)
        # Use a custom command wrapper to reset values after selection
        self._original_command = self.cget("command")
        self.configure(command=self._on_selection)

    def _on_keyrelease(self, event):
        """Filters the combobox values based on the entry text."""
        # Don't filter on navigation keys
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        current_text = self.get().lower()

        if current_text:
            filtered_values = [v for v in self._original_values if current_text in v.lower()]
        else:
            filtered_values = self._original_values[:]

        # Update the values and reopen the dropdown to show the filtered list
        self.configure(values=filtered_values)
        if self._dropdown_menu is not None and self._dropdown_menu.winfo_exists():
            self._dropdown_menu.destroy()
        self._open_dropdown_menu()

    def _on_selection(self, value):
        """Called when a value is selected. Resets the list and calls original command."""
        self.set(value)  # Set the value in the entry
        self.configure(values=self._original_values)  # Reset the list
        if self._original_command:
            self._original_command(value)

    def set(self, value):
        """Sets the value and resets the list of choices."""
        super().set(value)
        self.configure(values=self._original_values)


class SettingsManager:
    """Handles loading and saving settings to a JSON file."""

    def __init__(self):
        self.settings_path = SETTINGS_FILE
        self.default_settings = {
            "subtitle_color": "#FFFFFF",
            "background_color": "#000000",
            "background_opacity": 0.75,
            "subtitle_size": 16,
            "subtitle_font": "Arial",
            "language": "English",  # default language
            "block_size": 3000,
            # lower size will increase how quickly subtitles are generated, but it also cost more Resources
            "model_path": LANGUAGE_MODELS["English"],  # default language Model
            "window_width": 1200,  # width of subtitle window
            "window_height": 70,  # height of subtitle window
            "window_padding": 20,
            "delay_threshold": 3.0,  # time it should wait before clearing captions if there's no audio
            "ran_before": False,  # to track first run
            "show_about_on_startup": True,  # setting for showing about window
            "appearance_mode": "dark"  # setting for dark/light mode
        }
        self.settings, self.is_first_run = self.load_settings()

    def load_settings(self):
        is_first_run = not os.path.exists(self.settings_path)
        try:
            if not is_first_run:
                with open(self.settings_path, 'r') as f:
                    settings = json.load(f)
                    for key, value in self.default_settings.items():
                        settings.setdefault(key, value)
                    return settings, False
            else:
                self.save_settings(self.default_settings)
                updated_settings = self.default_settings.copy()
                updated_settings["ran_before"] = True
                self.save_settings(updated_settings)
                return self.default_settings, True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings file: {e}. Using defaults.")
            return self.default_settings.copy(), False

    def save_settings(self, settings):
        self.settings = settings
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}")


class AboutWindow(ctk.CTkToplevel):
    """The 'About' window providing app information and links."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Live Captions")
        self.geometry("550x450")
        self.transient(parent)
        self.center_window()
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Live Captions", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0,
                                                                                                pady=(20, 10))

        about_text = ("This application provides real-time transcription of your system's audio output, "
                      "displaying it as an overlay on your screen. It's designed to be a simple, "
                      "unobtrusive tool for anyone who needs live captions.")
        ctk.CTkLabel(self, text=about_text, wraplength=500, justify="left").grid(row=1, column=0, padx=20, pady=10)

        controls_text = ("Controls:\n"
                         "• Left-click and drag the caption bar to move it.\n"
                         "• Right-click to open the context menu for Settings or to Exit.")
        ctk.CTkLabel(self, text=controls_text, justify="left").grid(row=2, column=0, padx=20, pady=10, sticky="w")

        dev_text = ("This fantastic tool was developed by oscurprof, a developer dedicated to creating "
                    "useful and accessible software.")
        ctk.CTkLabel(self, text=dev_text, wraplength=500).grid(row=3, column=0, padx=20, pady=10)

        support_text = ("Need help or have suggestions? We're here to assist you!")
        ctk.CTkLabel(self, text=support_text, wraplength=500).grid(row=4, column=0, padx=20, pady=5)

        links_frame = ctk.CTkFrame(self, fg_color="transparent")
        links_frame.grid(row=5, column=0, pady=15)

        # Theme-aware link color: (dark_mode_color, light_mode_color)
        link_color = ("#A5C8E4", "#1F6AA5")

        dev_link2 = ctk.CTkLabel(links_frame, text="Meet the Dev", text_color=link_color, cursor="hand2",
                                 font=ctk.CTkFont(underline=True))
        dev_link2.pack(side="left", padx=15)
        dev_link2.bind("<Button-1>", lambda e: webbrowser.open(LinkedIn_URL))

        dev_link = ctk.CTkLabel(links_frame, text="Dev's GitHub", text_color=link_color, cursor="hand2",
                                font=ctk.CTkFont(underline=True))
        dev_link.pack(side="left", padx=15)
        dev_link.bind("<Button-1>", lambda e: webbrowser.open(DEVELOPER_URL))


        support_link = ctk.CTkLabel(links_frame, text="Support the Dev", text_color='green', cursor="hand2",
                                    font=ctk.CTkFont(underline=True))
        support_link.pack(side="left", padx=15)
        support_link.bind("<Button-1>", lambda e: webbrowser.open(SUPPORT_URL))

        vosk_link = ctk.CTkLabel(links_frame, text="Vosk Models", text_color=link_color, cursor="hand2",
                                 font=ctk.CTkFont(underline=True))
        vosk_link.pack(side="left", padx=15)
        vosk_link.bind("<Button-1>", lambda e: webbrowser.open(VOSK_MODELS_URL))

        ctk.CTkButton(self, text="Close", command=self.destroy).grid(row=6, column=0, pady=20)

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 550) // 2
        y = (screen_height - 450) // 2
        self.geometry(f"550x450+{x}+{y}")


class SettingsWindow(ctk.CTkToplevel):
    """The settings window GUI, built with customtkinter."""

    def __init__(self, parent, settings_manager, caption_window, restart_callback):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("540x750")  # Adjusted height for scrollable area
        self.transient(parent)
        self.center_window()

        self.settings_manager = settings_manager
        self.caption_window = caption_window
        self.restart_callback = restart_callback
        self.settings = self.settings_manager.settings.copy()

        self.initial_language = self.settings['language']
        self.initial_block_size = self.settings['block_size']
        self.initial_appearance_mode = self.settings['appearance_mode']

        self.language_models = LANGUAGE_MODELS
        self.download_cancelled = False

        self.setup_ui()
        self.load_settings_to_ui()

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 540) // 2
        y = (screen_height - 750) // 2
        self.geometry(f"540x750+{x}+{y}")

    def setup_ui(self):
        # Configure grid for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Main Scrollable Frame ---
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        scroll_frame.grid_columnconfigure(1, weight=1)

        # --- General Settings Section ---
        general_frame = ctk.CTkFrame(scroll_frame)
        general_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        general_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(general_frame, text="General", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3,
                                                                                          pady=(5, 10))

        appearance_label = ctk.CTkLabel(general_frame, text="Appearance Mode:")
        appearance_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.appearance_mode_menu = ctk.CTkOptionMenu(general_frame, values=["dark", "light", "system"],
                                                      command=self.on_appearance_mode_change)
        self.appearance_mode_menu.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ToolTip(appearance_label, "Choose the visual theme for the application interface")
        ToolTip(self.appearance_mode_menu, "Choose the visual theme for the application interface")

        show_about_label = ctk.CTkLabel(general_frame, text="Show About on Startup:")
        show_about_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.show_about_checkbox = ctk.CTkCheckBox(general_frame, text="", command=self.update_setting)
        self.show_about_checkbox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        ToolTip(show_about_label, "Display the About window when the application starts")
        ToolTip(self.show_about_checkbox, "Display the About window when the application starts")

        # --- Appearance Section ---
        appearance_frame = ctk.CTkFrame(scroll_frame)
        appearance_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        appearance_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(appearance_frame, text="Caption Appearance", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0,
                                                                                                        columnspan=3,
                                                                                                        pady=(5, 10))

        subtitle_color_label = ctk.CTkLabel(appearance_frame, text="Subtitle Color:")
        subtitle_color_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.subtitle_color_btn = ctk.CTkButton(appearance_frame, text="", command=self.pick_subtitle_color,
                                                border_width=1, border_color=("gray70", "gray30"))
        self.subtitle_color_btn.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ToolTip(subtitle_color_label, "Color of the caption text")
        ToolTip(self.subtitle_color_btn, "Color of the caption text")

        bg_color_label = ctk.CTkLabel(appearance_frame, text="Background Color:")
        bg_color_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.bg_color_btn = ctk.CTkButton(appearance_frame, text="", command=self.pick_bg_color,
                                          border_width=1, border_color=("gray70", "gray30"))
        self.bg_color_btn.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ToolTip(bg_color_label, "Background color behind the caption text")
        ToolTip(self.bg_color_btn, "Background color behind the caption text")

        opacity_label_widget = ctk.CTkLabel(appearance_frame, text="Opacity:")
        opacity_label_widget.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.opacity_slider = ctk.CTkSlider(appearance_frame, from_=0.1, to=1.0, command=self.update_setting)
        self.opacity_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.opacity_label = ctk.CTkLabel(appearance_frame, text="", width=40)
        self.opacity_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        opacity_tooltip = "Transparency of the caption window (0.1 = very transparent, 1.0 = solid)"
        ToolTip(opacity_label_widget, opacity_tooltip)
        ToolTip(self.opacity_slider, opacity_tooltip)

        font_size_label_widget = ctk.CTkLabel(appearance_frame, text="Font Size:")
        font_size_label_widget.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.font_size_slider = ctk.CTkSlider(appearance_frame, from_=8, to=72, number_of_steps=64,
                                              command=self.update_setting)
        self.font_size_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.font_size_label = ctk.CTkLabel(appearance_frame, text="", width=40)
        self.font_size_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        font_size_tooltip = "Size of the caption text in pixels"
        ToolTip(font_size_label_widget, font_size_tooltip)
        ToolTip(self.font_size_slider, font_size_tooltip)

        font_label = ctk.CTkLabel(appearance_frame, text="Font:")
        font_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        system_fonts = sorted(list(tkfont.families()))
        self.font_menu = SearchableComboBox(appearance_frame, values=system_fonts, command=self.update_setting)
        self.font_menu.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        font_tooltip = "Font family for the caption text"
        ToolTip(font_label, font_tooltip)
        ToolTip(self.font_menu, font_tooltip)

        width_label_widget = ctk.CTkLabel(appearance_frame, text="Window Width:")
        width_label_widget.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.width_slider = ctk.CTkSlider(appearance_frame, from_=300, to=2000, command=self.update_setting)
        self.width_slider.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.width_label = ctk.CTkLabel(appearance_frame, text="", width=40)
        self.width_label.grid(row=6, column=2, padx=10, pady=5, sticky="w")
        width_tooltip = "Width of the caption window in pixels"
        ToolTip(width_label_widget, width_tooltip)
        ToolTip(self.width_slider, width_tooltip)

        height_label_widget = ctk.CTkLabel(appearance_frame, text="Window Height:")
        height_label_widget.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.height_slider = ctk.CTkSlider(appearance_frame, from_=50, to=800, command=self.update_setting)
        self.height_slider.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
        self.height_label = ctk.CTkLabel(appearance_frame, text="", width=40)
        self.height_label.grid(row=7, column=2, padx=10, pady=5, sticky="w")
        height_tooltip = "Height of the caption window in pixels"
        ToolTip(height_label_widget, height_tooltip)
        ToolTip(self.height_slider, height_tooltip)

        padding_label_widget = ctk.CTkLabel(appearance_frame, text="Horiz. Padding:")
        padding_label_widget.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.padding_slider = ctk.CTkSlider(appearance_frame, from_=0, to=100, command=self.update_setting)
        self.padding_slider.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
        self.padding_label = ctk.CTkLabel(appearance_frame, text="", width=40)
        self.padding_label.grid(row=8, column=2, padx=10, pady=5, sticky="w")
        padding_tooltip = "Horizontal spacing inside the caption window (affects text wrapping)"
        ToolTip(padding_label_widget, padding_tooltip)
        ToolTip(self.padding_slider, padding_tooltip)

        # --- Audio & Model Section ---
        audio_frame = ctk.CTkFrame(scroll_frame)
        audio_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        audio_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(audio_frame, text="Audio & Language", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0,
                                                                                                 columnspan=3,
                                                                                                 pady=(5, 10))

        language_label = ctk.CTkLabel(audio_frame, text="Language Model:")
        language_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.language_menu = SearchableComboBox(audio_frame, values=list(self.language_models.keys()),
                                                command=self.on_language_change)
        self.language_menu.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        language_tooltip = "Language for speech recognition (requires corresponding model download)"
        ToolTip(language_label, language_tooltip)
        ToolTip(self.language_menu, language_tooltip)

        self.model_status_label = ctk.CTkLabel(audio_frame, text="", text_color="gray")
        self.model_status_label.grid(row=2, column=0, columnspan=3, pady=5)

        self.download_progress = ctk.CTkProgressBar(audio_frame, orientation="horizontal", mode="determinate")
        self.download_progress.set(0)
        
        # Cancel download button (initially hidden)
        self.cancel_download_btn = ctk.CTkButton(audio_frame, text="Cancel", 
                                                command=self.cancel_download, fg_color="#c76b29",
                                                hover_color="#a15621", width=80)
        
        # Retry download button (initially hidden)
        self.retry_download_btn = ctk.CTkButton(audio_frame, text="Retry Download", 
                                               command=None, fg_color="#2980b9",
                                               hover_color="#1f5582", width=120)

        block_size_label_widget = ctk.CTkLabel(audio_frame, text="Block Size:")
        block_size_label_widget.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.block_size_slider = ctk.CTkSlider(audio_frame, from_=1000, to=8000, number_of_steps=70,
                                               command=self.update_setting)
        self.block_size_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.block_size_label = ctk.CTkLabel(audio_frame, text="", width=40)
        self.block_size_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        block_size_tooltip = ("Audio buffer size in samples. Lower values = faster response but may affect accuracy. "
                              "Higher values = better accuracy but slower response. 2000-4000 is usually optimal.")
        ToolTip(block_size_label_widget, block_size_tooltip)
        ToolTip(self.block_size_slider, block_size_tooltip)

        delay_label_widget = ctk.CTkLabel(audio_frame, text="Pause Delay (s):")
        delay_label_widget.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.delay_slider = ctk.CTkSlider(audio_frame, from_=0.5, to=5.0, number_of_steps=9,
                                          command=self.update_setting)
        self.delay_slider.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.delay_label = ctk.CTkLabel(audio_frame, text="", width=40)
        self.delay_label.grid(row=5, column=2, padx=10, pady=5, sticky="w")
        delay_tooltip = ("Time in seconds after audio stops before clearing captions. "
                         "Lower values clear faster, higher values keep text visible longer during pauses.")
        ToolTip(delay_label_widget, delay_tooltip)
        ToolTip(self.delay_slider, delay_tooltip)

        # --- Restart Prompt Section (Initially Hidden, outside scroll frame) ---
        self.restart_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.restart_frame.grid(row=1, column=0, pady=5, sticky="ew")
        ctk.CTkLabel(self.restart_frame, text="A restart is required for some changes to take effect.",
                     text_color="orange").pack(pady=5)
        ctk.CTkButton(self.restart_frame, text="Restart Now", command=self.restart_and_close, fg_color="#c76b29",
                      hover_color="#a15621").pack(pady=5)
        self.restart_frame.grid_remove()  # Hide it initially

        # --- Bottom Section (outside scroll frame) ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=(10, 20))
        self.about_button = ctk.CTkButton(button_frame, text="About", command=self.open_about_window)
        self.about_button.pack(side="left", padx=10)
        self.reset_button = ctk.CTkButton(button_frame, text="Reset Defaults", command=self.reset_defaults)
        self.reset_button.pack(side="left", padx=10)
        self.save_button = ctk.CTkButton(button_frame, text="Save & Close", command=self.save_and_close)
        self.save_button.pack(side="left", padx=10)

    def open_about_window(self):
        if not any(isinstance(x, AboutWindow) for x in self.winfo_children()):
            AboutWindow(self)

    def on_appearance_mode_change(self, mode):
        self.settings['appearance_mode'] = mode
        ctk.set_appearance_mode(mode)
        if mode != self.initial_appearance_mode:
            self.show_restart_prompt()
        self.update_setting()

    def _update_slider_labels(self):
        self.opacity_label.configure(text=f"{self.opacity_slider.get():.2f}")
        self.font_size_label.configure(text=f"{int(self.font_size_slider.get())}")
        self.width_label.configure(text=f"{int(self.width_slider.get())}")
        self.height_label.configure(text=f"{int(self.height_slider.get())}")
        self.padding_label.configure(text=f"{int(self.padding_slider.get())}")
        self.block_size_label.configure(text=f"{int(self.block_size_slider.get())}")
        self.delay_label.configure(text=f"{self.delay_slider.get():.1f}")

    def load_settings_to_ui(self):
        self.subtitle_color_btn.configure(fg_color=self.settings['subtitle_color'])
        self.bg_color_btn.configure(fg_color=self.settings['background_color'])
        self.opacity_slider.set(self.settings['background_opacity'])
        self.font_size_slider.set(self.settings['subtitle_size'])
        self.font_menu.set(self.settings['subtitle_font'])
        self.width_slider.set(self.settings['window_width'])
        self.height_slider.set(self.settings['window_height'])
        self.padding_slider.set(self.settings['window_padding'])
        self.language_menu.set(self.settings['language'])
        self.block_size_slider.set(self.settings['block_size'])
        self.delay_slider.set(self.settings['delay_threshold'])
        self.appearance_mode_menu.set(self.settings['appearance_mode'])

        if self.settings['show_about_on_startup']:
            self.show_about_checkbox.select()
        else:
            self.show_about_checkbox.deselect()

        self.check_model_status()
        self._update_slider_labels()

    def pick_subtitle_color(self):
        color_code = colorchooser.askcolor(title="Choose Subtitle Color")[1]
        if color_code:
            self.subtitle_color_btn.configure(fg_color=color_code)
            self.update_setting()

    def pick_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose Background Color")[1]
        if color_code:
            self.bg_color_btn.configure(fg_color=color_code)
            self.update_setting()

    def update_setting(self, value=None):
        self.settings['subtitle_color'] = self.subtitle_color_btn.cget("fg_color")
        self.settings['background_color'] = self.bg_color_btn.cget("fg_color")
        self.settings['background_opacity'] = self.opacity_slider.get()
        self.settings['subtitle_size'] = int(self.font_size_slider.get())
        self.settings['subtitle_font'] = self.font_menu.get()
        self.settings['window_width'] = int(self.width_slider.get())
        self.settings['window_height'] = int(self.height_slider.get())
        self.settings['window_padding'] = int(self.padding_slider.get())
        self.settings['language'] = self.language_menu.get()
        self.settings['block_size'] = int(self.block_size_slider.get())
        self.settings['delay_threshold'] = self.delay_slider.get()
        self.settings['model_path'] = self.language_models[self.language_menu.get()]
        self.settings['show_about_on_startup'] = bool(self.show_about_checkbox.get())
        self.settings['appearance_mode'] = self.appearance_mode_menu.get()

        self._update_slider_labels()
        self.caption_window.apply_settings(self.settings)

        if (self.settings['language'] != self.initial_language or
                self.settings['block_size'] != self.initial_block_size or
                self.settings['appearance_mode'] != self.initial_appearance_mode):
            self.show_restart_prompt()

    def on_language_change(self, language):
        self.check_model_status()
        self.update_setting()

    def show_restart_prompt(self):
        self.restart_frame.grid()

    def check_model_status(self):
        selected_lang = self.language_menu.get()
        model_path = self.language_models.get(selected_lang)
        if model_path and os.path.isdir(model_path):
            self.model_status_label.configure(text=f"Model '{model_path}' found.", text_color="green")
        else:
            self.model_status_label.configure(text=f"Model for {selected_lang} not found. Attempting to download...",
                                              text_color="orange")
            self.download_and_extract_model(model_path)

    def download_and_extract_model(self, model_name):
        if not model_name:
            self.model_status_label.configure(text="Invalid model name.", text_color="red")
            return
        # Hide retry button if it's visible
        self.retry_download_btn.grid_forget()
        download_thread = threading.Thread(target=self._download_worker, args=(model_name,), daemon=True)
        download_thread.start()
        
    def cancel_download(self):
        """Cancel the current download operation"""
        self.download_cancelled = True
        self.model_status_label.configure(text="Cancelling download...", text_color="orange")

    def _download_worker(self, model_name):
        self.language_menu.configure(state="disabled")
        self.save_button.configure(state="disabled")
        
        # Show progress bar and cancel button
        self.download_progress.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.cancel_download_btn.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
        zip_path = f"{model_name}.zip"
        self.download_cancelled = False
        start_time = time.time()
        download_error = False
        
        try:
            self.model_status_label.configure(text=f"Connecting to download server...", text_color="orange")
            self.download_progress.set(0)  # Initialize progress bar
            self.update_idletasks()
            
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                bytes_downloaded = 0
                last_time = time.time()
                last_bytes = 0
                
                # Format total size for display
                total_size_mb = total_size / (1024 * 1024) if total_size > 0 else 0
                
                # Initial status update with total size
                self.model_status_label.configure(text=f"Downloading {model_name}... 0.0 MB / {total_size_mb:.1f} MB (0.0%) - Initializing...", text_color="orange")
                self.update_idletasks()
                
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if self.download_cancelled:
                            break
                            
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        current_time = time.time()
                        
                        # Calculate progress
                        progress = bytes_downloaded / total_size if total_size > 0 else 0
                        self.download_progress.set(progress)
                        
                        # Calculate speed and ETA every 0.5 seconds
                        if current_time - last_time >= 0.5:
                            elapsed_time = current_time - last_time
                            bytes_this_interval = bytes_downloaded - last_bytes
                            speed_bps = bytes_this_interval / elapsed_time if elapsed_time > 0 else 0
                            speed_mb = speed_bps / (1024 * 1024)
                            
                            # Calculate ETA
                            if speed_bps > 0 and total_size > 0:
                                remaining_bytes = total_size - bytes_downloaded
                                eta_seconds = remaining_bytes / speed_bps
                                eta_minutes = int(eta_seconds // 60)
                                eta_seconds = int(eta_seconds % 60)
                                eta_str = f"{eta_minutes}m {eta_seconds}s" if eta_minutes > 0 else f"{eta_seconds}s"
                            else:
                                eta_str = "calculating..."
                            
                            # Format current size for display
                            current_size_mb = bytes_downloaded / (1024 * 1024)
                            
                            # Update status with detailed information
                            status_text = f"Downloading {model_name}... {current_size_mb:.1f} MB / {total_size_mb:.1f} MB ({progress*100:.1f}%) - {speed_mb:.1f} MB/s - ETA: {eta_str}"
                            self.model_status_label.configure(text=status_text, text_color="orange")
                            
                            last_time = current_time
                            last_bytes = bytes_downloaded
                            
                        self.update_idletasks()
                        
            if self.download_cancelled:
                self.model_status_label.configure(text=f"Download cancelled", text_color="red")
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                return
                
            self.model_status_label.configure(text=f"Extracting {model_name}...", text_color="orange")
            self.update_idletasks()
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            os.remove(zip_path)
            
            total_time = time.time() - start_time
            total_time_str = f"{int(total_time // 60)}m {int(total_time % 60)}s" if total_time >= 60 else f"{int(total_time)}s"
            self.model_status_label.configure(text=f"Model '{model_name}' installed successfully in {total_time_str}", text_color="green")
            self.show_restart_prompt()
            
        except Exception as e:
            download_error = True
            error_msg = f"Error downloading model: {str(e)}"
            if "404" in str(e):
                error_msg = f"Model '{model_name}' not found on server"
            elif "timeout" in str(e).lower():
                error_msg = f"Download timeout - please check your internet connection"
            elif "connection" in str(e).lower():
                error_msg = f"Connection error - please check your internet connection"
                
            self.model_status_label.configure(text=error_msg, text_color="red")
            if os.path.exists(zip_path):
                os.remove(zip_path)
                
        finally:
            self.download_progress.grid_forget()
            self.cancel_download_btn.grid_forget()
            self.language_menu.configure(state="normal")
            self.save_button.configure(state="normal")
            
            # Show retry button only if there was an error
            if download_error and not self.download_cancelled:
                self.retry_download_btn.configure(command=lambda: self.download_and_extract_model(model_name))
                self.retry_download_btn.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    def reset_defaults(self):
        if messagebox.askyesno("Reset Settings",
                               "Are you sure you want to reset all settings to their defaults? This requires a restart."):
            self.settings = self.settings_manager.default_settings.copy()
            self.settings["ran_before"] = True
            self.load_settings_to_ui()
            self.caption_window.apply_settings(self.settings)
            self.show_restart_prompt()

    def restart_and_close(self):
        self.settings_manager.save_settings(self.settings)
        self.restart_callback()

    def save_and_close(self):
        self.settings_manager.save_settings(self.settings)
        self.destroy()


class CaptionWindow:
    """The main GUI window for displaying the captions."""

    def __init__(self, root, settings_manager, restart_callback):
        self.root = root
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings
        self.restart_callback = restart_callback

        self.root.title("Live Captions")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.max_lines = 2
        self.caption_history = collections.deque(maxlen=self.max_lines * 2)
        self.current_partial_text = ""
        self.text_wrap_width = 70
        self.is_paused = False

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill='both')

        self.caption_label = tk.Label(self.main_frame, text="Listening for audio...", justify="center", anchor="center")
        self.caption_label.pack(expand=True, fill='both')

        self.caption_label.bind("<ButtonPress-1>", self.start_move)
        self.caption_label.bind("<ButtonRelease-1>", self.stop_move)
        self.caption_label.bind("<B1-Motion>", self.do_move)
        self.main_frame.bind("<ButtonPress-1>", self.start_move)
        self.main_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.main_frame.bind("<B1-Motion>", self.do_move)

        self.settings_menu = tk.Menu(root, tearoff=0)
        self.settings_menu.add_command(label="Settings", command=self.open_settings_window)
        self.settings_menu.add_command(label="About", command=self.open_about_window)
        self.settings_menu.add_command(label="Restart", command=self.restart_app)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Exit", command=self.quit_app)

        self.root.bind("<Button-3>", self.show_settings_menu)
        self.caption_label.bind("<Button-3>", self.show_settings_menu)
        self.main_frame.bind("<Button-3>", self.show_settings_menu)

        self.apply_settings(self.settings)
        self.update_caption()

    def apply_settings(self, settings):
        self.settings = settings
        self.root.config(bg=settings['background_color'])
        self.main_frame.config(bg=settings['background_color'])
        self.root.attributes("-alpha", settings['background_opacity'])
        new_font = (settings['subtitle_font'], settings['subtitle_size'], "bold")
        self.caption_label.config(font=new_font, fg=settings['subtitle_color'], bg=settings['background_color'])
        self.root.geometry(f"{settings['window_width']}x{settings['window_height']}")
        self.main_frame.pack_configure(padx=settings['window_padding'], pady=10)

        try:
            font_obj = tkfont.Font(family=settings['subtitle_font'], size=settings['subtitle_size'])
            line_height = font_obj.metrics('linespace')
            if line_height > 0:
                available_height = settings['window_height'] - 20
                self.max_lines = max(1, available_height // line_height)
                self.caption_history = collections.deque(maxlen=self.max_lines * 2)

            sample_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            avg_char_width = font_obj.measure(sample_text) / len(sample_text)

            if avg_char_width > 0:
                effective_width = settings['window_width'] - (2 * settings['window_padding']) - 10
                self.text_wrap_width = max(20, int(effective_width / avg_char_width))
            else:
                effective_width = settings['window_width'] - (2 * settings['window_padding'])
                estimated_char_width = settings['subtitle_size'] * 0.6
                self.text_wrap_width = max(20, int(effective_width / estimated_char_width))

        except tk.TclError:
            effective_width = settings['window_width'] - (2 * settings['window_padding'])
            estimated_char_width = settings['subtitle_size'] * 0.6
            self.text_wrap_width = max(20, int(effective_width / estimated_char_width))
            self.max_lines = 2

    def open_settings_window(self):
        if not any(isinstance(x, SettingsWindow) for x in self.root.winfo_children()):
            SettingsWindow(self.root, self.settings_manager, self, self.restart_callback)

    def open_about_window(self):
        if not any(isinstance(x, AboutWindow) for x in self.root.winfo_children()):
            AboutWindow(self.root)

    def show_settings_menu(self, event):
        try:
            self.settings_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.settings_menu.grab_release()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_caption(self):
        global last_caption_time
        new_content_available = not caption_queue.empty()
        if new_content_available: self.is_paused = False
        try:
            while not caption_queue.empty():
                new_text = caption_queue.get_nowait()
                if new_text.startswith("..."):
                    self.current_partial_text = new_text[4:]
                else:
                    self.caption_history.append(new_text)
                    self.current_partial_text = ""
        except queue.Empty:
            pass
        if not new_content_available and (time.time() - last_caption_time) > self.settings[
            'delay_threshold'] and not self.is_paused:
            self.caption_history.clear()
            self.current_partial_text = ""
            self.is_paused = True

        full_text = " ".join(filter(None, self.caption_history))
        if self.current_partial_text:
            if full_text: full_text += " "
            full_text += self.current_partial_text

        wrapped_lines = textwrap.wrap(full_text, width=self.text_wrap_width, break_long_words=True,
                                      break_on_hyphens=False)
        display_lines = wrapped_lines[-self.max_lines:] if len(wrapped_lines) > self.max_lines else wrapped_lines
        display_text = "\n".join(display_lines)

        if not display_text.strip():
            display_text = "Listening for audio... (Right-click for settings)"

        self.caption_label.config(text=display_text)
        self.root.after(100, self.update_caption)

    def restart_app(self):
        self.restart_callback()

    def quit_app(self):
        stop_threads.set()
        self.root.destroy()


# --- Background Threads ---

def audio_capture_thread(block_size, sample_rate):
    """Captures audio from the default speaker and puts it into a queue."""
    try:
        default_speaker = sc.default_speaker()
        print(f"Using speaker: {default_speaker.name} for audio capture.")
        with sc.get_microphone(id=str(default_speaker.id), include_loopback=True).recorder(
                samplerate=sample_rate, channels=1, blocksize=int(block_size)
        ) as mic:
            print("Audio recorder started.")
            while not stop_threads.is_set():
                data = mic.record(numframes=int(block_size))
                data_int16 = (data * 32767).astype(np.int16)
                audio_queue.put(data_int16.tobytes())
    except Exception as e:
        print(f"Error in audio capture: {e}", file=sys.stderr)
        caption_queue.put("ERROR: Could not capture audio. Check audio devices.")


def speech_recognition_thread(model_path, sample_rate):
    """Processes audio from the queue using Vosk."""
    global last_caption_time
    try:
        if not os.path.isdir(model_path):
            raise FileNotFoundError(f"Model path '{model_path}' not found. Please select a valid model in settings.")
        model = vosk.Model(model_path)
        recognizer = vosk.KaldiRecognizer(model, sample_rate)
        recognizer.SetWords(True)
        print("Vosk model loaded. Speech recognition thread started.")
    except Exception as e:
        print(f"Error loading Vosk model: {e}", file=sys.stderr)
        caption_queue.put(f"ERROR: Failed to load model. Please check settings.")
        return

    while not stop_threads.is_set():
        try:
            audio_data = audio_queue.get(timeout=1)
            if recognizer.AcceptWaveform(audio_data):
                result_dict = json.loads(recognizer.Result())
                text = result_dict.get('text', '')
                if text:
                    caption_queue.put(text)
                    last_caption_time = time.time()
            else:
                partial_result_dict = json.loads(recognizer.PartialResult())
                partial_text = partial_result_dict.get('partial', '')
                if partial_text:
                    caption_queue.put(f"... {partial_text}")
                    last_caption_time = time.time()
        except queue.Empty:
            continue


def main():
    """Main function to set up the GUI and start the threads."""
    settings_manager = SettingsManager()
    settings = settings_manager.settings
    is_first_run = settings_manager.is_first_run

    ctk.set_appearance_mode(settings.get('appearance_mode', 'dark'))

    temp_root = ctk.CTk()
    temp_root.withdraw()

    if not os.path.isdir(settings['model_path']):
        messagebox.showerror("Model Not Found",
                             f"The model '{settings['model_path']}' was not found. Please open settings to download it or configure the correct path.")

    temp_root.destroy()

    root = tk.Tk()

    def restart_application():
        print("Restarting application...")
        stop_threads.set()
        time.sleep(0.5)
        root.destroy()

        try:
            if getattr(sys, 'frozen', False):
                subprocess.Popen([sys.executable])
            else:
                subprocess.Popen([sys.executable] + sys.argv)
        except Exception as e:
            print(f"Subprocess restart failed: {e}")
            try:
                os.execv(sys.executable, [sys.executable] + sys.argv)
            except Exception as e2:
                print(f"os.execv restart failed: {e2}")
                messagebox.showerror("Restart Failed",
                                     "Failed to restart the application automatically. Please restart it manually.")

    stop_threads.clear()
    SAMPLE_RATE = 16000

    audio_thread = threading.Thread(target=audio_capture_thread, args=(settings['block_size'], SAMPLE_RATE),
                                    daemon=True)
    audio_thread.start()

    recognizer_thread = threading.Thread(target=speech_recognition_thread, args=(settings['model_path'], SAMPLE_RATE),
                                         daemon=True)
    recognizer_thread.start()

    app = CaptionWindow(root, settings_manager, restart_application)

    if is_first_run or settings.get('show_about_on_startup', True):
        app.open_about_window()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coord = (screen_width / 2) - (settings['window_width'] / 2)
    y_coord = screen_height - (settings['window_height'] + 50)
    root.geometry(f"+{int(x_coord)}+{int(y_coord)}")

    root.mainloop()

    stop_threads.set()


if __name__ == "__main__":
    main()