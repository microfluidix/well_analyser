# Image analysis toolbox in Python

## Installation for development

Make sure you use Python 3.8 `python -V`

If not:

```
conda create -n ia python=3.8
conda activate ia
```

or download and install Python 3.8 

Install the package in development mode.
```
git clone git@gitlab.pasteur.fr:pub/image-analysis.git
cd image-analysis
pip install -e .
```

## API

### processing many 2d tiffs in one folder

```
>>> from api import read
>>> from api.core import Well

>>> prefix = r'Z:/Andrey/data/Salome/20200228/NIS_export/'

>>> vs = read.VirtualStack(prefix, search_names='*.tif', regex=r'([ctmz])(\d{1,2})')

>>> vs

    Virtial Stack instance. 
    Found 864 files in Z:/Andrey/data/Salome/20200228/NIS_export/. Ranges: {'t': {'min': 2, 'max': 33}, 'z': {'min': 1, 'max': 9}, 'c': {'min': 1, 'max': 3}}

>>> vs.ranges

    {'t': {'min': 2, 'max': 33},
    'z': {'min': 1, 'max': 9},
    'c': {'min': 1, 'max': 3}}

 >>> vs.order

    'tcz'

>>> img = vs.get_single_image(t=2,z=1,c=3)

>>> img

    array (7103, 10599), {'t': 2, 'z': 1, 'c': 3, 'path': 't02z1c3.tif', 'prefix': 'Z:/Andrey/data/Salome/20200228/NIS_export/'}

>>> img.bin(10)

    array (711, 1060), {'binning': 10, 't': 2, 'z': 1, 'c': 3, 'path': 't02z1c3.tif', 'prefix': 'Z:/Andrey/data/Salome/20200228/NIS_export/'}

>>> arr = []
    for v in vs.read(c=3, z=5, t=None):
        print(v.array.shape, v.array.mean(), v.meta)
        arr.append(v.bin(10))

>>> w = Well.stack(arr)

>>> w

    Showing first layer
    array (32, 711, 1060), {'binning': {10}, 'c': {3}, 'z': {5}, 't': {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33}, 'path': {'t14z5c3.tif', 't30z5c3.tif', 't18z5c3.tif', 't13z5c3.tif', 't02z5c3.tif', 't19z5c3.tif', 't29z5c3.tif', 't25z5c3.tif', 't33z5c3.tif', 't03z5c3.tif', 't32z5c3.tif', 't10z5c3.tif', 't31z5c3.tif', 't15z5c3.tif', 't27z5c3.tif', 't11z5c3.tif', 't17z5c3.tif', 't20z5c3.tif', 't06z5c3.tif', 't16z5c3.tif', 't05z5c3.tif', 't12z5c3.tif', 't04z5c3.tif', 't23z5c3.tif', 't24z5c3.tif', 't08z5c3.tif', 't22z5c3.tif', 't26z5c3.tif', 't07z5c3.tif', 't28z5c3.tif', 't21z5c3.tif', 't09z5c3.tif'}, 'prefix': {'Z:/Andrey/data/Salome/20200228/NIS_export/'}, 'stacked': 32}



```


