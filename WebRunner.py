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
def handle_user_upload():
    """
    This takes the uploaded file and folder and outputs finished pixelized image
    """
    if request.method == 'POST':
        usable_file = False
        usable_folder = False

        # check if the post request does not contain image file
        if 'file' not in request.files:
            flash("missing image file")
        # check if the post request does not contain image folder
        if 'folder' not in request.files:
            flash("missing image folder ")
            return redirect(request.url)
        file = request.files['file']  # get image file
        folder = request.files.getlist("folder")  # get iamge folder

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # check if folder is empty
        if len(folder) == 0:
            flash('empty folder')
            return redirect(request.url)

        # makes sure the image file is a safe file extension
        if file and allowed_file(file.filename):
            #  someone online said to do this, I dont remember what it does
            filename = secure_filename(file.filename)

            # save image file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            usable_file = True

        # do the sae thing as with image file for each image in image folder
        for file in folder:
            if file and allowed_file(file.filename):
                usable_folder = True
                folder_filename = secure_filename(file.filename.split('/')[-1])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], folder_filename))

        if usable_file and usable_folder:
            # creates template image object. This is a 2d array of RGB values based on the image
            template_image = TemplateImage.TemplateImage(UPLOAD_FOLDER + "/" + filename, images_per_side_string="m")

            # creates a pixel image library. This is a list of all images in the image folder
            pixel_image_library = PixelImageLibrary.PixelImageLibrary(UPLOAD_FOLDER)

            # uses pixel image library and and template image to create pixel pic object.
            # this at first simply holds all relevant information to create a pixelized image
            pixel_pic = PixelPic.PixelPic(template_image, pixel_image_library, size_m=1, repeating_images=True)

            # This builds the actual pixelized image.
            pixel_pic.buildMasterImage()

            # saves pixrlized image
            pil_pixel_pic = Image.fromarray(pixel_pic.get_overlay_image())
            pil_pixel_pic.show()
            pil_pixel_pic.save(OUTPUT_FOLDER + "/pixelPic.png")

            #shows the image to user
            return redirect(url_for('uploaded_file', filename="/pixelPic.png"))
    return render_template("upload.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    sends file name to wbe page
    """
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
