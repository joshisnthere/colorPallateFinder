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

        top = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12)
        top.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(top, text="Open Image", fg_color="#2a2a30",
                      command=self._open_image).pack(side="left", padx=16, pady=14)
        ctk.CTkLabel(top, text="Colors:", text_color=ACCENT).pack(side="left", padx=(20, 6))
        self.count_var = ctk.StringVar(value="6")
        ctk.CTkEntry(top, textvariable=self.count_var, width=50).pack(side="left")

        self.preview_label = ctk.CTkLabel(self, text="", fg_color=PANEL, corner_radius=12)
        self.preview_label.pack(padx=20, pady=(0, 10))

        self.palette_frame = ctk.CTkFrame(self, fg_color=BG)
        self.palette_frame.pack(fill="x", padx=20, pady=(0, 20))