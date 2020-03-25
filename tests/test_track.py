
import os
import numpy as np
from api import read, Well
from tifffile import imwrite
from glob import glob

import pandas
from api import track

def create_test_data(prefix):
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    for m in range(2):
        for t in range(11):
            for z in range(1):
                for c in range(1):
                    fname = f'm{m:02d}t{t:03d}z{z:02d}c{c}.tif'
                    path = os.path.join(prefix, fname)
                    if not os.path.exists(path):
                        arr = np.zeros((200,200), 'uint16')
                        arr[100:105, 50:55] = 1000
                        imwrite(path, arr)

def demolish_data(prefix):
    for f in glob(os.path.join(prefix, '*')):
        os.remove(f)
    os.rmdir(prefix)


def test_virtual_stack(prefix='tests/tmp'):

    create_test_data(prefix)

    vs = read.VirtualStack(prefix)

    track_frame = track.get_cell_tracks(vs, fluo_channel = 0)

    print(track_frame['m'].unique())

    assert isinstance(track_frame, pandas.DataFrame)
    assert len(track_frame) == 22

    demolish_data(prefix)


if __name__ == "__main__":
    test_virtual_stack()