from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from logging.config import dictConfig
from threading import Thread

## custom defined imports
from neopixelWrapper import DotStarWrapper
from tablegenerator import TableGenerator
from simpleInterface import SimpleInterface

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
templeteSimple = os.path.join('templates', 'simple.html')
pic_dir = 'static/pictures'



FlaskApp = Flask(__name__)  
tableGenerator = TableGenerator(templateTablePath, templateTableRowPath, pic_dir)
SimpleInterface = SimpleInterface(templeteSimple)
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

@FlaskApp.route('/off', methods=['GET', 'POST'])
def Off():
    if request.method == 'POST' and request.form['off_button'] == 'Turn Off':
        FlaskApp.logger.info("Turning off")
        os.system("shutdown now")
        
    FlaskApp.logger.info("Rendering off.html")
    return render_template('off.html')

@FlaskApp.route('/simple_redir')
def Simple_redir():
    return redirect(url_for('Simple'))


@FlaskApp.route('/simple', methods=['GET', 'POST'])
def Simple():
    FlaskApp.logger.info("Rendering simple.html")
    if request.method == 'POST':
        print(request.form)
        if request.form.get('add_color') == 'Add color':
            # TODO form validation
            # dont have to do if i have colors
            r = request.form.get('color_r')
            g = request.form.get('color_g')
            b = request.form.get('color_b')
            SimpleInterface.add_color((int(r), int(g), int(b)))
        elif request.form.get('rotate90'):
            FlaskApp.logger.info("rotating 90 degs")
        elif request.form.get('grad'):
            FlaskApp.logger.info("changing grad/just light model")
        elif request.form.get('start') == "START":
            SimpleInterface.display_image()
        return redirect(url_for('Simple_redir'))
        
        # TODO somehow clear the form

    # if request
    # prepare functions to create numpy arrays with appropriate pixel values
    # make numpy array with pixels
    return SimpleInterface.render()

def removeFile(filename: str):
    if os.path.isfile(os.path.join(pic_dir, filename)):
        os.remove(os.path.join(pic_dir, filename))
        return True
    return False

if __name__ == "__main__":
        imageThread = Thread(target=neopixel.print_image, daemon=True)
        imageThread.start()
        FlaskApp.run(host='0.0.0.0', debug=True)