import os
import sys
import numpy as np
import pandas

from skimage.measure import label, regionprops_table

def spheroid_properties(img_labeled,
    img_intensity):

    """

    Retrieve spheroid shape properties. If img_intensity is 
    non-empty, then we can extract the average intensity.
    
    Returns:
     - pandas DataFrame

    """

    properties = ['label', 
        'area', 
        'perimeter',
        'eccentricity',
        'orientation',
        'major_axis_length',
        'mean_intensity']

    im_label = label(img_labeled)

    return pandas.DataFrame(regionprops_table(im_label, img_intensity, properties))