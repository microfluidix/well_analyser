import logging
import os

import numpy as np
from api.core import Well
from api.read.interface import ReaderInterface
from pims_nd2 import ND2_Reader as reader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

EXAMPLE = """

"""


class ND2Reader(ReaderInterface):

    """
    pims_nd2 wrapper to get Well objects

    Example:
    --------
    >>> from api.read import nd2_stack
    >>> r = nd2_stack.ND2Reader('D2001.nd2')
    >>> r
        nd2 dataset from `/Volumes/Multicell/Gustave/13092019/TL_MigrationCD810pcMatrigel/D2001.nd2`,
            ranges: {'x': 2048, 'y': 2044, 'c': 2, 'm': 12},
            channels: ['FITC', 'DaFiTr']
            pixel size: 0.325 um
    >>> r.channels
        ['FITC', 'DaFiTr']
    >>> single_image = r.get_single_image(c=0, m=0)
    >>> single_image
        array (2044, 2048), {'x_um': -26555.7, 'y_um': -2942.4, 'z_um': 3691.9,
        't_ms': 1446.9611667967401, 'colors': [(0.0, 1.0, 0.0), (1.0, 1.0, 1.0)],
        'mpp': 0.325, 'max_value': 65535, 'x': 0, 'y': 0, 'c': 0, 'm': 0,
        'axes': ['y', 'x'], 'coords': {'m': 0, 'c': 0}}
    >>> single_image.array
        array([[173, 155, 183, ..., 126, 131, 125],
            [174, 153, 163, ..., 112, 129, 126],
            [168, 179, 169, ..., 125, 135, 119],
            ...,
            [135, 136, 134, ..., 142, 122, 123],
            [130, 135, 128, ..., 129, 129, 119],
            [144, 131, 131, ..., 124, 116, 127]], dtype=uint16)
    >>> mm = r.read(bin=10, c=1)
    >>> for m in mm:
    >>>     print(m.shape,m.meta['m'], m.meta['c'])
        (205, 205) 0 1
        (205, 205) 1 1
        (205, 205) 2 1
        (205, 205) 3 1
        (205, 205) 4 1
        (205, 205) 5 1
        (205, 205) 6 1
        (205, 205) 7 1
        (205, 205) 8 1
        (205, 205) 9 1
        (205, 205) 10 1
        (205, 205) 11 1
    >>> m
        array (205, 205),
        {'binning': 10, 'x_um': -15416.2, 'y_um': 5327.700000000001,
        'z_um': 3691.9, 't_ms': 23359.35130351549,
        'colors': [(0.0, 1.0, 0.0), (1.0, 1.0, 1.0)],
        'mpp': 0.325, 'max_value': 65535,
        'x': 0, 'y': 0, 'c': 1, 'm': 11,
        'axes': ['y', 'x'], 'coords': {'m': 11, 'c': 1},
        'channel': 'DaFiTr'}
    >>> m.array
        array([[1166.67, 1155.1 , 1165.44, ..., 1251.21, 1223.05,  952.66],
            [1158.88, 1167.49, 1166.63, ..., 1201.28, 1185.37,  927.92],
            [1158.49, 1161.95, 1167.47, ..., 1158.68, 1155.93,  947.83],
            ...,
            [1052.04, 1092.88, 1316.46, ..., 1237.19, 1245.07,  977.19],
            [1126.38, 1124.62, 1259.61, ..., 1231.87, 1254.46,  992.66],
            [ 467.3 ,  528.08,  474.7 , ...,  502.25,  515.58,  394.93]])

    """

    def __init__(self, path: str):
        assert os.path.exists(path), f"path {path} doesn't exist"
        self.path = path
        self.reader = reader(path)
        self.metadata = (met := self.reader.metadata)
        self.ranges = self.reader.sizes
        self.channels = [met[f"plane_{i}"]["name"] for i in range(met["plane_count"])]
        self.pixel_size_um = met["calibration_um"]

    def get_single_image(self, **kwargs) -> Well:
        """
        Read single 2D array

        Specify coordianates, get Well object
        """
        self._check_range(**kwargs)
        for k, v in kwargs.items():
            self.reader.default_coords[k] = v
        return Well(array=np.array(r := self.reader[0]), meta=r.metadata)

    def read(self, bin=0, **kwargs):
        """
        Get generator of Well objects

        if no coordinates specified: iterated over all coordinates
        (see .meta for particular values)
        if one or several coordinates specified: iterates over the rest.

        :param bin: int, applies binning if greater than 1.

        Return:
        -------
        api.core.Well object
        """

        self._check_range(**kwargs)
        r = self.reader
        axes = list(self.ranges)
        axes.remove("x")
        axes.remove("y")
        for k, v in kwargs.items():
            if isinstance(v, int):
                r.default_coords[k] = v
                axes.remove(k)
        if len(axes):
            r.iter_axes = (itax := "".join(axes))
            logger.debug(f"iterate over {itax}")
        logger.debug(f"list of {(ll := len(r))} frames")
        for i, frame in enumerate(r):
            w = Well(
                array=np.array(frame),
                meta={**(met := frame.metadata), "channel": self.channels[met["c"]]},
            )
            if bin > 1:
                w = w.bin(bin)
                logger.debug(f"bin {bin}")
            logger.debug(f"yield {i}/{ll}")
            yield w

    def _check_range(self, **kwargs: dict):
        assert all(
            [k in self.ranges] for k in kwargs
        ), f"Must provide all the coordiantes from {self.ranges}, got {kwargs}"
        assert all(
            [0 <= kwargs[k] < self.ranges[k] for k in kwargs]
        ), f"{kwargs} is out of range. Max values: {self.ranges}"

    def __getitem__(self, value):
        logger.debug(f"__getitem__({value})")
        return Well(array=np.array(im := self.reader[value]), meta=im.metadata)

    def __repr__(self):
        return f"""nd2 dataset from `{self.path}`,
        ranges: {self.ranges},
        channels: {self.channels}
        pixel size: {self.pixel_size_um} um"""
