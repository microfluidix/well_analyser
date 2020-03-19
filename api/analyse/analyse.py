import os
import sys
import numpy as np
import pandas
import trackpy

from skimage.measure import label, regionprops_table

def spheroid_properties(img_labeled,
    img_intensity = None):

    """

    Retrieve spheroid shape properties. If img_intensity is 
    non-empty, then we can extract the average intensity.
    
    Returns:
     - pandas DataFrame

    """

    if img_intensity is not None:

        properties = ['label', 
            'area',
            'centroid',
            'perimeter',
            'eccentricity',
            'orientation',
            'major_axis_length',
            'mean_intensity']

    else:
        properties = ['label', 
            'area',
            'centroid',
            'perimeter',
            'eccentricity',
            'orientation',
            'major_axis_length']

    im_label = label(img_labeled)

    return pandas.DataFrame(regionprops_table(im_label, img_intensity, properties))

def find_single_cells(img_fluo:np.ndarray,
    diameter:int,
    minmass:int):

    """

    Trackpy locate module implementation.

    Returns:
     - pandas.DataFrame object
    
    """

    return trackpy.locate(img_fluo, diameter = diameter, minmass = minmass)