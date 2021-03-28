import PixelPic
import TemplateImage
import PixelImageLibrary
import Utilities as u
import os
import numpy as np
from PIL import Image


def main():
    """
    Main Runner for terminal based program.
    uses image and folder to create a new image that has the same average rgb values as the chosen template image
    but is entirely made up of images from folder
    to change images per side side change m to l to increase or s to decrease
    to change quality of those images change size_m - size multiplier
    """
    images_per_side_string = "m"  # number of images on each axis of pixel image
    size_m = 1  # size of new image, when 1 the new image will be the size dimensions as originial template image
    folder = "Posters_small"  # path to folder
    image = "Dogs Playing Poker.jpg"  # path to image that will be used as template

    # creates template image object. This is a 2d array of RGB values bassed on the image
    template_image = TemplateImage.TemplateImage(image, images_per_side_string)

    # creates a pixel image library. This is a list of all images in the image folder
    pixel_image_library = PixelImageLibrary.PixelImageLibrary(folder)

    # uses pixel image library and and template image to create pixel pic object.
    # this at first simply holds all relevant information to create a pixelized image
    pixel_pic = PixelPic.PixelPic(template_image, pixel_image_library, size_m, repeating_images=True)

    # This builds the actual pixelized image.
    pixel_pic.buildMasterImage()

    # Overlays the master image with the original image to make iti look better.
    pixel_pic.overlay(0.3)

    # gives pixel pic a unique name and saves it to file.
    pixelPic_name = u.setFileExstension(image, "ppm")
    files = os.listdir("../PixelPic")
    pixelPic_name = u.uniquelyNameFile("Pixelized " + pixelPic_name, files)
    u.writeImageToPPM(pixelPic_name, pixel_pic.get_overlay_image())
    print("done")


def experiment():
    '''
    experiments to figure out best way to crate pixel pic
    '''
    files = os.listdir("../PixelPic")
    image1 = "good_test.jpeg"
    image2 = "base.jpeg"
    image3 = "bad_test.jpeg"
    image1 = np.array(Image.open(image1), dtype=np.uint8)  # reformat into numpy array
    image2 = np.array(Image.open(image2), dtype=np.uint8)  # reformat into numpy array
    image3 = np.array(Image.open(image3), dtype=np.uint8)  # reformat into numpy array
    hist_image1 = u.calc_hist(image1)
    hist_image2 = u.calc_hist(image2)
    hist_image3 = u.calc_hist(image3)
    print("good nad base", u.compare_hist(hist_image1, hist_image2))
    print("bad and base", u.compare_hist(hist_image2, hist_image3))
    print("bad and good", u.compare_hist(hist_image1, hist_image3))

    '''
    new_image = np.zeros((image.shape[0],image.shape[1],5))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
                new_image[i][j][0] = image[i][j][0]
                new_image[i][j][1] = image[i][j][1]
                new_image[i][j][2] = image[i][j][2]
                new_image[i][j][3] = i
                new_image[i][j][4] = j
    new_image = u.segmentImage(image,12)
    print(new_image.shape)
    file_name = u.uniquelyNameFile("image_resize_test.ppm", files)
    u.writeImageToPPM(file_name, new_image)
'''


# experiment()
main()
