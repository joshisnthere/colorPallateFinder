"""
A small from-scratch k-means over image pixels, sorted by cluster size so
the first swatch is genuinely the most dominant color, not an arbitrary
cluster order.
"""

import numpy as np


def extract_palette(image, k, max_iterations=15, sample_size=8000):
    image = image.copy()
    image.thumbnail((150, 150))
    pixels = np.array(image).reshape(-1, 3).astype(float)