import sys
import os
import click

import pandas

from api.track_spheroids import track_spheroids
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
    default='image_path',
    show_default=True,
    help='Where to save the resulting csv files'
)
@click.option(
    '--out_fname', '-fn',
    default='spheroid_frame',
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
    '--fluo_channel', '-f',
    type=int,
    default=2,
    show_default=True,
    help='Fluo channel number'
)
@click.option(
    '--get_fluo/--ignore_fluo', '-gf/-if',
    type=bool,
    default=False,
    show_default=True,
    help='Get fluo properties of masked spheroid'
)
@click.option(
    '--verify_seg', '-vs',
    type=bool,
    default=False,
    show_default=True,
    help='Create verification images of segmentation'
)
@click.option(
    '--wellSizeMu', '-ws',
    default=430,
    type=int,
    show_default=True,
    help='Well size in micrometers'
)

def main(image_path:str='',
    channel:int=1, 
    out_dir:str='',
    out_fname:str='',
    mutopx:int=3,
    fluo_channel:int=2,
    get_fluo:bool=False,
    verify_seg:bool=True,
    wellSizeMu:int=430):

    vs = read.VirtualStack(image_path)

    data_frame = track_spheroids.get_spheroid_properties(vs,
                        spheroid_channel = channel,
                        fluo_channel = fluo_channel,
                        get_fluo = get_fluo,
                        verify_seg = verify_seg,
                        wellSizeMu = wellSizeMu,
                        mutopx = mutopx)


    data_frame.to_csv(os.path.join(out_dir, out_fname + '.csv'))

    return True

if __name__ == "__main__":
    main()

