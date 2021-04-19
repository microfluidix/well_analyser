# Image analysis toolbox

The current image analysis code serves to analyse the chip microscopy images. Each image is composed of a single spheroid-containing well and can be multi-channeled.

## Installation

Make sure you use Python 3.8 by typing the command `python -V`.

Otherwise:

```
conda create -n ia python=3.8
conda activate ia
```

Install the package in development mode:

```
git clone git@gitlab.pasteur.fr:pub/image-analysis.git
cd image-analysis
pip install .
```

## API

### From the command line

The well images are extracted from their native `ND2` format to tiff files using Nikon proprietary software. All the images are now in a single folder and indexed according to their position number, time frame and channel. See the format in the `example_image` folder.

The image analysis code is designed to be called from the command line in the terminal. To see all the analysis options available type:

```
python -m api.track_ot1 --help

```

Starting from the example images and using the default parameters, one types:


```
python -m api.track_ot1 PATH_TO_EXAMPLE_FOLDER

```

This should generate two new folders containing the segmentation results and the T-cell detection results, allowing the user to fine-tune the parameters for optimal detection results. This also generates a single CSV file that will be the basis for the future analysis.

### From a Jupyter Notebook


After loading the virtual stack object, we analyze successively the spheroid 
and the T-cell track properties.

```python
from api import read
from api import track

import matplotlib.pyplot as plt

save_path = r'/Example/Path/As/String'

vs = read.VirtualStack(save_path)

spheroid_frame = track.get_spheroid_properties(vs,
                                               spheroid_channel = 1, 
                                               fluo_channel = 3, 
                                               get_fluo = True, 
                                               verify_seg = True,
                                               wellSizeMu = 430,
                                               muTopx = 3)

t_cell_frame = track.get_cell_tracks(vs,
                                    fluo_channel = 2,
                                    muTopx = 3,
                                    search_range = 40,
                                    minsize = 10,
                                    minmass = 10000,
                                    percentile = 90)
```

You now have access to the spheroid and T-cell positions in your image stack.