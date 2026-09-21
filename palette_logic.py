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

    if len(pixels) > sample_size:
        idx = np.random.choice(len(pixels), sample_size, replace=False)
        pixels = pixels[idx]

    rng = np.random.default_rng(42)
    centers = pixels[rng.choice(len(pixels), k, replace=False)]

    for _ in range(max_iterations):
        distances = np.linalg.norm(pixels[:, None, :] - centers[None, :, :], axis=2)
        assignments = np.argmin(distances, axis=1)

        new_centers = []
        for i in range(k):
            members = pixels[assignments == i]
            new_centers.append(members.mean(axis=0) if len(members) else centers[i])
        centers = np.array(new_centers)