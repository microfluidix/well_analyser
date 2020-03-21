import os
import numpy as np

import trackpy
import pandas

from api.segment import segment
from api.analyse import analyse


def get_image_array(VirtualStack, 
    m, 
    c):
    
    c2_time_reader = VirtualStack.read(t = None, m = m, c = c)
    
    return [img.array for img in c2_time_reader]

def get_spheroid_properties(VirtualStack,
    m:int,
    spheroid_channel:int):

    """"""

    spheroid_frame = pandas.DataFrame()

    c1_time_reader = VirtualStack.read(t = None, 
        m = m, 
        c = spheroid_channel)

    for img in c1_time_reader:
        
        t = img.meta['t']
        m = img.meta['m']
        
        crop_img_BF = segment.select_well(img.array, img.array, 430, 430, 3)            
        sph_img = segment.find_spheroid(crop_img_BF, 430, 3)
        
        timeFrame = analyse.spheroid_properties(sph_img)
        timeFrame['t'] = t
        timeFrame['m'] = m
        
        spheroid_frame = spheroid_frame.append(timeFrame)

    return spheroid_frame

def get_cell_tracks(img_list:np.ndarray,
    muTopx = 3,
    minsize = 10,
    minmass = 10000):

    min_size = muTopx*minsize

    return trackpy.batch(img_list, min_size, minmass=minmass)