from math import *
import numpy as np
from PIL import Image, UnidentifiedImageError


class PixelImage(object):
    usable = bool
    pil_image = Image
    image_array = np.array

    def __init__(self, image_file_name):
        try:
            self.pil_image = Image.open(image_file_name).convert('RGB')
            self.image_array = np.array(self.pil_image, dtype=np.uint8)
            self.calc_color_average()
        except UnidentifiedImageError as e:
            self.usable = False



    def resize(self,pid):
        '''
        pil = pixel image dimensions
        '''
        self.pil_image = self.pil_image.resize((pid[1],pid[0]))
        self.image_array = np.array(self.pil_image, dtype=np.uint8)



    def get_image(self):
        return self.image_array


    def is_usable(self):
        return self.usable


    def calc_color_average(self):
        self.color_average = np.sum(self.image_array, (0, 1))
        self.color_average = self.color_average / (self.image_array.shape[0] * self.image_array.shape[1])

    def get_color_average(self):
        return self.color_average
