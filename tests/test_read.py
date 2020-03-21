import os
import numpy as np
from api import read, Well
from tifffile import imwrite
from glob import glob


def create_test_data(prefix):
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    for m in range(1):
        for t in range(11):
            for z in range(1):
                for c in range(1):
                    fname = f'm{m:02d}t{t:03d}z{z:02d}c{c}.tif'
                    path = os.path.join(prefix, fname)
                    if not os.path.exists(path):
                        arr = np.random.randint(0,255,(8,8), 'uint16')
                        imwrite(path, arr)


def demolish_data(prefix):
    for f in glob(os.path.join(prefix, '*')):
        os.remove(f)
    os.rmdir(prefix)


def test_virtual_stack(prefix='tests/tmp'):

    create_test_data(prefix)

    vs = read.VirtualStack(prefix)

    assert vs.order == 'mtzc'
    assert tuple(vs.ranges['m'].values()) == (0,0)
    assert tuple(vs.ranges['t'].values()) == (0,10)
    assert tuple(vs.ranges['z'].values()) == (0,0)
    assert tuple(vs.ranges['c'].values()) == (0,0)

    img = vs.get_single_image(m=0, t=0, z=0, c=0)
    assert img.array.shape == (8,8)

    print(img.meta)

    assert img.meta['path'] == 'm00t000z00c0.tif'
    assert img.meta['t'] == 0
    assert img.meta['m'] == 0
    assert img.meta['z'] == 0
    assert img.meta['c'] == 0

    reader = vs.read(t=None, m=0, z=0, c=0)
    stack = []
    for img in reader:
        stack.append(img)

    assert len(stack) == 11
    assert isinstance(stack[0], Well)

    assert Well.stack(stack).array.shape == (11, 8, 8)

    assert stack[0].bin(2).array.shape == (4,4)

    demolish_data(prefix)
