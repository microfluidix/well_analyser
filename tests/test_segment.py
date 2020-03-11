from api import segment
import numpy as np

def test_well():
    shape = (20,20)
    arr = np.zeros(shape)

    arr[5:15, 10:20] = segment.utilities._makeDiskMask(10, 10, 1)

    print(arr)


    #assert well.shape == shape
    #assert well.meta['shape'] == shape
    #assert well.ndim == len(shape)