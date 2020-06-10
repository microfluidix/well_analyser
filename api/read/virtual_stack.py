import os
import re
from glob import glob

import numpy as np
from api.core import Well
from api.read import interface
from skimage.transform import downscale_local_mean
from tifffile import imread


class VirtualStack(interface.ReaderInterface):

    """Handle tif exports from NIS"""

    def __init__(
        self,
        folder: str,
        search_names: str = "*.tif",
        regex: str = r"([ctmz])(\d{1,2})",
    ):
        self.folder = folder
        self.flist = glob(os.path.join(folder, search_names))
        assert len(self.flist) > 0, "No files found"
        self.indices = list(map(lambda p: get_indices(p, regex), self.flist))
        self.order = "".join(self.indices[0].keys())
        self.ranges = get_sizes(self.indices, self.order)

    def read(self, bin=0, **kwargs):
        """
        Get generator with a selected sequence

        Parameters:
        -----------
        t, int, tuple or None:
            time value or range
        z - the same
        c - the same
        Return:
        -------
        api.Well object
        Raise:
        ------
        ValueError if coordiantes are out of range
        """
        ranges = []
        for ax in self.order:
            if ax in kwargs:
                _range = kwargs[ax]
            else:
                _range = None
            ranges.append(self._check_range(_range, ax))

        params = [{}]
        for ax, _range in zip(self.order[-1::-1], ranges[-1::-1]):
            params = [{**p, ax: r} for r in _range for p in params]

        for param in params:
            img = self.get_single_image(**param)
            if bin > 1:
                img = img.bin(bin)
            yield img

    def get_single_image(self, **kwargs) -> Well:
        """reads .tif from disk, returns api.core.Well instance"""
        args = {ax: self._check_range(v, ax)[0] for ax, v in kwargs.items()}
        try:
            index = self.indices.index(args)
        except ValueError:
            raise ValueError(f"Can't find data for coordinates {args}")
        path = self.flist[index]
        if not os.path.exists(path):
            raise ValueError(f"File not found for coordinates {args}")
        fname = os.path.basename(path)
        return Well(imread(path), meta={**args, "path": fname, "prefix": self.folder})

    def _check_range(self, values: tuple, axis: str):
        """
        Check range values and generate range

        """

        def single_check(value, axis=axis, upper: bool = False):
            side = ["min", "max"][int(upper)]
            sr = self.ranges[axis]
            if value is None:
                return sr[side]
            assert isinstance(value, int)
            assert (
                sr["min"] <= value <= sr["max"]
            ), f"{value} out of range for {axis}: {sr}"
            return value

        if values is None:
            return range(
                single_check(None, upper=False), single_check(None, upper=True) + 1
            )

        elif isinstance(values, int):
            return (single_check(values),)

        elif isinstance(values, tuple):
            assert len(values) == 2
            return range(
                single_check(values[0], upper=False),
                single_check(values[1], upper=True) + 1,
            )
        else:
            raise ValueError(f"range {values} not understood, provide int or tuple")

    def __repr__(self):
        return f"Virtial Stack instance. \nFound {len(self.flist)} files in {self.folder}. \nRanges: {self.ranges}"


def get_indices(fname: str, regexp=r"([ctmz])(\d{1,2})") -> dict:
    """
    scans file name for regex and returns dict of values
    """
    r = re.compile(regexp)
    res = r.findall(fname)
    assert len(res) > 0, f"Nothing found in {fname} using regexp {regexp}"
    indices = {k: int(v) for k, v in res}
    return indices


def get_sizes(indices: dict, order="tzc"):
    """
    Returns min-max values for each dimension in the dict
    """
    tzc = np.array([[d[ax] for ax in order] for d in indices], dtype="uint8")
    _max = tzc.max(axis=0)
    _min = tzc.min(axis=0)
    ranges = {o: {"min": low, "max": high} for o, low, high in zip(order, _min, _max)}
    return ranges
