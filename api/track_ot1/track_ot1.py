import os
import numpy as np

import trackpy
import pims
import pandas
from tqdm import tqdm

from api.segment import segment
from api.analyse import analyse
from api.segment import verify_segmentation
import api.segment.utilities as utilities


def make_tracks(track_frame:pandas.DataFrame,
    search_range:int):

    result_frame = pandas.DataFrame()

    for m in track_frame['m'].unique():

        result_frame = result_frame.append(trackpy.link(track_frame[track_frame['m'] == m],
            search_range = search_range))
    
    return result_frame

def get_cell_tracks(vs,
        fluo_channel:int,
        mutopx:int,
        search_range:int,
        minsize:int,
        minmass:int,
        percentile:float):

    """
    
    Takes a VirtualStack as entry and returns the cell tracks.

    Returns:
     - pandas.DataFrame
    
    """

    min_size = (2*mutopx*minsize//2)+1
    track_frame = pandas.DataFrame()

    c2_time_reader = vs.read(t = None, 
        m = None, 
        c = fluo_channel)

    for img in tqdm(c2_time_reader):

        t = img.meta['t']
        m = img.meta['m']
        
        # the parameter values returned by vs.ranges is a str
        # but the input of vs.read is an int.
        well_frame = trackpy.locate(img.array, 
            min_size, 
            minmass=minmass,
            percentile = percentile)

        well_frame['m'] = m
        well_frame['frame'] = t

        track_frame = track_frame.append(well_frame)

    return make_tracks(track_frame, search_range)