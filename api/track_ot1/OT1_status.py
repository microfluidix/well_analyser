import os
import numpy as np

from skimage.measure import label, regionprops
from api.analyse import analyse

import pandas


def get_state(well_frame: pandas.DataFrame, 
    radius: int, 
    spheroid_mask: np.ndarray
):

    """
    
    Get the state of the OT1 cells (contact/no contact)
    as a function of the distance to border of the sph.

    This is approximated by the radius of the equivalent
    disk.

    Returns:
     - pandas.DataFrame
    
    """

    spheroid_positions = analyse.spheroid_properties(spheroid_mask, img_intensity=None)

    if len(spheroid_positions) == 0:

        well_frame["state"] = 0
        well_frame["spheroid_center_x"] = 0
        well_frame["spheroid_center_y"] = 0
        well_frame["spheroid_radius"] = 0

        return well_frame

    idxmax = spheroid_positions['area'].idxmax()

    x = spheroid_positions.loc[idxmax, "centroid-1"]
    y = spheroid_positions.loc[idxmax, "centroid-0"]
    R = np.sqrt(spheroid_positions.loc[idxmax, "area"] / np.pi)

    state = (well_frame["x"] - x) ** 2 + (well_frame["y"] - y) ** 2 < (radius + R) ** 2

    well_frame["state"] = state
    well_frame["spheroid_center_x"] = x
    well_frame["spheroid_center_y"] = y
    well_frame["spheroid_radius"] = R

    return well_frame
