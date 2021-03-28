from math import *
import numpy as np
from PIL import Image, UnidentifiedImageError


class PixelImage(object):
    usable = bool
    pil_image = Image
    image_array = np.array

    def __init__(self, image_file_name):
        """"
        image_file_name: string - path to image
        opens image and saves it as a numpy array
        naming system is weird sorry.
        Pixel images are all the images that may be used to replaces pixels in the template images t form a pixel pic
        """
        try:
            self.pil_image = Image.open(image_file_name).convert('RGB')
            self.image_array = np.array(self.pil_image, dtype=np.uint8)
            self.calc_color_average()
        except UnidentifiedImageError as e:
            self.usable = False



    def resize(self,pid):
        '''
        pid = pixel image dimensions tupels of ints
        resizes image to PID
        '''
        self.pil_image = self.pil_image.resize((pid[1],pid[0]))
        self.image_array = np.array(self.pil_image, dtype=np.uint8)



    def get_image(self):
        return self.image_array


    def is_usable(self):
        """
        returns false if there was some error in opening image
        """
        return self.usable


    def calc_color_average(self):
        """
        calculates the average color of pixel iamge
        """
        self.color_average = np.sum(self.image_array, (0, 1))
        self.color_average = self.color_average / (self.image_array.shape[0] * self.image_array.shape[1])

    def get_color_average(self):
        return self.color_average
