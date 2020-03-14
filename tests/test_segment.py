from api.segment import utilities
from api.segment import segment

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
from tifffile import imread

def test_well():
    shape = (20,20)
    arr = np.zeros(shape)

    arr[5:15, 10:20] = utilities._make_circ_mask(10, 10, 1)

    #assert well.shape == shape
    #assert well.meta['shape'] == shape
    #assert well.ndim == len(shape)

def _test_crop():

    for fileName in glob.glob('*.tif'):

        im = imread(fileName)
        im_crop = segment.select_well(im, 410, 410, 3)
        im_sph = segment.find_spheroid(im_crop, 410, 40, 3)

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
    _test_crop()