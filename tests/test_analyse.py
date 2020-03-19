from api.analyse import analyse
from api.segment import segment

import numpy as np
import pandas
from PIL import Image
import matplotlib.pyplot as plt
import glob
from tifffile import imread

from pandas._testing import assert_frame_equal


def test_analyse():

    img = np.zeros((20,20))
    img[5:10, 10:15] = 1

    props = analyse.spheroid_properties(img)
    ground_truth_frame = pandas.DataFrame(
        [[1, 25, 7, 12, 16.0, 0.0, 0.785398, 5.656854]],
        columns = ['label', 'area', 'centroid-0', 'centroid-1',
        'perimeter', 'eccentricity', 'orientation', 
        'major_axis_length'])

    assert_frame_equal(props, ground_truth_frame)

def _test_analyse_functional():

    for fileName in glob.glob('*.tif'):

        im = imread(fileName)
        im_crop = segment.select_well(im, 410, 410, 3)
        im_sph = segment.find_spheroid(im_crop, 410, 40, 3)

        props = analyse.spheroid_properties(im_sph, im_crop)
        props.to_csv('test_properties.csv')

    return


if __name__ == "__main__":
    test_analyse()