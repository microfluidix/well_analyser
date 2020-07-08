import os
import numpy as np

import trackpy
import pims
import pandas

from api.segment import segment
from api.analyse import analyse
from api.segment import verify_segmentation
import api.segment.utilities as utilities


def get_spheroid_properties(
    vs,
    spheroid_channel: int,
    fluo_channel=None,
    get_fluo=False,
    verify_seg=False,
    wellSizeMu=430,
    mutopx=3,
):

    """
    
    extracts spheroid properties from image batch.

    COMMENT: with meta data we will integrate the above
    variables implicitely.

    Returns:
     - pandas.DataFrame
    
    """

    spheroid_frame = pandas.DataFrame()

    c1_time_reader = vs.read(t=None, m=None, c=spheroid_channel)

    for img in c1_time_reader:

        try:

            t = img.meta["t"]
            m = img.meta["m"]

            (xc, yc) = utilities._get_center(img.array, wellSizeMu, wellSizeMu, mutopx)

            # function to be changed to Andrey's version
            crop_img_BF = segment.select_well(
                img.array, img.array, wellSizeMu, wellSizeMu, mutopx
            )
            sph_img = segment.find_spheroid(crop_img_BF, wellSizeMu, mutopx)

            if get_fluo:

                img_Fluo = vs.get_single_image(m=m, t=t, c=fluo_channel)

                crop_img_Fluo = segment.select_well(
                    img.array, img_Fluo.array, wellSizeMu, wellSizeMu, mutopx
                )

                timeFrame = analyse.spheroid_properties(sph_img, crop_img_Fluo)

            else:

                timeFrame = analyse.spheroid_properties(sph_img)

            timeFrame["t"] = int(t)
            timeFrame["m"] = int(m)
            timeFrame["well_center_x"] = xc
            timeFrame["well_center_y"] = yc
            timeFrame["mask_size"] = wellSizeMu * mutopx

            folder = os.path.dirname(vs.folder)

            if not os.path.exists(os.path.join(folder, "spheroid_data_frame")):
                os.makedirs(os.path.join(folder, "spheroid_data_frame"))

            timeFrame.to_csv(
                os.path.join(
                    os.path.join(folder, "spheroid_data_frame", str(m) + "_" + str(t))
                )
            )

            spheroid_frame = spheroid_frame.append(timeFrame)

            # Verify segmentation

            if verify_seg:

                folder = vs.folder

                if not os.path.exists(os.path.join(folder, "verify segmentation")):
                    os.makedirs(os.path.join(folder, "verify segmentation"))

                verify_segmentation.verifySegmentationBF(
                    crop_img_BF,
                    sph_img,
                    os.path.join(folder, "verify segmentation"),
                    int(m),
                    int(t),
                )

        except Exception as e:
            print(e)

    return spheroid_frame
