import sys
import os
import click

import pandas

from api.track_ot1 import track_ot1
from api import read

@click.command()
@click.argument('image_path', nargs=1)

@click.option(
    '--channel_fluo', '-cfl', 
    type=int, 
    default=2, 
    show_default=True, 
    help='Relevant channel for analysis'
)

@click.option(
    '--channel_bf', '-cbf', 
    type=int, 
    default=1, 
    show_default=True, 
    help='BF channel'
)

@click.option(
    '--out_dir', '-o',
    default='',
    show_default=True,
    help='Where to save the resulting csv files'
)
@click.option(
    '--out_fname', '-fn',
    default='ot1_frame',
    show_default=True,
    help='Name of output csv file'
)
@click.option(
    '--mutopx', '-mu', 
    type=int, 
    default=3, 
    show_default=True, 
    help='Micrometers to pixels conversion rate'
)
@click.option(
    '--search_range', '-r',
    type=int,
    default=40,
    show_default=True,
    help='Search range (mu) for the tracking'
)
@click.option(
    '--minsize', '-ms',
    type=int,
    default=10,
    show_default=True,
    help='Minimum feature size for the tracking'
)
@click.option(
    '--minmass', '-mm',
    type=int,
    default=5000,
    show_default=True,
    help='Minimum particle mass in tracking'
)
@click.option(
    '--percentile', '-p',
    type=float,
    default=90.0,
    show_default=True,
    help='Percentile below which local maxima will be ignored'
)

@click.option(
    '--state', '-s',
    type=bool,
    default=True,
    show_default=True,
    help='Get position of OT-1 relative to the spheroid'
)

@click.option(
    '--verify_seg', '-vseg',
    type=bool,
    default=True,
    show_default=True,
    help='Verify the segmentation results'
)

@click.option(
    '--radius', '-r',
    type=int,
    default=10,
    show_default=True,
    help='Error margin (in px) for the OT-1 state attribution.'
)

@click.option(
    '--wellsizemu', '-ws',
    type=int,
    default=430,
    show_default=True,
    help='Default well size in mu.'
)

def main(image_path:str,
    channel_fluo:int = 2,
    channel_bf:int = 1, 
    out_dir:str = '',
    out_fname:str = 'ot1_frame',
    mutopx:int = 3,
    search_range:int = 20,
    minsize:int = 17,
    minmass:int = 1000,
    percentile:float = 60,
    state:bool = True,
    verify_seg:bool = True,
    radius:int = 10,
    wellsizemu:int = 430):

    if '.nd2' in image_path:

        vs = read.nd2(image_path)

    else:

        vs = read.VirtualStack(image_path)

    if out_dir == '':

        out_dir = image_path

    print(vs.ranges)

    if not state:

        data_frame = track_ot1.get_cell_tracks(
            vs,
            fluo_channel=channel_fluo,
            mutopx=mutopx,
            search_range=search_range,
            minsize=minsize,
            minmass=minmass,
            percentile=percentile,
        )

        data_frame.to_csv(os.path.join(out_dir, out_fname + '.csv'))

    else:

        data_frame =track_ot1.get_cell_tracks_state(vs,
                            fluo_channel = channel_fluo,
                            fluo_BF = channel_bf,
                            mutopx = mutopx,
                            search_range = search_range,
                            minsize = minsize,
                            minmass = minmass,
                            percentile = percentile,
                            verify_seg = verify_seg,
                            radius = radius,
                            wellsizemu = wellsizemu)

        data_frame.to_csv(os.path.join(out_dir, out_fname + ".csv"))

    return True

if __name__ == "__main__":

    main()
   