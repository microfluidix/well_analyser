import pandas
import os
import numpy as np
from glob import glob
from tifffile import imread, imwrite

from api.segment import segment
from api import read


def demolish_data(prefix):
    for f in glob(os.path.join(prefix, '*')):
        os.remove(f)
    os.rmdir(prefix)


def create_test_data_sph(prefix):
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    for m in range(1):
        for t in range(2):
            for z in range(1):
                for c in range(1):
                    fname = f'm{m:02d}t{t:03d}z{z:02d}c{c}.tif'
                    path = os.path.join(prefix, fname)
                    if not os.path.exists(path):

                        # make circle

                        X = np.arange(2000)
                        Y = X

                        X, Y = np.meshgrid(X, Y)

                        mask = ((np.sqrt((X-600)**2 + (Y-1200)**2) > 200) & 
                                (np.sqrt((X-600)**2 + (Y-1200)**2) < 210)).astype('int32')

                        mask[650:700, 1200:1250] = -100
                        mask *= -1

                        imwrite(path, mask)


def test_crop():
    shape = (20, 20)
    arr = np.zeros(shape, dtype="int64")
    bool_arr = np.zeros(shape)

    bool_arr[1:6, 11:16] = 1
    bool_arr = bool_arr.astype(bool)

    cropped_arr = segment.crop(arr, bool_arr)

    assert cropped_arr.shape == (5, 5)
    assert cropped_arr.dtype == "int64"



def test_find_well(prefix='tests/tmp_sph'):

    create_test_data_sph(prefix)

    vs = read.VirtualStack(prefix)

    img = vs.get_single_image(m=0, t=0, z = 0, c=0).array

    crop_img = segment.select_well(img, 
        img, 
        maskSizeUm = 410, 
        wellDiameterUm = 410, 
        mutopx = 1)

    sph_img = segment.find_spheroid(crop_img,
        wellDiameterUm = 410,
        marginDistance = 10,
        minRegionArea = 100,
        mutopx = 1)

    assert isinstance(sph_img, np.ndarray)
    assert np.shape(sph_img) == (410,410)

    demolish_data(prefix)



if __name__ == "__main__":
    _test_crop()
