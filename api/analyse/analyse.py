import os
import sys
import numpy as np

from numpy import unravel_index
from scipy import ndimage, misc
from skimage.measure import label, regionprops

def spheroid_properties(img_labeled:np.ndarray(int),
    img_intensity:np.ndarray(int) = None):

    """

    Retrieve spheroid shape properties. If img_intensity is 
    non-empty, then we can extract the average intensity.
    
    Returns:
     - dict

    """

    spheroid_props = {}

    im_label = label(img_labeled, img_intensity)

    for region in regionprops(im_label):

        spheroid_props['spheroid label'] = region.label

        spheroid_props['spheroid label']['ecc'] = region.eccentricity
        spheroid_props['spheroid label']['perimenter'] = region.perimeter
        spheroid_props['spheroid label']['area'] = region.area
        spheroid_props['spheroid label']['orientation'] = region.orientation
        spheroid_props['spheroid label']['major_axis_length'] = region.major_axis_length
        spheroid_props['spheroid label']['minor_axis_length'] = region.minor_axis_length

        if img_intensity != None:
            spheroid_props['spheroid label']['intensity'] = region.mean_intensity

    return spheroid_props