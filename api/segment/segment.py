import os
import sys
import numpy as np

import pims
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import cv2
from numpy import unravel_index
from scipy import ndimage, misc
from skimage.measure import label, regionprops



def crop(imgToCrop:np.ndarray,
    imgToAnalyze:np.ndarray,
    maskSize:int,
    wellSize:int,
    muToPx:float):

    """

    Crop function. Works only on 2D images. The imgToCrop is the to be cropped
    image and imgToAnalyze serves to find the well center.

    Returns:
    - np.ndarray

    """

    assert len(imgToCrop.shape) == 2

    (xc, yc) = _getCenter(imgToAnalyze,maskSize,wellSize,muToPx)

    cropDist = maskSize*muToPx

    startx = max(xc-(cropDist//2), 0)
    starty = max(yc-(cropDist//2), 0)

    return imgToCrop[int(startx):int(startx+cropDist),int(starty):int(starty+cropDist)]


from api import core

core.

def _getSphCoords(PATH:str, experiment:str, time:str, CHANNEL:str,
    wellDiameter:int, marginDistance:int, umToPx:float):

    """
    CORE FUNCTION:

    Function to retrieve the spheroid coordinates from the BF images. Relies
    upon ID by max gradient values.

    Returns:
    - tuple_of_arrays

    """

    img = pims.ImageSequence(os.path.join(PATH, experiment, CHANNEL, '*.tif'),
        as_grey=True)
    imToCrop = img[int(time)]


    BFimage = cropper._centerSelect(imToCrop, wellDiameter,
        marginDistance, umToPx)
    rRegion = _findSpheroid(BFimage, wellDiameter, umToPx, marginDistance)


    # Image the segmentation to keep intermediary result of the segmentation.
    _verifySegmentationBF(BFimage, rRegion, PATH, experiment, time)

    return np.nonzero(rRegion)


##### Local utility functions #####


def _findSpheroid(imCropped, wellDiameter, umToPx, marginDistance, fraction = 5,
                  minRegionArea = 15000, maxRegionArea = 120000):

    """

    We find the spheroid by thresholding the intensity
    and area filling. Sph. must have a dark border around
    it.

    """


    result1 = ndimage.sobel(imCropped, 1)
    result2 = ndimage.sobel(imCropped, 0)

    mask = cropper._makeDiskMask(wellDiameter, wellDiameter-marginDistance-20,
        umToPx)

    a, b = np.shape(result1)

    sobelMasked = np.multiply(mask[:a, :b], np.sqrt(result1**2+result2**2))
    toThresh = gaussian_filter(sobelMasked, sigma=5)

    imThresh = toThresh > np.max(toThresh)/fraction

    cnts, h = cv2.findContours(imThresh.astype('uint8'), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    temp = cv2.drawContours(imThresh.astype('uint8'), cnts, -1, (255,255,255), thickness=cv2.FILLED)

    imLabel = label(temp)

    for region in regionprops(imLabel):

        if region.area < minRegionArea:
        #check it is inside or outside

            temp[imLabel == region.label] = 0
            #region given same value as sph. border

        if region.area > maxRegionArea:
        #check it is inside or outside

            temp[imLabel == region.label] = 0
            #region given same value as sph. border

        if region.eccentricity > 0.8:
        #check it is inside or outside

            temp[imLabel == region.label] = 0
            #region given same value as sph. border

    return temp

def _verifySegmentationBF(BFimage, rRegion, PATH, experiment, time):

    if not os.path.exists(os.path.join(PATH, experiment, 'Spheroid Region Detection')):
        os.makedirs(os.path.join(PATH, experiment, 'Spheroid Region Detection'))
    savePath = os.path.join(PATH, experiment, 'Spheroid Region Detection')

    fig, ax = plt.subplots(1,1, figsize = (10,10))

    plt.imshow(BFimage, cmap='gray', origin = 'lower')
    plt.imshow(rRegion, alpha = 0.1, origin = 'lower')
    plt.savefig(os.path.join(savePath, 'testFrame_%frame.jpeg' %round(int(time,0))))
    plt.close(fig)

    return
