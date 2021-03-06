import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pims
from numpy import unravel_index
from scipy import misc
from scipy import ndimage
from scipy.ndimage import gaussian_filter
from skimage.measure import label
from skimage.measure import regionprops


def _make_circ_mask(maskSize: int, wellSize: int, mutopx: float):

    """

    Makes a donut mask for future convolution.

    Returns:
    - np.ndarray

    """

    cropDist = maskSize * mutopx

    X = np.arange(cropDist)
    Y = X

    X, Y = np.meshgrid(X, Y)

    mask = (
        np.sqrt((X - cropDist // 2) ** 2 + (Y - cropDist // 2) ** 2)
        > (wellSize * mutopx) // 2 - 10 * mutopx
    ) & (
        np.sqrt((X - cropDist // 2) ** 2 + (Y - cropDist // 2) ** 2)
        < (wellSize * mutopx) // 2 + 10 * mutopx
    )

    return mask.astype(np.int)


def _get_center(imgToAnalyze: np.ndarray, maskSize: int, wellSize: int, mutopx: float):

    """

    Find the well center of an image.

    Returns:
    - tuple

    """

    mask = _make_circ_mask(maskSize, wellSize, mutopx)

    conv = cv2.filter2D(imgToAnalyze, cv2.CV_32F, mask)

    return unravel_index(conv.argmin(), conv.shape)


def _make_disk_mask(maskSize: int, diskSize: int, mutopx: float):

    """

    Makes a circular mask of given radius.

    Returns:
    - np.ndarray

    """

    cropDist = int(maskSize * mutopx)

    X = np.arange(cropDist)
    Y = X
    X, Y = np.meshgrid(X, Y)

    mask = (
        np.sqrt((X - cropDist // 2) ** 2 + (Y - cropDist // 2) ** 2)
        < (diskSize * mutopx) // 2
    )

    return mask.astype(np.int)
