# Lightpainting stick
The goal of the project is to create a lightpainting stick to enhance photos taken with a camera on a longer exposure.
A Raspberry Pi is used as a controler of the LED strip.
Additionally, the Raspberry Pi is configured as a WiFi access point.
The stick is then controlled via a web interface using devices connected to the WiFi access point. Thanks to the web interface, the need for physical buttons is eliminated. The web app an upload of bitmap images. The resolution of the uploaded images is downscaled so that they draw using the stick. The whole stick is powered by a power bank, which makes the whole setup portable and capable of drawing even in field conditions.
The repository contains the code for the Raspberry Pi's web interface and led strip driver. The web app is implemented with the help of `Flask` and `adafruit_dotstar` library.

TODO show a picture with some lightpainting

## Usage
Install the required packages by running the following command:
```bash
pip install -r requirements.txt
```
Run the server by executing the following command:
```bash
python main.py
```
Open the server in a web browser and start uploading images. The drawing requires setup of the number of leds and the specification of the pins, where the led strip is connected. The setup can be found in `neopixelWrapper.py` and the fields to be edited are:
```python
self.num_pixels = 216 # Number of pixels in the DotStar strip
self.pin_sck = 11
self.pin_mosi = 10
```

### Disclaimer
TODO we know that it is not perfect