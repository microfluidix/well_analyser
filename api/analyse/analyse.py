import os
import sys
import numpy as np

from numpy import unravel_index
from scipy import ndimage, misc
from skimage.measure import label, regionprops

def spheroid_properties(img_labeled,
    img_intensity = None):

    """

    Retrieve spheroid shape properties. If img_intensity is 
    non-empty, then we can extract the average intensity.
    
    Returns:
     - dict

    """

    spheroid_props = {}

    im_label = label(img_labeled)

    for region in regionprops(im_label):

        dic = {}

        dic['ecc'] = region.eccentricity
        dic['perimenter'] = region.perimeter
        dic['area'] = region.area
        dic['orientation'] = region.orientation
        dic['major_axis_length'] = region.major_axis_length
        dic['minor_axis_length'] = region.minor_axis_length

        if img_intensity != None:
            dic['intensity'] = region.mean_intensity

        spheroid_props[region.label] = dic

    return spheroid_props