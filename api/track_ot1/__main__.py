import sys
import os
import click

import pandas

from api.track import track
from api import read

@click.command()
@click.argument('image_path', nargs=1)
@click.option(
    '--ot1/--spheroid', '-o/-s',
    type=bool,
    help='Operation type: OT-1 or spheroid tracking'
)
@click.option(
    '--channel', '-c', 
    type=int, 
    default=1, 
    show_default=True, 
    help='Relevant channel for analysis'
)
@click.option(
    '--out_dir', '-o',
    default='image_path',
    show_default=True,
    help='Where to save the resulting csv files'
)
@click.option(
    '--muTopx', '-mu', 
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
    help='Search range (px) for the tracking'
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
    default=10000,
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
    '--fluo_channel', '-f',
    type=int,
    default=2,
    show_default=True,
    help='Fluo channel number'
)
@click.option(
    '--get_fluo/--ignore_fluo', '-gf/-if',
    type=bool,
    help='Get fluo properties of masked spheroid'
)
@click.option(
    '--verify_seg', '-vs',
    default='image_path',
    show_default=True,
    help='Where to save the resulting csv files'
)
@click.option(
    '--wellSizeMu', '-ws',
    default='image_path',
    show_default=True,
    help='Where to save the resulting csv files'
)



def main(image_path:str='', 
    ot1:bool=True, 
    channel:int=1, 
    out_dir:str='',):

    vs = read.VirtualStack(image_path)

    if ot1:

        data_frame = track.get_cell_tracks(vs,
                        fluo_channel = channel,
                        muTopx = 3,
                        search_range = 40,
                        minsize = 10,
                        minmass = 10000,
                        percentile = 90)

    else:

        data_frame = track.get_spheroid_properties(vs,
                        spheroid_channel = channel,
                        fluo_channel = None,
                        get_fluo = False,
                        verify_seg = False,
                        wellSizeMu = 430,
                        muTopx = 3)


    data_frame.to_csv(os.path.join(out_dir, ot1 + '.csv'))

    return True

if __name__ == "__main__":
    main()

