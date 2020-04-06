```python
import pandas
import numpy as np
import os
from pathlib import Path

from tqdm.notebook import tqdm
```

## Preparing the local environment

Do not forget to launch the kernel in the "ia" environment by typing

`conda activate ia`

in the terminal before launching jupyter.


```python
import sys
sys.path.insert(0,os.path.join(os.getcwd(),'image-analysis'))
```


```python
from api import read
```


```python
from api.segment import segment
from api.segment import verify_segmentation
from api.analyse import analyse
from api import track
```


```python
import matplotlib.pyplot as plt
```

## Analyze image features

After loading the virtual stack object, we analyze successively the spheroid and the T-cell track properties.


```python
save_path = r'/Users/gustaveronteix/Documents/Projets/Projets Code/imges_test_image_analysis/imges'
```


```python
vs = read.VirtualStack(save_path)
```


```python
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