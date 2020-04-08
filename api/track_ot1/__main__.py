import sys
import os
import click

import pandas

from api.track_ot1 import track_ot1
from api import read

@click.command()
@click.argument('image_path', nargs=1)
@click.option(
    '--channel', '-c', 
    type=int, 
    default=1, 
    show_default=True, 
    help='Relevant channel for analysis'
)
@click.option(
    '--out_dir', '-o',
    default='.',
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

def main(image_path:str,
    channel:int, 
    out_dir:str,
    out_fname:str,
    mutopx:int,
    search_range:int,
    minsize:int,
    minmass:int,
    percentile:float):

    vs = read.VirtualStack(image_path)

    data_frame = track_ot1.get_cell_tracks(vs,
                        fluo_channel = channel,
                        mutopx = mutopx,
                        search_range = search_range,
                        minsize = minsize,
                        minmass = minmass,
                        percentile = percentile)

    data_frame.to_csv(os.path.join(out_dir, out_fname + '.csv'))

    return True

if __name__ == "__main__":

    main()

