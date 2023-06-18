from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from logging.config import dictConfig
from threading import Thread

## custom defined imports
from neopixelWrapper import DotStarWrapper
from tablegenerator import TableGenerator

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

templateTableRowPath = os.path.join('templates', 'pictureTableRow.html')
templateTablePath = os.path.join('templates', 'picturesTable.html')
pic_dir = 'static/pictures'



FlaskApp = Flask(__name__)  
tableGenerator = TableGenerator(templateTablePath, templateTableRowPath, pic_dir)
neopixel = DotStarWrapper(0.05)

@FlaskApp.route('/', methods=['GET','POST'])
def Index():
    if request.method == 'POST':
        # Check if the POST request tries to upload a file
        if 'image' in request.files:

            image_file = request.files['image']

            # Check if the user submitted an empty form
            if image_file.filename == '':
                return 'No selected image'

            # Process the uploaded image
            # You can save the image to disk or perform any other operations here

            if not os.path.isdir(pic_dir):
                os.makedirs(pic_dir)

            image_file.save(os.path.join(pic_dir, secure_filename(image_file.filename)))

        ## check status of buttons
        else:
            FlaskApp.logger.info("Checking all pictures to match button request...")
            for picture_path in os.listdir(pic_dir):

                FlaskApp.logger.info(f"Checking {picture_path}")

                if request.form.get(f'delete-{picture_path}') == 'DELETE':
                    FlaskApp.logger.info(f"Deleting {picture_path}")
                    removeFile(picture_path)

                elif request.form.get(f'start-{picture_path}') == 'START':
                    image_path = os.path.join(pic_dir, picture_path)
                    FlaskApp.logger.info(f"Starting {image_path}")
                    neopixel.load_image(image_path)

        FlaskApp.logger.info("Generating table of available pictures")
        return tableGenerator.createPicturesTable()
    
    elif request.method == 'GET':
        FlaskApp.logger.info("Generating table of available pictures")
        return tableGenerator.createPicturesTable()

def removeFile(filename: str):
    if os.path.isfile(os.path.join(pic_dir, filename)):
        os.remove(os.path.join(pic_dir, filename))
        return True
    return False

if __name__ == "__main__":
        imageThread = Thread(target=neopixel.print_image, daemon=True)
        imageThread.start()
        FlaskApp.run(host='0.0.0.0', debug=True)