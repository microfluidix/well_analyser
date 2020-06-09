import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas
from api.analyse import analyse
from api.segment import segment
from pandas._testing import assert_frame_equal
from PIL import Image
from tifffile import imread


def test_analyse():

    img = np.zeros((20, 20))
    img[5:10, 10:15] = 1

    props = analyse.spheroid_properties(img)
    ground_truth_frame = pandas.DataFrame(
        [[1, 25, 7, 12, 16.0, 0.0, 0.785398, 5.656854]],
        columns=[
            "label",
            "area",
            "centroid-0",
            "centroid-1",
            "perimeter",
            "eccentricity",
            "orientation",
            "major_axis_length",
        ],
    )

    assert_frame_equal(props, ground_truth_frame)


def test_find_single_cells():

    img = np.zeros((20, 20))
    img[5:8, 10:13] = 10
    diameter = 7
    minmass = 1

    props = analyse.find_single_cells(img, diameter, minmass)
    ground_truth_frame = pandas.DataFrame(
        [[6.0, 11.0, 40.07147, 1.254729, 0.174658, 5.958149, 90.0, 0.0]],
        columns=["y", "x", "mass", "size", "ecc", "signal", "raw_mass", "ep"],
    )

    assert_frame_equal(props, ground_truth_frame)


def _test_analyse_functional():

    for fileName in glob.glob("*.tif"):

        im = imread(fileName)
        im_crop = segment.select_well(im, 410, 410, 3)
        im_sph = segment.find_spheroid(im_crop, 410, 40, 3)

        props = analyse.spheroid_properties(im_sph, im_crop)
        props.to_csv("test_properties.csv")

    return


if __name__ == "__main__":
    test_analyse()
    test_find_single_cells()
