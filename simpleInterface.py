import os
from flask import render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class simple_interface():
    def __init__(self, template, height, static_dir) -> None:
        self.colors = []
        self.orientation = 0
        self.templatePath = template
        self.grad = False
        self.discrete = True
        self.height = height
        self.width = 400
        self.static_dir = static_dir

        # numpy array for storing the image
        self.image_exists = False
        self.image = None 
    
    def render(self):
        # template = open(self.templatePath).read()
        # if i have more than one color create the image to some static file
        if len(self.colors) > 0:
            self.image_exists = True
            self.image = self.create_img_buffer()
        else:
            self.image_exists = False
            self.image = None

        return render_template("simple.html",
                               colors=list(enumerate(self.colors)),
                               image_exists=self.image_exists,
                               grad=self.grad,
                               discrete=self.discrete,
                               image=self.image,
                               width=self.width
                               )
    
    def colors_to_rgb(self):
        rgb_colors = []
        for hex_code in self.colors:
            hex_code = hex_code.lstrip('#')
            rgb_colors.append(tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)))
        return rgb_colors
    
    def create_np_representation(self):
        rgb_colors = self.colors_to_rgb()
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # TODO add gradient

        for i, rgb_color in enumerate(rgb_colors):
            if self.orientation == 0:
                column_size = self.height // len(rgb_colors)
                img[i * column_size : (i + 1) * column_size, :] = rgb_color
            elif self.orientation == 1:
                column_size = self.width // len(rgb_colors)
                img[:, i * column_size : (i + 1) * column_size] = rgb_color
            elif self.orientation == 2:
                column_size = self.height // len(rgb_colors)
                img[(len(rgb_colors) - i - 1) * column_size : (len(rgb_colors) - i) * column_size, :] = rgb_color
            elif self.orientation == 3:
                column_size = self.width // len(rgb_colors)
                img[:, (len(rgb_colors) - i - 1) * column_size : (len(rgb_colors) - i) * column_size] = rgb_color
        return img


    def create_img_buffer(self):
        img = self.create_np_representation()

        # Save image to a buffer
        buffer = io.BytesIO()
        plt.imsave(buffer, img, format='png')
        buffer.seek(0)

        # Encode image buffer to base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return image_base64
        
    def add_color(self, color):
        print("Simple interface: adding color")
        self.colors.append(color)
        print(self.colors)

    def rotate90(self):
        self.orientation = (self.orientation + 1) % 4

    def remove_color(self, color_idx):
        self.colors.pop(int(color_idx))

    def flip_grad_discrete(self):
        self.grad = not self.grad
        self.discrete = not self.discrete

    def add_to_pictures(self):
        print("Saving the image to the static folder")
        img = self.create_np_representation()
        img_name = "from_color_mixer"
        count = 0
        while os.path.isfile(os.path.join(self.static_dir, img_name + "_" + str(count) + ".png")):
            count += 1

        plt.imsave(os.path.join(self.static_dir, img_name + "_" + str(count) + ".png"), img)
    
    def set_width(self, width):
        self.width = int(width)