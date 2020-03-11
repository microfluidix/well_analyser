from glob import glob
import re
import numpy as np
import os
from api.core import Well
from tifffile import imread
from skimage.transform import downscale_local_mean


class VirtualStack:

    '''Handle tif exports from NIS'''
    
    def __init__(self, folder:str, search_names:str='*.tif', regex:str=r't(\d{2})z(\d)c(\d)'):
        self.folder = folder
        self.flist = glob(os.path.join(folder, search_names))
        assert len(self.flist) > 0, 'No files found'
        self.indices = list(map(get_indices, self.flist))
        self.ranges = get_sizes(self.indices)

     
    def read(self, t=(None, None), z=(None, None), c=(None,None), bin=0):
        '''
        Get generator with a selected sequence

        Parameters:
        -----------
        t, int, tuple or None:
            time value or range
        z - the same
        c - the same
        Return:
        -------
        api.Well object
        Raise:
        ------
        ValueError if coordiantes are out of range
        '''
        ranges = []
        for ax, values in zip('tzc', (t, z, c)):
            _range = self.check_range(values, ax)
            ranges.append(_range)
        for _t in ranges[0]:
            for _z in ranges[1]:
                for _c in ranges[2]:
                    img =  self.get_single_image(_t, _z, _c)
                    if bin > 1:
                        img = img.bin(bin)
                    yield img
      
    def get_single_image(self, t:int, z:int, c:int) -> Well:
        '''reads .tif from disk, returns api.core.Well instance'''
        t, z, c = [self.check_range(v, ax)[0] for v, ax in zip((t,z,c), 'tzc')]
        fname = get_fname({'t': t, 'z': z, 'c': c})
        path = os.path.join(self.folder, fname)
        return Well(imread(path),  meta={'t': t, 'z': z, 'c': c, 'path': fname, 'prefix': self.folder})
    
    def check_range(self, values:tuple, axis:str):
        '''
        Check range values and generate range
        
        '''
        
        def single_check(value, axis=axis, upper:bool=False):
            side = ['min', 'max'][int(upper)]
            sr = self.ranges[axis]
            if value is None:
                return sr[side]
            assert isinstance(value, int)
            assert sr['min'] <= value <= sr['max'], f'{value} out of range for {axis}: {sr}'
            return value
            
        if values is None:
            return range(single_check(None, upper=False), single_check(None, upper=True) + 1) 
        elif isinstance(values, int):
            return (single_check(values),)
        
        elif isinstance(values, tuple):
            assert len(values) == 2
            return range(single_check(values[0], upper=False), single_check(values[1], upper=True) + 1)
        else:
            raise ValueError(f'range {values} not understood, provide int or tuple')

    def __repr__(self):
        return f'Virtial Stack instance. \nFound {len(self.flist)} files in {self.folder}. Ranges: {self.ranges}'
   

def get_indices(fname:str, regexp=r't(\d{2})z(\d)c(\d)', order='tzc'):
    r = re.compile(regexp)
    finds = r.findall(fname)
    assert len(finds) == 1
    assert len(finds[0]) == 3
    indices = {k: int(v) for k, v in zip(order, finds[0])}
    return indices


def get_fname(indices:dict, order='tzc'):
    '''
    Returns filename.tif in format `t00z0c0.tif`
    '''
    assert ''.join(indices.keys()) == order
    t, z, c = indices.values()
#     print(t,z,c)
    return f't{t:02d}z{z}c{c}.tif'


def get_sizes(indices:dict, order='tzc'):
    '''
    Returns min-max values for each dimension in the dict
    '''
    tzc = np.array([[d['t'], d['z'], d['c']] for d in indices], dtype='uint8')
    _max = tzc.max(axis=0)
    _min = tzc.min(axis=0)
    ranges = {o: {'min': low, 'max': high} for o, low, high in zip(order, _min, _max)}
    return ranges
    