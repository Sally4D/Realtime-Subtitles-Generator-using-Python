import tkinter as tk
import soundcard as sc
import vosk
import queue
import threading
import json
import sys
import numpy as np
import collections
import textwrap
import time  # Import the time module

# --- Configuration ---
MODEL_PATH = "vosk-model-small-en-us-0.15"  # CHANGE THIS TO YOUR MODEL'S PATH
SAMPLE_RATE = 16000
BLOCK_SIZE = 2000
DELAY_THRESHOLD = 1.0  # Time in seconds to wait before starting a new line

# --- Global Queues ---
audio_queue = queue.Queue()
caption_queue = queue.Queue()

# --- Global State for tracking time ---
# This variable tracks the timestamp of the last text received, whether full or partial.
# This is crucial for detecting a pause in the speech stream.
last_caption_time = time.time()


def audio_capture_thread():
    """
    Captures audio from the default speaker output and puts it into a queue.
    This function runs in a separate thread.
    """
    try:
        default_speaker = sc.default_speaker()
        print(f"Using speaker: {default_speaker.name} for audio capture.")

        with sc.get_microphone(id=str(default_speaker.id), include_loopback=True).recorder(samplerate=SAMPLE_RATE,
                                                                                           channels=1,
                                                                                           blocksize=BLOCK_SIZE) as mic:
            print("Audio recorder started.")
            while True:
                data = mic.record(numframes=BLOCK_SIZE)
                data_int16 = (data * 32767).astype(np.int16)
                audio_queue.put(data_int16.tobytes())

    except Exception as e:
        print(f"Error in audio capture: {e}", file=sys.stderr)
        if "exclusive mode" in str(e).lower():
            caption_queue.put("ERROR: Another app is using the audio device in exclusive mode.")
        else:
            caption_queue.put("ERROR: Could not capture audio. Check audio devices.")


def speech_recognition_thread():
    """
    Processes audio from the queue using Vosk and puts the recognized text
    into another queue. This function runs in a separate thread.
    """
    global last_caption_time
    try:
        model = vosk.Model(MODEL_PATH)
        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        recognizer.SetWords(True)
        print("Vosk model loaded. Speech recognition thread started.")
    except Exception as e:
        print(f"Error loading Vosk model from '{MODEL_PATH}': {e}", file=sys.stderr)
        caption_queue.put(f"ERROR: Failed to load model from '{MODEL_PATH}'. Please check the path.")
        return

    while True:
        audio_data = audio_queue.get()

        if recognizer.AcceptWaveform(audio_data):
            result_json = recognizer.Result()
            result_dict = json.loads(result_json)
            text = result_dict.get('text', '')
            if text:
                caption_queue.put(text)
                # Update the timestamp when a full, complete caption is received
                last_caption_time = time.time()
        else:
            partial_result_dict = json.loads(recognizer.PartialResult())
            partial_text = partial_result_dict.get('partial', '')
            if partial_text:
                caption_queue.put(f"... {partial_text}")
                # Update the timestamp for partial results as well
                last_caption_time = time.time()


class CaptionWindow:
    """
    The GUI window for displaying the captions.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Live Captions")

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.75)
        self.root.config(bg='black')

        # Use a deque to store the last two full captions
        self.caption_history = collections.deque(maxlen=2)
        self.current_partial_text = ""
        # Define a width for manual text wrapping
        self.text_wrap_width = 70

        # New flag to track if a pause has already been handled
        self.is_paused = False

        self.caption_label = tk.Label(
            root,
            text="Listening for audio...",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="black",
            justify="left"
        )
        self.caption_label.pack(padx=20, pady=20)

        self.caption_label.bind("<ButtonPress-1>", self.start_move)
        self.caption_label.bind("<ButtonRelease-1>", self.stop_move)
        self.caption_label.bind("<B1-Motion>", self.do_move)

        self.update_caption()

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
        """
        Periodically checks the caption queue for new text and updates the label.
        Now uses a delay threshold to create new lines for partial results.
        """
        global last_caption_time

        # Check if there is new content in the queue.
        new_content_available = not caption_queue.empty()

        # If there is new content, it means speech is happening.
        if new_content_available:
            self.is_paused = False

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

        # New logic to handle pauses.
        # If there's no new content, and the pause has exceeded the threshold,
        # and we haven't already marked the pause, then force a new line.
        if not new_content_available and (time.time() - last_caption_time) > DELAY_THRESHOLD and not self.is_paused:
            self.caption_history.clear()
            self.current_partial_text = ""
            self.is_paused = True

        # Combine history and partial text into a single string.
        # Use filter(None, ...) to handle the empty strings we added for new lines.
        full_text = " ".join(filter(None, self.caption_history))
        if self.current_partial_text:
            if full_text:
                full_text += " "
            full_text += self.current_partial_text

        # Manually wrap the entire text to the defined width
        wrapped_lines = textwrap.wrap(full_text, width=self.text_wrap_width)

        # Take only the last two lines
        display_lines = wrapped_lines[-2:] if len(wrapped_lines) > 2 else wrapped_lines
        display_text = "\n".join(display_lines)

        if not display_text:
            display_text = "Listening for audio..."

        self.caption_label.config(text=display_text)

        self.root.after(100, self.update_caption)


def main():
    """
    Main function to set up the GUI and start the threads.
    """
    audio_thread = threading.Thread(target=audio_capture_thread, daemon=True)
    audio_thread.start()

    recognizer_thread = threading.Thread(target=speech_recognition_thread, daemon=True)
    recognizer_thread.start()

    root = tk.Tk()
    app = CaptionWindow(root)

    window_width = 750
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coord = (screen_width / 2) - (window_width / 2)
    y_coord = (screen_height) - (window_height + 50)
    root.geometry(f"{window_width}x{window_height}+{int(x_coord)}+{int(y_coord)}")

    root.mainloop()


if __name__ == "__main__":
    main()
