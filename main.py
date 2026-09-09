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