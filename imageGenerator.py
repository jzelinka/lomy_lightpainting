import numpy as np
from PIL import Image


def flat_color(color, num_pixels):
    data = np.zeros((num_pixels, num_pixels, 3), dtype=np.uint8)
    data[:, :] = color
    return data

def gradient(color1, color2, num_pixels):
    difference = np.array(color2) - np.array(color1)
    data = np.zeros((num_pixels, num_pixels, 3), dtype=np.uint8)
    for i in range(num_pixels):
        data[:, i] = color1 + difference * i / num_pixels
    return data

def rainbow(num_pixels):
    data = np.zeros((num_pixels, num_pixels, 3), dtype=np.uint8)
    for i in range(num_pixels):
        data[:, i] = 255 * np.sin(2 * np.pi * i / num_pixels + 2 * np.pi / 3) ** 2
    return data

if __name__ == "__main__":
    image = Image.fromarray(rainbow(216), 'RGB')
    image.save('rainbow.png')
    image.show()
    