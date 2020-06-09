import os
import numpy as np
from api import read
from tifffile import imwrite
from glob import glob

import pandas

from api.track_ot1 import track_ot1
from api.track_spheroids import track_spheroids
from api.segment import segment


def create_test_data(prefix):
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    for m in range(2):
        for t in range(11):
            for z in range(1):
                for c in range(1):
                    fname = f"m{m:02d}t{t:03d}z{z:02d}c{c}.tif"
                    path = os.path.join(prefix, fname)
                    if not os.path.exists(path):
                        arr = np.zeros((200, 200), "uint16")
                        arr[100:105, 50:55] = 1000
                        imwrite(path, arr)


def create_test_data_sph(prefix):
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    for m in range(1):
        for t in range(5):
            for z in range(1):
                for c in range(1):
                    fname = f"m{m:02d}t{t:03d}z{z:02d}c{c}.tif"
                    path = os.path.join(prefix, fname)
                    if not os.path.exists(path):

                        # make circle

                        X = np.arange(2000)
                        Y = X

                        X, Y = np.meshgrid(X, Y)

                        mask = (
                            (np.sqrt((X - 600) ** 2 + (Y - 1200) ** 2) > 200)
                            & (np.sqrt((X - 600) ** 2 + (Y - 1200) ** 2) < 210)
                        ).astype("int32")

                        mask[650:760, 1200:1310] = -100
                        mask *= -1

                        imwrite(path, mask)


def demolish_data(prefix):
    for f in glob(os.path.join(prefix, "*")):
        os.remove(f)
    os.rmdir(prefix)


def demolish_data_sph(prefix):
    import shutil

    shutil.rmtree(os.path.join(prefix, "spheroid_data_frame"))


def test_track_cells(prefix="tests/tmp_cells"):

    create_test_data(prefix)

    vs = read.VirtualStack(prefix)

    track_frame = track_ot1.get_cell_tracks(
        vs,
        fluo_channel=0,
        mutopx=1,
        search_range=10,
        minsize=10,
        minmass=10,
        percentile=50.0,
    )

    print(track_frame["m"].unique())

    assert isinstance(track_frame, pandas.DataFrame)

    demolish_data(prefix)


def test_find_well(prefix="tests/tmp_sph"):

    create_test_data_sph(prefix)

    vs = read.VirtualStack(prefix)

    img = vs.get_single_image(m=0, t=0, z=0, c=0).array

    crop_img = segment.select_well(
        img, img, maskSizeUm=410, wellDiameterUm=410, mutopx=1
    )

    sph_img = segment.find_spheroid(
        crop_img, wellDiameterUm=410, marginDistance=10, mutopx=1
    )

    assert isinstance(sph_img, np.ndarray)
    assert np.shape(sph_img) == (410, 410)
    # assert np.max(sph_img) > 0

    demolish_data(prefix)


def test_spheroid_props(prefix="tests/tmp_sph"):

    create_test_data_sph(prefix)

    vs = read.VirtualStack(prefix)

    track_frame = track_spheroids.get_spheroid_properties(
        vs, spheroid_channel=0, wellSizeMu=410, mutopx=1
    )

    assert isinstance(track_frame, pandas.DataFrame)

    # print(len(track_frame))
    # assert len(track_frame) == 22

    demolish_data_sph(prefix)
    demolish_data(prefix)


if __name__ == "__main__":
    test_track_cells()
    test_find_well()
    #### test_spheroid_props()
