import os
import numpy as np

import trackpy
import pims
import pandas

from api.segment import segment
from api.analyse import analyse
from api.segment import verify_segmentation
import api.segment.utilities as utilities


def make_tracks(track_frame:pandas.DataFrame):

    for m in track_frame['m'].unique():

        track_frame.loc[track_frame['m'] == m] = trackpy.link(track_frame[track_frame['m'] == m],
            search_range = 40)
    
    return track_frame

def get_cell_tracks(vs,
    fluo_channel:int,
    muTopx = 3,
    search_range = 40,
    minsize = 10,
    minmass = 10000,
    percentile = 90):

    """
    
    Takes a VirtualStack as entry and returns the cell tracks.

    Returns:
     - pandas.DataFrame
    
    """

    min_size = (2*muTopx*minsize//2)+1
    track_frame = pandas.DataFrame()

    c2_time_reader = vs.read(t = None, 
        m = None, 
        c = fluo_channel)

    for img in c2_time_reader:

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

    return make_tracks(track_frame)

def get_spheroid_properties(vs,
    spheroid_channel:int,
    fluo_channel = None,
    get_fluo = False,
    verify_seg = False,
    wellSizeMu = 430,
    muTopx = 3):

    """
    
    extracts spheroid properties from image batch.

    COMMENT: with meta data we will integrate the above
    variables implicitely.

    Returns:
     - pandas.DataFrame
    
    """

    spheroid_frame = pandas.DataFrame()

    c1_time_reader = vs.read(t = None, 
        m = None, 
        c = spheroid_channel)

    for img in c1_time_reader:

        try:

            print(img.meta)
            
            t = img.meta['t']
            m = img.meta['m']

            (xc, yc) = utilities._get_center(img.array,wellSizeMu,wellSizeMu,muTopx)

            # function to be changed to Andrey's version
            crop_img_BF = segment.select_well(img.array, img.array, wellSizeMu, wellSizeMu, muTopx)            
            sph_img = segment.find_spheroid(crop_img_BF, wellSizeMu, muTopx)

            if get_fluo:

                img_Fluo = vs.get_single_image(m=m, t=t, c=fluo_channel)

                crop_img_Fluo = segment.select_well(img.array, 
                    img_Fluo.array, wellSizeMu, wellSizeMu, muTopx)

                timeFrame = analyse.spheroid_properties(sph_img, crop_img_Fluo)
            
            else:
                
                timeFrame = analyse.spheroid_properties(sph_img)
            
            
            timeFrame['t'] = int(t)
            timeFrame['m'] = int(m)
            timeFrame['well_center_x'] = xc
            timeFrame['well_center_y'] = yc
            timeFrame['mask_size'] = wellSizeMu*muTopx

            folder = vs.folder

            if not os.path.exists(os.path.join(folder, 'spheroid_data_frame')):
                os.makedirs(os.path.join(folder, 'spheroid_data_frame'))

            timeFrame.to_csv(os.path.join(os.path.join(folder, 
                'spheroid_data_frame',
                str(m) + '_' + str(t))))
            
            spheroid_frame = spheroid_frame.append(timeFrame)

            # Verify segmentation

            if verify_seg:

                folder = vs.folder

                if not os.path.exists(os.path.join(folder, 'verify segmentation')):
                    os.makedirs(os.path.join(folder, 'verify segmentation'))

                verify_segmentation.verifySegmentationBF(crop_img_BF,
                    sph_img,
                    os.path.join(folder, 'verify segmentation'),
                    int(m),
                    int(t))

        except Exception as e: print(e)

    return spheroid_frame