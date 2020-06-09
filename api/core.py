import logging

import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import downscale_local_mean

logging.getLogger("matplotlib").setLevel(logging.WARNING)


class Well:
    def __init__(self, array: np.ndarray, meta: dict):
        self.array = array
        self.ndim = array.ndim
        self.shape = array.shape
        self.meta = meta

    @classmethod
    def stack(self, list_of_wells):
        """
        Makes a stack from 1D list of wells
        """
        arr = np.stack([w.array for w in list_of_wells])
        try:
            meta = {
                k: {w.meta[k] for w in list_of_wells} for k in list_of_wells[0].meta
            }
        except TypeError:
            meta = {
                k: [w.meta[k] for w in list_of_wells] for k in list_of_wells[0].meta
            }

        return Well(arr, {**meta, "stacked": len(list_of_wells)})

    def bin(self, factor):
        """bin xy `factor` times"""
        factors = np.ones_like(self.array.shape)
        factors[-2:] = factor
        arr = downscale_local_mean(self.array, tuple(factors))
        return Well(arr, meta={"binning": factor, **self.meta})

    def show(self):
        plt.imshow(self.array)

    def __repr__(self,):
        try:
            if self.array.ndim == 2:
                plt.imshow(self.array, cmap="gray")
                # plt.title(self.meta)
            elif self.array.ndim == 3:
                plt.imshow(self.array[0], cmap="gray")
                # plt.title(self.meta)
                print("Showing first layer")
            else:
                pass

        except Exception:
            pass
        finally:
            return f"array {self.array.shape}, {self.meta}"
