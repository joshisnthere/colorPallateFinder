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

        self.status_var = ctk.StringVar(value="Open an image to begin.")
        ctk.CTkLabel(self, textvariable=self.status_var, text_color="#8a8a8a").pack(anchor="w", padx=24)

    def _open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if not path:
            return

        try:
            count = max(2, min(12, int(self.count_var.get())))
        except ValueError:
            count = 6

        image = Image.open(path).convert("RGB")
        preview = image.copy()
        preview.thumbnail((640, 360))
        photo = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo

        self.status_var.set("Extracting palette...")
        self.update_idletasks()

        colors = logic.extract_palette(image, count)
        self._render_palette(colors)
        self.status_var.set(f"{os.path.basename(path)} -- {count} dominant colors")

    def _render_palette(self, colors):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()

        for r, g, b in colors:
            hex_code = f"#{r:02x}{g:02x}{b:02x}"
            swatch = ctk.CTkFrame(self.palette_frame, fg_color=hex_code, corner_radius=10, width=90, height=90)
            swatch.pack(side="left", padx=6)
            swatch.pack_propagate(False)
            label = ctk.CTkLabel(swatch, text=hex_code.upper(), text_color=self._label_color(r, g, b))
            label.pack(expand=True)
            label.bind("<Button-1>", lambda e, h=hex_code: self._copy(h))
            swatch.bind("<Button-1>", lambda e, h=hex_code: self._copy(h))