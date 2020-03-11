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

def _makeCircMask(maskSize:int,
    wellSize:int,
    muToPx:float):

    """

    Makes a donut mask for future convolution.

    Returns:
    - np.ndarray

    """

    cropDist = maskSize*muToPx

    X = np.arange(cropDist)
    Y = X

    X, Y = np.meshgrid(X, Y)

    mask = ((np.sqrt((X-cropDist//2)**2 + (Y-cropDist//2)**2) > (wellSize*muToPx)//2 - 10*muToPx) &
            (np.sqrt((X-cropDist//2)**2 + (Y-cropDist//2)**2) < (wellSize*muToPx)//2 + 10*muToPx))

    return mask.astype(np.int)


def _getCenter(imgToAnalyze:np.ndarray, maskSize:int, wellSize:int,
    muToPx:float):

    """

    Find the well center of an image.

    Returns:
    - tuple

    """

    mask = _makeCircMask(maskSize,wellSize,muToPx)

    conv = cv2.filter2D(imgToAnalyze, cv2.CV_32F, mask)

    return unravel_index(conv.argmin(), conv.shape)


def _centerSelect(imToCrop:np.ndarray, wellDiameter:int, marginDistance:int,
    umToPx:float):

    """

    Function to take image, find the well center,
    throw away all the points beyond the marginDistance.

    Returns:
    - np.ndarray

    """

    img = _crop(imToCrop, imToCrop, wellDiameter, wellDiameter, umToPx)

    mask = _makeDiskMask(wellDiameter, wellDiameter-marginDistance, umToPx)
    t = np.zeros(np.shape(mask))
    a, b = np.shape(img)
    t[:a, :b] = img
    #combine pour gerer les crops de forme non carree

    finalIm = np.multiply(t, mask)
    finalIm[finalIm == 0] = np.max(finalIm)

    return gaussian_filter(finalIm, sigma=5)


def _makeDiskMask(maskSize:int, diskSize:int, umToPx:float):

    """

    Makes a circular mask of given radius.

    Returns:
    - np.ndarray

    """

    cropDist = int(maskSize*umToPx)

    X = np.arange(cropDist)
    Y = X
    X, Y = np.meshgrid(X, Y)

    mask = (np.sqrt((X-cropDist//2)**2 + (Y-cropDist//2)**2) < (diskSize*umToPx)//2)

    return mask.astype(np.int)

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