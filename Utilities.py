# from sklearn.cluster import KMeans
# from sklearn.utils import shuffle
import numpy as np
#import cv2
import time


def writeImageToPPM(filename, image):
    """
    This functions takes a ppm image stored in the format of a 3D list [y][x][c] where
    c is color channel
        0 for red
        1 for green
        2 for blue
    and writes a plain text P3 style PPM image under the name filename
    Args: image name, image data
    Return: none
    """
    start = time.time()
    height = len(image)
    width = len(image[0])
    print("writing image with dimensions", height, " X ", width)
    f = open(filename, "w")
    f.write("P3\n")
    f.write(str(width) + " " + str(height) + "\n")
    f.write("255\n")
    percentDone = 0
    for y in range(len(image)):
        percentDone = updateProgress(percentDone, (y / len(image)), "writing image to " + str(filename))
        for x in range(len(image[y])):
            # for c in range(len(image[y][x])):
            for c in range(3):
                f.write(str(int(image[y][x][c])) + " ")
            f.write("\n")
    f.close()
    end = time.time()
    print(filename, " written to file in ", round(end - start, 2), "seconds")


def updateProgress(percentDoneBefore, PercentDoneNow, actionString):
    timeDivider = 10
    percentDoneNow = int(PercentDoneNow * timeDivider)
    # if percentDoneNow > percentDoneBefore *timeDivider:
    # print(percentDoneNow * timeDivider, "percent done " + actionString)
    return percentDoneNow


def uniquelyNameFile(fileName, fileList):
    """
    fileName: String
    fileList: Array of string
    checks if file name if in list, if not returns filename, else adds number that makes it unique
    """
    if fileName not in fileList:
        return fileName
    version = 1
    fileName = fileName.split('.', -1)
    candidateName = fileName[0] + " " + str(version) + "." + fileName[1]
    while candidateName in fileList:
        version += 1
        candidateName = fileName[0] + " " + str(version) + "." + fileName[1]
    return candidateName


def setFileExstension(name, extension):
    '''
    this just adds the given extension to a string
    '''
    name = name.split('.', -1)
    return name[0] + "." + extension

