from api.segment import utilities
from api.segment import segment

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def test_well():
    shape = (20,20)
    arr = np.zeros(shape)

    arr[5:15, 10:20] = utilities._make_circ_mask(10, 10, 1)

    #assert well.shape == shape
    #assert well.meta['shape'] == shape
    #assert well.ndim == len(shape)

def _test_crop():

    for fileName in glob.glob('*.tif'):

        im = Image.open(fileName)
        imCrop = segment.well(im, 410, 410, 3)

        fig, ax = plt.subplots(1,2)

        ax[0].imshow(im)
        ax[1].imshow(imCrop)

        plt.savefig('test_result.tiff')

    return


if __name__ == "__main__":
    _test_crop()