import os
import sys

import api.segment.utilities as utilities
import cv2
import numpy as np
import pims
from numpy import unravel_index
from scipy import misc
from scipy import ndimage
from scipy.ndimage import gaussian_filter
from skimage.measure import label
from skimage.measure import regionprops


def select_well(
    imgToAnalyze: np.ndarray,
    imgToCrop: np.ndarray,
    maskSizeUm: int,
    wellDiameterUm: int,
    mutopx: float,
):

    """

    From 2D BF image finds and crops around well position.

    Returns:
     - np.ndarray

    """

    boolMask = find_well(imgToAnalyze, maskSizeUm, wellDiameterUm, mutopx)

    return crop(imgToCrop, boolMask)


def crop(imgToCrop: np.ndarray, boolMask: np.ndarray):

    """

    Crop function. Works only on 2D images. The imgToCrop is the to be cropped
    image and imgToAnalyze serves to find the well center.

    Returns:
    - np.ndarray

    """

    assert imgToCrop.shape == boolMask.shape

    coords = np.argwhere(boolMask)
    x_min, y_min = coords.min(axis=0)
    x_max, y_max = coords.max(axis=0)

    return np.multiply(imgToCrop, boolMask.astype(int))[
        x_min : x_max + 1, y_min : y_max + 1
    ]


def find_well(
    imgToAnalyze: np.ndarray, maskSizeUm: int, wellDiameterUm: int, mutopx: float
):

    """

    Returns a np.ndarray(bool) where the well area is delimited by True
    values.

    """

    assert len(imgToAnalyze.shape) == 2

    (xc, yc) = utilities._get_center(imgToAnalyze, maskSizeUm, wellDiameterUm, mutopx)

    cropDist = maskSizeUm * mutopx

    startx = max(xc - (cropDist // 2), 0)
    starty = max(yc - (cropDist // 2), 0)

    boolArray = np.zeros_like(imgToAnalyze, dtype=bool)
    boolArray[
        int(startx) : int(startx + cropDist), int(starty) : int(starty + cropDist)
    ] = True

    return boolArray


def find_spheroid(
    imCropped: np.ndarray,
    wellDiameterUm: int,
    mutopx: float,
    marginDistance=100,
    fraction=3.5,
    minRegionArea=1000,
    maxRegionArea=120000):

    """

    We find the spheroid by thresholding the intensity
    and area filling. Sph. must have a dark border around
    it.

    Returns:
     - labeled array.

    """

    result1 = ndimage.sobel(imCropped, 1)
    result2 = ndimage.sobel(imCropped, 0)

    mask = utilities._make_disk_mask(
        wellDiameterUm, wellDiameterUm - marginDistance, mutopx
    )

    nx, ny = np.shape(result1)
    mask = mask[:nx,:ny]

    sobelMasked = np.multiply(mask, np.sqrt(result1 ** 2 + result2 ** 2))
    toThresh = gaussian_filter(sobelMasked, sigma=5)

    imThresh = toThresh > np.max(toThresh) / fraction

    cnts, _ = cv2.findContours(
        imThresh.astype("uint8"), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    temp = cv2.drawContours(
        imThresh.astype("uint8"), cnts, -1, (255, 255, 255), thickness=cv2.FILLED
    )

    imLabel = label(temp)

    for region in regionprops(imLabel):

        if region.area < minRegionArea:
            # check it is inside or outside

            temp[imLabel == region.label] = 0
            # region given same value as sph. border

        if region.area > maxRegionArea:
            # check it is inside or outside

            temp[imLabel == region.label] = 0
            # region given same value as sph. border

        if region.eccentricity > 0.7:
            # check it is inside or outside

            temp[imLabel == region.label] = 0
            # region given same value as sph. border

    return temp
