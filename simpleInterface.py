import os
from flask import render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class simple_interface():
    def __init__(self, template, pixel_height) -> None:
        self.colors = []
        self.orientation = None
        self.templatePath = template
        self.grad = False
        self.discrete = True
        self.pixel_height = pixel_height

        # numpy array for storing the image
        self.image_exists = False
        self.image = None 
    
    def render(self):
        # template = open(self.templatePath).read()
        # if i have more than one color create the image to some static file
        if len(self.colors) > 0:
            self.image_exists = True
            # TODO create the image
            self.image = self.create_image()
        else:
            self.image_exists = False
            self.image = None

        return render_template("simple.html",
                               colors=list(enumerate(self.colors)),
                               image_exists=self.image_exists,
                               grad=self.grad,
                               discrete=self.discrete,
                               image=self.image
                               )
    
    def colors_to_rgb(self):
        rgb_colors = []
        for hex_code in self.colors:
            hex_code = hex_code.lstrip('#')
            rgb_colors.append(tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)))
        return rgb_colors

    def create_image(self):
        rgb_colors = self.colors_to_rgb()
        img = np.zeros((self.pixel_height, self.pixel_height, 3), dtype=np.uint8)
        # TODO improve to show all colors
        for rgb_color in rgb_colors:
            img[:, :] = rgb_color


        # Save image to a buffer
        buffer = io.BytesIO()
        plt.imsave(buffer, img, format='png')
        buffer.seek(0)

        # Encode image buffer to base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return image_base64
        

    def add_to_pictures(self):
        pass

    def add_color(self, color):
        print("Simple interface: adding color")
        self.colors.append(color)
        print(self.colors)

    def rotate90(self):
        # TODO prepare the numpy array so that it is rotated
        pass

    def remove_color(self, color_idx):
        self.colors.pop(int(color_idx))

    def flip_grad_discrete(self):
        self.grad = not self.grad
        self.discrete = not self.discrete

    def display_image(self):
        # TODO ask the neopixel wrapper to show the image
        print("Displaying the image onto the light bar.")
        pass

    def update_preview(self):
        pass