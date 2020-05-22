import os
import numpy as np

from skimage.measure import label, regionprops
from api.analyse import analyse

import pandas
from tqdm import tqdm

def get_state(well_frame:pandas.DataFrame,
              radius:int,
              spheroid_mask:np.ndarray):

    """
    
    Get the state of the OT1 cells (contact/no contact)
    as a function of the distance to border of the sph.

    This is approximated by the radius of the equivalent
    disk.

    Returns:
     - pandas.DataFrame
    
    """

    spheroid_positions = analyse.spheroid_properties(spheroid_mask, 
                                             img_intensity=None)

    spheroid_positions = spheroid_positions.sort_values('area')

    x = spheroid_positions['centroid-0'].iloc[0]
    y = spheroid_positions['centroid-1'].iloc[0]
    R = np.sqrt(spheroid_positions['area']/np.pi)

    well_frame['state'] = ((well_frame['x'] - x)**2 + (well_frame['y'] - y)**2 < (radius + R)**2).astype(int)
    well_frame['spheroid_center_x'] = x
    well_frame['spheroid_center_y'] = y
    well_frame['spheroid_radius'] = R

    return well_frame