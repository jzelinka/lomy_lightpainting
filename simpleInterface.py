import os

class SimpleInterface():
    def __init__(self, template) -> None:
        self.colors = []
        self.orientation = None
        self.templatePath = template

        # numpy array for storing the image
        self.image = None 
        pass

    def render(self):
        # TODO fill in the things i want to display
        template = open(self.templatePath).read()
        return template

    def add_to_pictures(self):
        pass

    def add_color(self, color):
        print("Simple interface: adding color")
        self.colors.append(color)
        print(self.colors)

    def switch_orientation(sefl, orientation):
        pass

    def remove_color(self, color):
        pass

    def display_image(self):
        # TODO ask the neopixel wrapper to show the image
        print("Displaying the image onto the light bar.")
        pass

    def update_preview(self):
        pass