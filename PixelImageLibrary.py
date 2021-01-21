from PIL import Image, UnidentifiedImageError
import numpy as np
import os
import PixelImage, Utilities as u
import time


class PixelImageLibrary(object):
    folder_name = str
    image_library = list
    images_in_folder = 0
    failCount = 0
    usable_images_count = 0
    pid = None
    files = list

    def __init__(self, folder):
        self.image_library = []
        if type(folder) == str:
            self.folder_name = folder
            self.files = os.listdir(self.folder_name)
            self.images_in_folder = len(self.files)
            #print(self.files)
            for i in range(len(self.files)):
                self.files[i] = self.folder_name + "/" + self.files[i]

        elif type(folder) == list:
            self.folder_name = "user_folder"
            self.files = folder

        self.create_pixel_images()
        print(self.failCount, "images failed out of ", self.images_in_folder)
        print("total usable images =", self.usable_images_count)


    def create_pixel_images(self):
        start = time.time()
        for i in range(len(self.files)):
            image = PixelImage.PixelImage(self.files[i])
            if image.is_usable():
                self.image_library.append(image)
                self.usable_images_count +=1
            else:
                self.failCount +=1
        end = time.time()
        print("library created in",round(end - start,2),"seconds")



    def resize_library(self, pid):
        start = time.time()
        for i in range(len(self.image_library)):
            self.image_library[i].resize(pid)
        end = time.time()
        print("library resized in",round(end - start,2),"seconds")
    def get_pixel_image(self, index):
        return self.image_library[index]

    def get_length(self):
        return len(self.image_library)

    def remove_image(self, index):
        self.image_library.pop(index)




#============ not in use==========================

    def open_image_folder(self):
        self.files = os.listdir(self.folder_name)
        self.images_in_folder = len(self.files)
        self.getUsableImages()
        self.usable_images_count = self.images_in_folder - self.failCount

    def getUsableImages(self):
        percent_done = 0
        for i in range(len(self.files)):
            u.updateProgress(percent_done,(i / len(self.files)),"loading images from folder")

            try:
                self.image_library.append(
                    PixelImage.PixelImage(np.array(Image.open(self.folder_name + "/" + self.files[i]).convert('RGB'), dtype=np.uint8)))

            except UnidentifiedImageError as e:
                self.failCount += 1

    def check_rgb_dimensions(self):
        for i in range(self.usable_images_count - 1, 0, -1):
            if self.image_library[i].get_shape()[2] != 3:

                self.image_library.pop(i)
                self.failCount += 1
        self.usable_images_count = self.images_in_folder - self.failCount