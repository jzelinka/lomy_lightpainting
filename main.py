# i want to write a simple python flask app which will allow me to control the neopixel strip

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os, logging
from logging.config import dictConfig

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

class TableGenerator:
    def __init__(this):
        pass

    ## Creates a new table with pictures and buttons
    def createPicturesTable(this):
        return this.fillPictureTable()

    ## Fills the table with all pictures in the picture directory
    def fillPictureTable(this):
        rows = ""
        for picture_path in os.listdir(pic_dir):
            rows += this.fillTableRow(picture_path)
        template = open(templateTablePath).read()
        template = template.replace("[PICTURE-ROWS]", rows)
        return template

    ## Fills a table row with the picture and buttons
    def fillTableRow(this, filename: str):
        template = open(templateTableRowPath).read()
        template = template.replace("[PICTURE-PATH]", f'{pic_dir}/{filename}')
        template = template.replace("[PICTURE-NAME]", filename.split('/')[-1])
        return template

FlaskApp = Flask(__name__)  
tableGenerator = TableGenerator()

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
            FlaskApp.logger.info("Checking all pictures to match deletion request...")
            for picture_path in os.listdir(pic_dir):
                FlaskApp.logger.info(f"Checking {picture_path}")
                if request.form.get(f'delete-{picture_path}') == 'DELETE':
                    FlaskApp.logger.info(f"Deleting {picture_path}")
                    removeFile(picture_path)

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
        FlaskApp.run(host='0.0.0.0', debug=True)
    # TODO use on rpi to run on prot 80
    # FlaskApp.run(host='0.0.0.0', port=80, debug=True)
