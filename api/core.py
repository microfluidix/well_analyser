import numpy as np

class Well:

    def __init__(
        self,
        array:np.ndarray,
        meta:dict
    ):
        self.array = array
        self.ndim = array.ndim
        self.shape = array.shape

