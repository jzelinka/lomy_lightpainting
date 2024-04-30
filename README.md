# Lightpainting stick
The project aims to create a light painting stick to enhance photos taken with a camera over prolonged exposure.
A Raspberry Pi is used as a controller of the LED strip.
Additionally, the Raspberry Pi is configured as a WiFi access point.
The stick is then controlled via a web interface using devices connected to the WiFi access point.
Thanks to the web interface, the need for physical buttons is eliminated.
The web app uploads bitmap images.
The resolution of the uploaded images is downscaled so that they draw using the stick.
The whole stick is powered by a power bank, which makes the entire setup portable and capable of drawing even in field conditions.

The repository contains the code for Raspberry Pi's web interface and LED strip driver.
The web app is implemented with the help of the `Flask` and `adafruit_dotstar` library.

TODO show a picture

## Usage
Install the required packages by running the following command:
```bash
pip install -r requirements.txt
```
Run the server by executing the following command:
```bash
python main.py
```
Open the server in a web browser and start uploading images.
The drawing requires setting up the number of LEDs and the specification of the pins where the LED strip is connected.
The setup can be found in `neopixelWrapper.py`, and the fields to be edited are:
```python
self.num_pixels = 216 # Number of pixels in the DotStar strip
self.pin_sck = 11
self.pin_mosi = 10
```

### Disclaimer
This project does not include a production-ready version, and the authors assume the user's interest in the final pictures created using the light painting stick.
Thus, the code does not include any reasonable security measures.