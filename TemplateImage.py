from PIL import Image
from math import *
import numpy as np
import time


class TemplateImage(object):
    template_image = np.array
    images_per_side = int
    pid = tuple  # pixel image dimensions
    partitioned_image = []
    pixelated_image = np.array

    def __init__(self, image, images_per_side_string):
        """
        Image: string - path to image
        images_per_side_string - char (not my best naming) either S, M, or L. This will be translated into an int
        this int will define how many pieces the template image will be partitioned into
        Note images per side and PID are independent

        This opens the given image and decideds how many peices to partition it into.
        This then creates a new 2d array, partitioned array, of sub images (also 2d arrays)
        sub images have dimensions pid x pid and are comprised of the pixels in the original image
        partition array has dimension images_per_side

        Finally creates a Pixelated image. This is a Images_per_side X Images_per_side image
        comprised of the average colors of each partition

        """
        # opens image and reformats image into numpy array
        self.template_image = np.array((Image.open(image)).convert("RGB"), dtype=np.uint8)
        # calculates the number of sections per side the the image will be partitioned into
        self.set_images_per_side(images_per_side_string)

        # calculates the pixel image dimensions.
        # This is how big each pixel image would have to be to exactly replace the pixels in a partition
        self.pid = (int(self.template_image.shape[0] / self.images_per_side),
                    int(self.template_image.shape[1] / self.images_per_side))
        # partitions the template image
        self.partition_template()


        self.pixelate_template()

    def partition_template(self):
        """
        Creates new 2d array with dimension Images_per_side,
        and adds pid x pid sub images to that array from template image
        the result is almost exactly the same as the original image but broken into PID PID pieces

        Honestly if I was writing this now I don't think I would do this
        """
        start = time.time()
        for r in range(self.images_per_side):
            self.partitioned_image.append([])
            for c in range(self.images_per_side):
                # creates a partitioned piece of image and adds it to partitioned image
                self.partitioned_image[r].append(self.create_sub_image(r * self.pid[0], c * self.pid[1]))
        end = time.time()
        print("template image partitioned in", round(end - start, 2), "seconds")

    def create_sub_image(self, start_row, start_column):
        """
        start_row: int
        start_column: column
        does not really need to be a separate function but used to be more complicated
        returns a piece of template image oof size PID X PID start at point start_row and start_column
        """
        sub_image = self.template_image[start_row:start_row + self.pid[0], start_column:start_column + self.pid[1]]
        return sub_image

    def pixelate_template(self):
        """
        creates a Pixelated image. This is a Images_per_side X Images_per_side image
        comprised of the average colors of each partition
        """
        start = time.time()
        # creates pixelated image
        self.pixelated_image = np.zeros((self.images_per_side, self.images_per_side, 3))
        for r in range(self.images_per_side):
            for c in range(self.images_per_side):
                # calculates the average RGB of each partition
                self.pixelated_image[r][c] = np.mean(self.partitioned_image[r][c], axis=(0, 1))
        end = time.time()
        print("template image pixilated  in", round(end - start, 2), "seconds")

    def set_images_per_side(self, images_per_side_string):
        """
        images_per_side_string: string S M or L roughly the desired size of pixel image
        This calculates the Images per side. that is the number of images that the template image will be transformed into

        """
        min_size = int(sqrt(self.template_image.shape[0]))
        max_size = int(sqrt(min_size) * min_size)
        mid_size = int((max_size + min_size) / 4)
        # min_size = ceil(self.template_image.shape[0]/1000)
        # mid_size = ceil(self.template_image.shape[0]/100)
        # max_size = ceil(self.template_image.shape[0]/10)
        # print(self.template_image.shape[0], min_size, mid_size, max_size)
        if images_per_side_string == "s":
            self.images_per_side = min_size
        elif images_per_side_string == "m":
            self.images_per_side = mid_size
        elif images_per_side_string == "l":
            self.images_per_side = max_size
        else:
            print("=========ERROR, USER INPUT NOT CORRECT==========")

    def get_image(self):
        return self.template_image

    def get_partitioned_image(self):
        return self.partitioned_image

    def get_pid(self):
        return self.pid

    def get_images_per_side(self):
        return self.images_per_side

    def get_template_pixel(self, r, c):
        return self.pixelated_image[r][c]

    # ==========not useing =================================
    #
    # def get_user_preferences(self):
    #     '''
    #     gets the user imputs for:
    #         if they want images to be reused
    #         if they do, pixel size of new image
    #         number of images they want the new image to be created from
    #     :return: user answers to these questions
    #     '''
    #     print("template shape is", self.template_image.shape)
    #     max_size = int(sqrt(self.template_image.shape[0]))
    #     max_size = int(ceil(max_size * ceil(sqrt(max_size))))
    #
    #     while self.images_per_side not in range(1, max_size + 1):
    #         # bounding it by the square root limits how large the boarder
    #         self.images_per_side = int(
    #             input("how many images do you want on each edge, between 1 and " + str(max_size)))
    #
    # def pixelate_image_old(self):
    #     '''
    #
    #     :param images_across:
    #     :param sections_per_side:
    #     :return:
    #     '''
    #     print("===STATS====")
    #     print("TEMPLATE SHAPE", self.template_image.shape)
    #     print("images per side", self.images_per_side)
    #     print("pixels per image across ", self.pixel_image_dimension_across)
    #     print("pixels per image down ", self.pixel_image_dimension_down)
    #     self.pixelated_image = np.zeros((self.images_per_side, self.images_per_side, 3))
    #     # iterating through sections that will become images, row by row/ down
    #
    #     for r in range(self.images_per_side):
    #         if r == self.images_per_side - 1:
    #             holder_down = self.template_image.shape[0] - (
    #                         self.images_per_side - 1) * self.pixel_image_dimension_down
    #             print("holder down", holder_down)
    #         else:
    #             holder_down = self.pixel_image_dimension_down
    #         # iterating through sections that will become images, by column / across
    #         for c in range(self.images_per_side):
    #             if c == self.images_per_side - 1:
    #                 holder_across = self.template_image.shape[1] - (
    #                         (self.images_per_side - 1) * self.pixel_image_dimension_across)
    #                 # print("holder across", holder_across)
    #             else:
    #                 holder_across = self.pixel_image_dimension_across
    #             # iterating through pixels in each section, rp = row pixel
    #             samples_taken = 0
    #             row_step = int(sqrt(holder_down)) + 1
    #             for rp in range(0, int(holder_down), row_step):
    #                 # iterating through pixels in each section, cp = column pixel
    #                 column_step = int(sqrt(holder_down)) + 1
    #                 for cp in range(0, int(holder_across), column_step):
    #                     # iterating through rgb values
    #                     samples_taken += 1
    #                     self.pixelated_image[r][c] += self.template_image[r * self.pixel_image_dimension_down + rp][
    #                         c * self.pixel_image_dimension_across + cp]
    #             if samples_taken > 0:
    #                 for i in range(3):
    #                     self.pixelated_image[r][c][i] = self.pixelated_image[r][c][i] / samples_taken
    #     print("done with pixelation:", self.pixelated_image.shape)
