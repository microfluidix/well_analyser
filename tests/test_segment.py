from api.segment import utilities
import numpy as np

def test_well():
    shape = (20,20)
    arr = np.zeros(shape)

    arr[5:15, 10:20] = utilities._make_circ_mask(10, 10, 1)

    #assert well.shape == shape
    #assert well.meta['shape'] == shape
    #assert well.ndim == len(shape)