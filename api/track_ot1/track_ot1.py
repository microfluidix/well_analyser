import os
import numpy as np

import trackpy
import pims
import pandas
from tqdm import tqdm
import csv

import collections

from api.segment import segment
from api.analyse import analyse
from api.segment import verify_segmentation
import api.segment.utilities as utilities

from api.track_ot1 import OT1_status


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


def get_cell_tracks_state(vs,
        fluo_channel:int,
        fluo_BF:int,
        mutopx:int,
        search_range:int,
        minsize:int,
        minmass:int,
        percentile:float,
        verify_seg:bool,
        radius:int,
        wellSizeMu:int):

    """
    
    Takes a VirtualStack as entry and returns the cell tracks
    marked wrt the position relative to the spheroid.

    Returns:
     - pandas.DataFrame
    
    """

    min_size = (2*mutopx*minsize//2)+1
    track_frame = pandas.DataFrame()

    error = collections.defaultdict(dict)
    folder = vs.folder

    c2_time_reader = vs.read(t = None, 
        m = None, 
        c = fluo_channel)

    for img in tqdm(c2_time_reader):

        t = img.meta['t']
        m = img.meta['m']

        try:

            img_BF = vs.get_single_image(m=m, t=t, c=fluo_BF)

            (xc, yc) = utilities._get_center(img_BF.array,
                                            wellSizeMu,
                                            wellSizeMu,
                                            mutopx)

            crop_img_BF = segment.select_well(img_BF.array, 
                                            img_BF.array, 
                                            wellSizeMu, 
                                            wellSizeMu,
                                            mutopx)

            crop_img_fluo = segment.select_well(img_BF.array, 
                                            img.array, 
                                            wellSizeMu, 
                                            wellSizeMu,
                                            mutopx)

            sph_img = segment.find_spheroid(crop_img_BF, 
                                            wellSizeMu, 
                                            mutopx)
            
            # the parameter values returned by vs.ranges is a str
            # but the input of vs.read is an int.
            well_frame = trackpy.locate(crop_img_fluo, 
                min_size, 
                minmass=minmass,
                percentile = percentile)

            well_frame = OT1_status.get_state(well_frame,
                                radius,
                                sph_img)

            if verify_seg:

                folder = vs.folder

                if not os.path.exists(os.path.join(folder, 'verify segmentation OT1')):
                    os.makedirs(os.path.join(folder, 'verify segmentation OT1'))

                verify_segmentation.verify_OT1_state(crop_img_BF,
                                                    well_frame,
                                                    folder,
                                                    m,
                                                    t)

            well_frame['m'] = m
            well_frame['frame'] = t

            well_frame['well_center_x'] = xc
            well_frame['well_center_y'] = yc

            track_frame = track_frame.append(well_frame)

        except Exception as e:

            error[m][t] = e

    with open(os.path.join(folder, 'error_message.csv','wb')) as f:
        w = csv.writer(f)
        w.writerows(error.items())

    return make_tracks(track_frame, search_range)