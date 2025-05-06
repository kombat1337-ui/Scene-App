
import tkinter as tk
from tkinter import font as tkfont
import os
import ctypes
import time
from PIL import Image, ImageTk, ImageSequence
import pygame

FONT_PATH = "digital-7.ttf"
ASSETS_DIR = "assets"

SCENES = {
    "Fire": {"gif": "fire.gif", "sound": "fire.mp3"},
    "Rain": {"gif": "rain.gif", "sound": "rain.mp3"},
    "Clock": {"gif": None, "sound": "clock.mp3"},
}

pygame.mixer.init()

def register_custom_font(font_path):
    if os.path.exists(font_path):
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(font_path)

def get_digital_font(size=80):
    register_custom_font(FONT_PATH)
    fonts = tkfont.families()
    if "Digital-7" in fonts:
        return tkfont.Font(family="Digital-7", size=size)
    return tkfont.Font(family="Consolas", size=size)

class SceneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Choose Your Scene")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.label = None
        self.image_label = None
        self.clock_label = None
        self.frames = []
        self.current_frame = 0
        self.animating = False

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root, bg="black")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Choose a Scene", font=("Helvetica", 24), fg="white", bg="black").pack()

        button_frame = tk.Frame(top_frame, bg="black")
        button_frame.pack(pady=10)

        for scene in SCENES:
            btn = tk.Button(button_frame, text=scene, font=("Helvetica", 16), width=10, command=lambda s=scene: self.load_scene(s))
            btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(top_frame, text="Exit", command=self.root.quit, bg="red", fg="white", font=("Helvetica", 14))
        exit_btn.pack(pady=5)

        self.image_label = tk.Label(self.root, bg="black")
        self.image_label.pack(expand=True, fill="both")

    def load_scene(self, scene_name):
        self.stop_sound()
        self.clear_scene()

        data = SCENES[scene_name]
        gif_path = os.path.join(ASSETS_DIR, data["gif"]) if data["gif"] else None
        sound_path = os.path.join(ASSETS_DIR, data["sound"]) if data["sound"] else None

        if gif_path and os.path.exists(gif_path):
            self.load_gif(gif_path)
        elif scene_name == "Clock":
            self.show_clock()

        if sound_path and os.path.exists(sound_path):
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(-1)

    def stop_sound(self):
        pygame.mixer.music.stop()

    def clear_scene(self):
        self.animating = False
        if self.clock_label:
            self.clock_label.destroy()
            self.clock_label = None
        if self.image_label:
            self.image_label.config(image='')

    def load_gif(self, path):
        gif = Image.open(path)
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.ANTIALIAS).convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
        self.current_frame = 0
        self.animating = True
        self.animate_gif()

    def animate_gif(self):
        if not self.animating or not self.frames:
            return
        self.image_label.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(100, self.animate_gif)

    def show_clock(self):
        font = get_digital_font(160)
        self.clock_label = tk.Label(self.root, text="", font=font, fg="white", bg="black")
        self.clock_label.pack(expand=True)
        self.update_clock()

    def update_clock(self):
        if not self.clock_label:
            return
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = SceneApp(root)
    root.mainloop()
