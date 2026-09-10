"""
Color Palette Extractor

Open any image and pull out its dominant colors as a palette of swatches
with hex codes you can click to copy. Uses a small hand-rolled k-means so
the only dependencies are Pillow and numpy -- no heavier vision libraries
needed.
"""

import os

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

import palette_logic as logic

ctk.set_appearance_mode("dark")

BG = "#0d0d10"
PANEL = "#19191d"
ACCENT = "#c792ea"


class PaletteExtractorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Color Palette Extractor")
        self.geometry("720x560")
        self.configure(fg_color=BG)