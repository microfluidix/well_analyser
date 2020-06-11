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
    for m in range(3):
        for t in range(2):
            for c in range(2):
                fname = f"c{c}t{t:03d}m{m:02d}.tif"
                path = os.path.join(prefix, fname)
                if not os.path.exists(path):

                    if c == 1:
                        arr = np.zeros((2000, 2000), "uint16")
                        arr[100:105, 50:55] = 1000

                        print(np.unique(arr))
                        imwrite(path, arr)

                    if c == 0:
                        # make circle

                        X = np.arange(2000)
                        Y = X

                        X, Y = np.meshgrid(X, Y)

                        mask = -50*(
                            (np.sqrt((X - 600) ** 2 + (Y - 1200) ** 2) > 200)
                            & (np.sqrt((X - 600) ** 2 + (Y - 1200) ** 2) < 210)
                        ).astype("int32")

                        mask[600:760, 1000:1310] = -100
                        mask += 150

                        imwrite(path, mask)

def demolish_data(prefix):
    for f in glob(os.path.join(prefix, "*")):
        os.remove(f)
    os.rmdir(prefix)

def test_track_cells_OT1(prefix="tests/tmp_cells"):

    create_test_data(prefix)

    vs = read.VirtualStack(prefix)

    track_frame = track_ot1.get_cell_tracks_state(
        vs,
        fluo_channel=1,
        fluo_BF = 0,
        mutopx=1,
        search_range=10,
        minsize=10,
        minmass=10,
        percentile=50.0,
        verify_seg=True,
        radius=10,
        wellSizeMu=410
    )

    assert isinstance(track_frame, pandas.DataFrame)

    demolish_data(prefix)

if __name__ == "__main__":
    test_track_cells_OT1()