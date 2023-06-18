import time
# import neopixel
from PIL import Image
import numpy as np

class NeoPixelWrapper:
    def __init__(self,pin, timeOn, timeOff):
        self.num_pixels = 80

        # auto_write=False means that the pixels won't change colors until you call pixels.show()
        # self.pixels = neopixel.NeoPixel(pin, self.num_pixels, pixel_order=neopixel.RGB,auto_write=False)
        
        ## image data
        self.image = None
        self.imageWidth = None
        self.imageHeight = None

        self.lineIndex = 0
        self.lastPrintTime = 0

        ## milliseconds expected
        self.lightOnTime = timeOn  # time length for how long do the LEDs stay on
        self.lightOffTime = timeOff  # time break between turning on the next vertical line

    def load_image(self, image_path):
        # Open the image
        originalImage = Image.open(image_path)

        # get the image ratio
        image_ratio = originalImage.width / originalImage.height

        self.new_height = self.num_pixels ## height corresponds to the number of pixels
        self.new_width = int(self.new_height * image_ratio) ## width is calculated based on the ratio
        
        # resize and convert the image into a RGB matrix
        self.image = originalImage.resize((self.new_width, self.new_height)).convert("RGB")

        self.lineIndex = 0
        self.lastPrintTime = 0

    def print_next_line(self):
        if self.lineIndex >= self.imageWidth:
            return False  # Image is fully printed

        current_time = time.time()
        if current_time - self.lastPrintTime < self.lightOnTime:
            return True  # Delay not reached, wait for the next iteration

        # Iterate through each pixel in the current line and set the corresponding Neopixel color
        for y in range(self.imageHeight):
            x = self.lineIndex
            r, g, b = self.image.getpixel((x, y))
            pixel_index = y  # Assuming a vertical line representation
            self.pixels[pixel_index] = (r, g, b)

        # Update the Neopixels to display the current line
        self.pixels.show()

        self.lineIndex += 1
        self.lastPrintTime = current_time
        return True  # Image printing is in progress
