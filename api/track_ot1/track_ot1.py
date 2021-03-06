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
from api.segment import utilities as utilities

from api.track_ot1 import OT1_status

def make_tracks(track_frame: pandas.DataFrame, 
                search_range: int, 
                mutopx: int):

    result_frame = pandas.DataFrame()

    for m in track_frame["m"].unique():

        result_frame = result_frame.append(
            trackpy.link(track_frame[track_frame["m"] == m], search_range=search_range*mutopx)
        )

    return result_frame


def get_cell_tracks(
    vs,
    fluo_channel: int,
    mutopx: int,
    search_range: int,
    minsize: int,
    minmass: int,
    percentile: float,
):

    """
    
    Takes a VirtualStack as entry and returns the cell tracks.

    Returns:
     - pandas.DataFrame
    
    """

    min_size = (2 * mutopx * minsize)//2 + 1
    track_frame = pandas.DataFrame()
    folder = vs.folder

    c2_time_reader = vs.read(t=None, m=None, c=fluo_channel)

    for img in tqdm(c2_time_reader):

        t = img.meta["t"]
        m = img.meta["m"]

        # the parameter values returned by vs.ranges is a str
        # but the input of vs.read is an int.
        well_frame = trackpy.locate(
            img.array, min_size, minmass=minmass, percentile=percentile
        )

        well_frame["m"] = m
        well_frame["frame"] = t

        track_frame = track_frame.append(well_frame)

        if not os.path.exists(os.path.join(folder, "verify_segmentation_OT1")):
            os.makedirs(os.path.join(folder, "verify_segmentation_OT1"))

        folder = os.path.join(vs.folder, "verify_segmentation_OT1")

        verify_segmentation.verify_OT1_segmentation(
            img.array,  well_frame, folder, m, t
        )

    return make_tracks(track_frame, search_range, mutopx)


def get_cell_tracks_state(
    vs,
    fluo_channel: int,
    fluo_BF: int,
    mutopx: int,
    search_range: int,
    minsize: int,
    minmass: int,
    percentile: float,
    verify_seg: bool,
    radius: int,
    wellsizemu: int,
    out_dir,
    out_fname
):

    """
    
    Takes a VirtualStack as entry and returns the cell tracks
    marked wrt the position relative to the spheroid.

    Returns:
     - pandas.DataFrame
    
    """

    min_size = (2 * mutopx * minsize)//2 + 1
    track_frame = pandas.DataFrame()
    folder = os.path.dirname(vs.folder)
    #folder = vs.folder
    c2_time_reader = vs.read(t=None, m=None, c=fluo_channel)

    print(vs.ranges)

    for img in tqdm(c2_time_reader):

        t = img.meta["t"]
        m = img.meta["m"]

        well_frame = pandas.DataFrame()
        img_BF = vs.get_single_image(m=m, t=t, c=fluo_BF)


        (xc, yc) = utilities._get_center(
                        img_BF.array, wellsizemu, wellsizemu, mutopx
        )

        crop_img_BF = segment.select_well(
                    img_BF.array, img_BF.array, wellsizemu, wellsizemu, mutopx
        )

        crop_img_fluo = segment.select_well(
                    img_BF.array, img.array, wellsizemu, wellsizemu, mutopx
        )

        sph_img, sobelMasked, imThresh = segment.find_spheroid(crop_img_BF, wellsizemu, mutopx)

        well_frame = trackpy.locate(crop_img_fluo.astype(float), 
                    minsize, 
                    minmass, 
                    percentile
        )

        # rm out of focus cells
        #if len(well_frame) > 0:
        #    well_frame = well_frame[well_frame['ep'] < 0.015]

        well_frame = OT1_status.get_state(well_frame, radius, sph_img)

        if verify_seg:

            if not os.path.exists(os.path.join(folder, "verify_segmentation_OT1")):
                        os.makedirs(os.path.join(folder, "verify_segmentation_OT1"))

            verify_OT1_folder = os.path.join(folder, "verify_segmentation_OT1")

            verify_segmentation.verify_OT1_state(
                        crop_img_BF, crop_img_fluo, well_frame, verify_OT1_folder, m, t
            )

            if not os.path.exists(
                os.path.join(folder, "Spheroid_Region_Detection")
            ):
                os.makedirs(os.path.join(folder, "Spheroid_Region_Detection"))

            verify_sph_folder = os.path.join(folder, "Spheroid_Region_Detection")

            label = well_frame['region_label'].max()

            verify_segmentation.verifySegmentationBF(
                crop_img_BF, sph_img, sobelMasked, imThresh, verify_sph_folder, m, t, label,
            )

            well_frame["m"] = m
            well_frame["frame"] = t

            well_frame["well_center_x"] = xc
            well_frame["well_center_y"] = yc
            well_frame["BF_status"] = True

            track_frame = track_frame.append(well_frame)

            track_frame.to_csv(os.path.join(out_dir, out_fname + ".csv"))

        else:

            well_frame["well_center_x"] = 0
            well_frame["well_center_y"] = 0
            well_frame["spheroid_center_x"] = 0
            well_frame["spheroid_center_y"] = 0
            well_frame["state"] = 0
            well_frame["m"] = m
            well_frame["frame"] = t
            well_frame["BF_status"] = False

            track_frame = track_frame.append(well_frame)

    return make_tracks(track_frame, search_range, mutopx)
