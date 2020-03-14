from api.analyse import analyse
from api.segment import segment

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
from tifffile import imread


def _test_analyse():

    for fileName in glob.glob('*.tif'):

        im = imread(fileName)
        im_crop = segment.select_well(im, 410, 410, 3)
        im_sph = segment.find_spheroid(im_crop, 410, 40, 3)

        print(np.shape(im_sph))

        props = analyse.spheroid_properties(im_sph, im_crop)

    return


if __name__ == "__main__":
    _test_analyse()