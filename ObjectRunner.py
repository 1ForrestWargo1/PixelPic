import PixelPic
import TemplateImage
import PixelImageLibrary
import Utilities as u
import os
import numpy as np
from PIL import Image


def main():

    size_m = 1
    #folder = "Test_image_folder"
    #image = "Tester_img.jpeg"
    folder = "Posters_small"
    image = "Dogs Playing Poker.jpg"
    template_image = TemplateImage.TemplateImage(image, images_per_side_string="m")
    pixel_image_library = PixelImageLibrary.PixelImageLibrary(folder)
    pixel_pic = PixelPic.PixelPic(template_image, pixel_image_library, size_m, repeating_images=True)
    files = os.listdir("../PixelPic")
    pixel_pic.buildMasterImage()
    #pixel_pic.overlay((0.3))
    pixelPic_name = u.setFileExstension(image, "ppm")
    pixelPic_name = u.uniquelyNameFile("Pixelized " + pixelPic_name, files)
    u.writeImageToPPM(pixelPic_name, pixel_pic.get_overlay_image())
    print("done")


def experiment():
    files = os.listdir("../PixelPic")
    image1 = "good_test.jpeg"
    image2 = "base.jpeg"
    image3 = "bad_test.jpeg"
    image1 = np.array(Image.open(image1), dtype=np.uint8)  # reformat into numpy array
    image2 = np.array(Image.open(image2), dtype=np.uint8)  # reformat into numpy array
    image3 = np.array(Image.open(image3), dtype=np.uint8)  # reformat into numpy array
    hist_image1 = u.calc_hist(image1)
    hist_image2  = u.calc_hist(image2)
    hist_image3  = u.calc_hist(image3)
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


#experiment()
main()