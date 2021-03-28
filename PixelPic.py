import numpy as np
import os
import PixelImageLibrary, TemplateImage, Utilities as u
import random
import time


class PixelPic(object):
    pixel_image_library = PixelImageLibrary
    template_image = TemplateImage
    master_image = np.array
    repeating_images = bool
    size_m = int
    overlay_image = np.array
    overlayed = False

    def __init__(self, template_image, pixel_image_library, size_m, repeating_images):
        """
        template_image: object - contains all information about the image that will be replaced to for final output
        pixel_image_library: object - contains images for all images that may be used for final output
        size_m: int - how much bigger the final image will be than the original. when 1 it will be the same size
        when 2 each dimension will be twice the size
        repeating_images: Bool - determines if images in the image library will be used more than once in final output

        Pixel pic is what creates the final pixelized image - referred to as a pixelPic
        However, when this is created it only stores the information.
        A pixelized image can create created by calling buildMasterImage
        """
        self.template_image = template_image
        self.pixel_image_library = pixel_image_library
        self.size_m = size_m
        self.repeating_images = repeating_images
        self.pixel_image_library.resize_library(
            (self.template_image.get_pid()[0] * size_m, self.template_image.get_pid()[1] * size_m))

    def buildMasterImage(self):
        '''
        uses the pixelized template image and the list of cropped images in image library to find the best match
        for each pixel. it then adds these images to "master image" row by row
        '''
        start = time.time()
        images_per_side = self.template_image.get_images_per_side()
        imageRow = None
        percentDone = 0
        for r in range(images_per_side):
            percentDone = u.updateProgress(percentDone, (r / images_per_side), "building image")
            for c in range(images_per_side):
                targetRGB = self.template_image.get_template_pixel(r, c)
                # finds the image in image library that has the closest RGB value
                selectedImage = self.popBestMatch(targetRGB)
                # adds selected image to the row currently being worked on
                imageRow = self.add_Pixel_image_to_row(c, selectedImage, imageRow)
                # if c == images_per_side-1: # if the row is finished I don't think this is needed but kinda afraid to delete
            self.addRowToMasterImage(r, imageRow)
        end = time.time()
        print("Master image created in", round(end - start, 2), "seconds")

    def popBestMatch(self, targetRGB):
        '''
        targetRGB: tuple of RGB ints
        returns image from image library that has the closest RGB value
        '''

        smallest_dif = np.sum(np.square([256, 265, 265]))
        bestIndex = -1
        difference_list = []  # not used right now
        for i in range(self.pixel_image_library.get_length()):
            difference = np.sum(np.square(self.pixel_image_library.get_pixel_image(i).get_color_average() - targetRGB))
            if difference < smallest_dif:
                smallest_dif = difference
                bestIndex = i
        # bestIndex = self.addVariety(targetRGBs)
        bestMatch = self.pixel_image_library.get_pixel_image(bestIndex)
        # this gives the option to build only using each image once
        if not self.repeating_images:
            self.pixel_image_library.remove_image(bestIndex)
        return bestMatch

    '''
    def addVariety(self, targetRGBs):
        difference_list = []
        for i in range(self.pixel_image_library.get_library_length()):
            difference = np.sum(np.square(self.pixel_image_library.get_image(i).get_color_average() - targetRGBs))
            difference_list.append((difference, i))
        difference_list.sort(key=lambda tup: tup[0])
        options = []

        smallestDifference = difference_list[0][0]
        for i in range(10):
            if smallestDifference + smallestDifference/100 > difference_list[i][0]:
                options.append(difference_list[i])
        bestIndex = options[random.randint(0, len(options) - 1)][1]
        return bestIndex
    '''

    def full_image_comp(self, image):
        """
        image: 2d RGB array of partition
        NOT IN USE
        Can be used instaed of popBestImage finds image bassed on full image comparison instead of average RGB
        """
        smallest_dif = np.sum(np.square(np.power(image - self.pixel_image_library.get_pixel_image(0).get_image(), 2)))
        bestIndex = 0
        for i in range(self.pixel_image_library.get_length()):
            difference = np.sum(np.square(np.power(image - self.pixel_image_library.get_pixel_image(i).get_image(), 2)))
            if difference < smallest_dif:
                smallest_dif = difference
                bestIndex = i
        # bestIndex = self.addVariety(targetRGBs)
        bestMatch = self.pixel_image_library.get_pixel_image(bestIndex)
        # this gave the option to build only using each image once, but is not in use with this version
        if not self.repeating_images:
            self.pixel_image_library.remove_image(bestIndex)
        return bestMatch

    def addRowToMasterImage(self, imagesDown, imageRow):
        """
        This is called in build master image
        concatenates a row to the master image

        """
        if imagesDown == 0:  # if this is the first row being added set master image to imageRow,
            self.master_image = imageRow
        else:  # else concatenate it to the master image
            self.master_image = np.concatenate((self.master_image, imageRow), axis=0)

    def add_Pixel_image_to_row(self, column, pixel_image, image_row):
        """
            This is called in build master image
            concatenates an image to a row

        """
        if column == 0:  # if this is the first column entry in row just return image
            return pixel_image.get_image()
        else:  # else concatenate image to row
            return np.concatenate((image_row, pixel_image.get_image()), axis=1)

    def overlay(self, percent_overlay):
        """
        percent_overlay: float: percent of original image that should be mixed into the master image
        this overlays the template image on the final output to make it look more like the original
        its a trick so don't tell anyone!
        basically does some match and replaes each pixel in master iamge with a combination of the original image
        and the one that image in the master image replaced in the template image
        """
        start = time.time()
        self.overlayed = True
        percent_normal = 1 - percent_overlay
        self.overlay_image = np.zeros(self.master_image.shape)
        og_row_count = self.template_image.get_images_per_side() * self.template_image.get_pid()[0]
        og_column_count = self.template_image.get_images_per_side() * self.template_image.get_pid()[1]
        for r in range(og_row_count):  # rows in original image
            for c in range(og_column_count):  # column in original image
                template_pixel = self.template_image.get_image()[r][c] * percent_overlay
                for rM in range(self.size_m):
                    for cM in range(self.size_m):
                        master_pixel = self.master_image[r * self.size_m + rM][c * self.size_m + cM] * percent_normal
                        self.overlay_image[r * self.size_m + rM][c * self.size_m + cM] = template_pixel + master_pixel
        end = time.time()
        print("overlay completed in", round(end - start, 2), "seconds")

    def get_user_preferences(self):
        '''
        gets the user imputs for:
            if they want images to be reused
            if they do, pixel size of new image
            number of images they want the new image to be created from
        :return: user answers to these questions
        '''
        pixelPercent = " "

        while pixelPercent != "s" and pixelPercent != "m" and pixelPercent != "l":
            # bounding it by the square root limits how large the boarder
            pixelPercent = input(
                "do you want a small (s), medium (m), or large (l) amount of pixel images in your Pixel Pick:")
        return pixelPercent

    def get_master_image(self):
        return self.master_image

    def get_overlay_image(self):
        print(type(self.master_image))
        if (self.overlayed):
            return self.overlay_image
        else:
            return self.master_image
