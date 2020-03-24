from api.segment import utilities
from api.segment import segment

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
from tifffile import imread

def test_crop():
    shape = (20,20)
    arr = np.zeros(shape, dtype = 'int64')
    bool_arr = np.zeros(shape)

    bool_arr[1:6,11:16] = 1
    bool_arr = bool_arr.astype(bool)

    cropped_arr = segment.crop(arr, bool_arr)

    assert cropped_arr.shape == (5,5)
    assert cropped_arr.dtype == 'int64'

def _test_crop_functional():

    for fileName in glob.glob('*.tif'):

        im = imread(fileName)
        im_crop = segment.select_well(im, 410, 410, 3)
        im_sph = segment.find_spheroid(im_crop, 410, 3)

        fig, ax = plt.subplots(1,3)

        ax[0].imshow(im, origin = 'lower', cmap="gray")
        ax[0].set_title('Raw image')
        ax[1].imshow(im_crop, origin = 'lower', cmap="gray")
        ax[1].set_title('Cropped image')
        ax[2].imshow(im_crop, origin = 'lower', cmap="gray")
        ax[2].imshow(im_sph, origin = 'lower', alpha = 0.3)
        ax[2].set_title('Segmented spheroid image')

        plt.savefig('test_result.tiff')

    return


if __name__ == "__main__":
    test_crop()