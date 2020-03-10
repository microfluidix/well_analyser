from api import core
import numpy as np

def test_well():
    shape = (4,4)
    arr = np.zeros(shape)
    well = core.Well(arr, meta={'name': 'test array', 'shape': shape})
    assert well.shape == shape
    assert well.meta['shape'] == shape
    assert well.ndim == len(shape)