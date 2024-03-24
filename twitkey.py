from pynput import keyboard
import pygame
import pystray
from PIL import Image
import os
import tkinter as tk
from tkinter import ttk

SOUND_FOLDER = os.path.dirname(os.path.abspath(__file__))  
ICON_FILE = 'twitter.ico'  
MAX_DURATION = 2  # Maximum duration of sound files in seconds

# Initialize Pygame mixer
pygame.mixer.init()

# Load the sound files from the folder
sound_files = [file for file in os.listdir(SOUND_FOLDER) if file.endswith(('.wav', '.mp3', '.ogg'))]
sounds = {}
for sound_file in sound_files:
    sound = pygame.mixer.Sound(os.path.join(SOUND_FOLDER, sound_file))
    if sound.get_length() <= MAX_DURATION:
        sounds[sound_file] = sound

# Set the initial sound effect
current_sound = list(sounds.values())[0] if sounds else None

def on_press(key):
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        # Stop the currently playing sound effect
        if current_sound:
            current_sound.stop()
        # Play the current sound effect asynchronously
        if current_sound:
            current_sound.play()

def quit_program(icon, item):
    icon.stop()

def select_sound(sound_file):
    global current_sound
    current_sound = sounds[sound_file]

def open_sound_selection():
    sound_window = tk.Tk()
    sound_window.title("Select Sound")

    # Set the initial window size and center it on the screen
    window_width = 300
    window_height = 200
    screen_width = sound_window.winfo_screenwidth()
    screen_height = sound_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    sound_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Bring the tkinter window to the front and keep it on top
    sound_window.lift()
    sound_window.attributes('-topmost', True)

    selected_sound = tk.StringVar(sound_window)
    selected_sound.set(list(sounds.keys())[0])  # Set the default selected sound

    # Create a frame for the dropdown menu, preview button, and select button with margins
    frame = ttk.Frame(sound_window, padding=20)
    frame.pack(expand=True)

    sound_dropdown = ttk.Combobox(frame, textvariable=selected_sound, values=list(sounds.keys()), state="readonly")
    sound_dropdown.pack(fill=tk.X, padx=10, pady=(0, 10))

    def on_preview():
        sound = sounds[selected_sound.get()]
        sound.stop()  # Stop any currently playing sound
        sound.play()  # Play the selected sound

    preview_button = ttk.Button(frame, text="Preview", command=on_preview)
    preview_button.pack(fill=tk.X, padx=10, pady=(0, 10))

    def on_select():
        select_sound(selected_sound.get())
        sound_window.destroy()

    select_button = ttk.Button(frame, text="Select", command=on_select)
    select_button.pack(fill=tk.X, padx=10)

    # Force focus on the tkinter window after a brief delay
    sound_window.after(0, sound_window.focus_force)

    sound_window.mainloop()

def setup(icon):
    icon.visible = True
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

if __name__ == '__main__':
    image = Image.open(ICON_FILE)
    menu = pystray.Menu(
        pystray.MenuItem("Select Sound", lambda icon, item: open_sound_selection()),
        pystray.MenuItem("Quit", quit_program)
    )
    icon = pystray.Icon("AutoShift Sound", image, "AutoShift Sound", menu)
    icon.run(setup)