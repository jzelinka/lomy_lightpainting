import os
from flask import render_template

class SimpleInterface():
    def __init__(self, template) -> None:
        self.colors = []
        self.orientation = None
        self.templatePath = template
        self.grad = False
        self.discrete = True

        # numpy array for storing the image
        self.image_exists = False
        self.image = None 

    def render(self):
        # TODO fill in the things i want to display
        # template = open(self.templatePath).read()
        # if i have more than one color create the image to some static file

        return render_template("simple.html", colors=list(enumerate(self.colors)), image_exists=self.image_exists, grad=self.grad, discrete=self.discrete)

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