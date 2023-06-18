import time
import adafruit_dotstar as dotstar
from PIL import Image

class DotStarWrapper:
    def __init__(self, delay):
        self.num_pixels = 216 # Number of pixels in the DotStar strip
        self.pin_sck = 11
        self.pin_mosi = 10

        # auto_write=False means that the pixels won't change colors until you call pixels.show()
        self.pixels = dotstar.DotStar(self.pin_sck, self.pin_mosi, self.num_pixels, brightness=0.1, baudrate=3000000, auto_write=False)
        
        ## image data
        self.image = None
        self.imageWidth = None
        self.imageHeight = None

        self.lineIndex = 0
        self.lastPrintTime = 0

        ## milliseconds expected
        self.ledDelay = delay

        self.isLoaded = False

    def load_image(self, image_path):
        # Open the image
        originalImage = Image.open(image_path)

        # get the image ratio
        image_ratio = originalImage.width / originalImage.height

        self.new_height = self.num_pixels ## height corresponds to the number of pixels
        self.new_width = int(self.new_height * image_ratio) ## width is calculated based on the ratio

        self.imageWidth = self.new_width
        self.imageHeight = self.new_height

        # resize and convert the image into a RGB matrix
        self.image = originalImage.resize((self.new_width, self.new_height)).convert("RGB")

        self.lineIndex = 0
        self.lastPrintTime = 0

        self.pixels.brightness = 0.1
        self.isLoaded = True
    
    def print_image(self):
        ## infinite loop
        while True:
            if self.isLoaded:
                if not self.print_next_line():
                    self.isLoaded = False
                    self.pixels.fill((0,0,0))

    ## returning TRUE when image is still printing
    ## returning FALSE when image is fully printed
    def print_next_line(self):
        if self.lineIndex >= self.imageWidth:
            return False  # Image is fully printed

        current_time = time.time()
        if current_time - self.lastPrintTime < self.ledDelay:
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
