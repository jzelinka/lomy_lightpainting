import time
import adafruit_dotstar as dotstar
from PIL import Image

class DotStarWrapper:
    def __init__(self):
        self.num_pixels = 216 # Number of pixels in the DotStar strip
        self.pin_sck = 11
        self.pin_mosi = 10

        ## milliseconds expected
        self.ledDelay = 0.05

        ## brightness between 0 and 1
        self.ledBrightness = 0.1

        # auto_write=False means that the pixels won't change colors until you call pixels.show()
<<<<<<< HEAD
        self.pixels = dotstar.DotStar(self.pin_sck, self.pin_mosi, self.num_pixels, brightness=self.ledBrightness, baudrate=1000000, auto_write=False)
=======
        self.pixels = dotstar.DotStar(self.pin_sck, self.pin_mosi, self.num_pixels, brightness=self.ledBrightness, baudrate=3000000, auto_write=False)
>>>>>>> e555155419eefed3678b5e40b766e4dd1a92fe3d
        #self.pixels = []
        
        ## image data
        self.image = None
        self.imageWidth = None
        self.imageHeight = None
 
        self.lineIndex = 0
        self.lastPrintTime = 0

        self.isLoaded = False

    
    def load_numpy_array(self, numpy_array):
        # create tmp image from numpy array
        # load image for drawing
        # delete tmp image
        pass

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

        ## is controlled by single button
        # self.lineIndex = 0
        # self.lastPrintTime = 0
        # self.pixels.brightness = self.ledBrightness
        # self.isLoaded = True
    
    def print_image(self):
        ## change the brightness (might be changed by the user)
        self.pixels.brightness = self.ledBrightness
        print(self.pixels.brightness)
        ## infinite loop
        while True:
            if self.isLoaded:
                if not self.print_next_line():
                    self.isLoaded = False
                    self.pixels.fill((0,0,0))
                    self.pixels.show()
                    print('Finished printing')

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
            self.pixels[self.num_pixels - pixel_index - 1] = (r, g, b)

        # Update the Neopixels to display the current line
        self.pixels.show()

        self.lineIndex += 1
        self.lastPrintTime = current_time
        print('Printing line', self.lineIndex)
        return True  # Image printing is in progress

    def stop_printing(self):
        self.isLoaded = False
        self.lineIndex = 0
        self.lastPrintTime = 0
        self.pixels.fill((0,0,0))
        self.pixels.show()
        print('Stopped printing')

    def start_printing(self):
        self.lineIndex = 0
        self.lastPrintTime = 0
        self.pixels.brightness = self.ledBrightness
        self.isLoaded = True
