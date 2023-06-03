# i want to write a simple python flask app which will allow me to control the neopixel strip

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

FlaskApp = Flask(__name__)

@FlaskApp.route('/img', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'image' not in request.files:
            return 'No image file uploaded'

        image_file = request.files['image']

        # Check if the user submitted an empty form
        if image_file.filename == '':
            return 'No selected image'

        # Process the uploaded image
        # You can save the image to disk or perform any other operations here
        pic_dir = 'pictures'

        if not os.path.isdir(pic_dir):
            os.makedirs(pic_dir)

        image_file.save(os.path.join(pic_dir, secure_filename(image_file.filename)))

        return 'Image uploaded successfully'

    return render_template('upload.html')

@FlaskApp.route("/")
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    FlaskApp.run(host='0.0.0.0', debug=True)
    # TODO use on rpi to run on prot 80
    # FlaskApp.run(host='0.0.0.0', port=80, debug=True)
