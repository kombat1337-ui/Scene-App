import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import time
import pygame
import os

FONT_PATH = "digital-7.ttf"  # Ensure this file is in the same folder

class AnimatedGIF(tk.Label):
    def __init__(self, parent, gif_path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.gif = Image.open(gif_path)
        self.frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(self.gif)]
        self.idx = 0
        self.animate()

    def animate(self):
        self.config(image=self.frames[self.idx])
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(100, self.animate)

class ClockDisplay(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.custom_font = (self.load_font(), 80)
        self.configure(font=self.custom_font, fg="lime", bg="black")
        self.update_time()

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.config(text=current_time)
        self.after(1000, self.update_time)

    def load_font(self):
        try:
            from tkinter import font as tkfont
            tkfont.Font(family="Digital-7")
            return "Digital-7"
        except:
            return "Consolas"

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Mode Selector")
        self.root.geometry("800x600")
        self.root.configure(bg='black')

        pygame.mixer.init()
        self.current_music = None

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        title = tk.Label(frame, text="Select a visual mode", font=("Arial", 24), fg="white", bg="black")
        title.pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", foreground="white", background="#222", font=("Arial", 14), padding=10)
        style.map("TButton", background=[("active", "#444")])

        ttk.Button(frame, text="🔥 Fireplace", command=self.show_fire).pack(pady=10)
        ttk.Button(frame, text="🌧️ Rain", command=self.show_rain).pack(pady=10)
        ttk.Button(frame, text="🕒 Clock", command=self.show_clock).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def play_music(self, music_file):
        pygame.mixer.music.stop()
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    def add_volume_slider(self):
        slider_frame = ttk.Frame(self.root)
        slider_frame.pack(pady=10)

        label = tk.Label(slider_frame, text="Volume", font=("Arial", 12), fg="white", bg="black")
        label.pack(side="left")

        slider = ttk.Scale(slider_frame, from_=0, to=1, orient="horizontal", command=self.set_volume)
        slider.set(0.5)
        slider.pack(side="left", padx=10)

    def add_back_button(self):
        back_btn = ttk.Button(self.root, text="← Back", command=self.show_main_menu)
        back_btn.pack(pady=10)

    def show_fire(self):
        self.clear_window()
        AnimatedGIF(self.root, "fire.gif").pack(expand=True)
        self.play_music("fire.mp3")
        self.add_volume_slider()
        self.add_back_button()

    def show_rain(self):
        self.clear_window()
        AnimatedGIF(self.root, "rain.gif").pack(expand=True)
        self.play_music("rain.mp3")
        self.add_volume_slider()
        self.add_back_button()

    def show_clock(self):
        self.clear_window()
        ClockDisplay(self.root, bg="black").pack(expand=True)
        self.play_music("clock.mp3")
        self.add_volume_slider()
        self.add_back_button()

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()
