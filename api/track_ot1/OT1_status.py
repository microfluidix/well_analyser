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

    spheroid_positions = spheroid_positions.sort_values("area")

    x = spheroid_positions["centroid-1"].iloc[0]
    y = spheroid_positions["centroid-0"].iloc[0]
    R = np.sqrt(spheroid_positions["area"] / np.pi).iloc[0]

    state = (well_frame["x"] - x) ** 2 + (well_frame["y"] - y) ** 2 < (radius + R) ** 2

    well_frame["state_radius"] = state
    well_frame["spheroid_center_x"] = x
    well_frame["spheroid_center_y"] = y
    well_frame["spheroid_radius"] = R

    return well_frame
