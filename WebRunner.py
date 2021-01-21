import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import PixelPic
import TemplateImage
import PixelImageLibrary
import Utilities as u
import os
import numpy as np
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'ppm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        usable_file = False
        usable_folder = False
        

        # check if the post request has the file part
        if 'file' not in request.files or 'folder' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        folder = request.files.getlist("folder")
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if len(folder) == 0:
            flash('No selected folder')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            usable_file = True
        for file in folder:
            if file and allowed_file(file.filename):
                usable_folder = True
                folder_filename = secure_filename(file.filename.split('/')[-1])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], folder_filename))
        if usable_file and usable_folder:
            template_image = TemplateImage.TemplateImage(UPLOAD_FOLDER+"/"+filename, images_per_side_string="m")
            pixel_image_library = PixelImageLibrary.PixelImageLibrary(UPLOAD_FOLDER)
            pixel_pic = PixelPic.PixelPic(template_image, pixel_image_library, size_m=1, repeating_images=True)
            pixel_pic.buildMasterImage()
            pil_pixel_pic = Image.fromarray(pixel_pic.get_overlay_image())
            pil_pixel_pic.show()
            pil_pixel_pic.save(OUTPUT_FOLDER+"/pixelPic.png")
            return redirect(url_for('uploaded_file',filename="/pixelPic.png"))
    return  render_template("upload.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'],filename)

if __name__ == '__main__':
    app.run(debug=True)