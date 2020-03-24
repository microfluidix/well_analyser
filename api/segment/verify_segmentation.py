import os
import numpy as np
import matplotlib.pyplot as plt

def verifySegmentationBF(BFimage:np.ndarray, 
    rRegion:np.ndarray, 
    PATH:str, 
    m:int, 
    t:int):

    if not os.path.exists(os.path.join(PATH, str(m), 'Spheroid Region Detection')):
        os.makedirs(os.path.join(PATH, str(m), 'Spheroid Region Detection'))
    savePath = os.path.join(PATH, str(m), 'Spheroid Region Detection')

    fname = f'verif_seg_m{int(m):02d}t{int(t):03d}.jpeg'

    print(os.path.join(savePath, fname))

    fig, _ = plt.subplots(1,1, figsize = (10,10))

    plt.imshow(BFimage, cmap='gray', origin = 'lower')
    plt.imshow(rRegion, alpha = 0.1, origin = 'lower')
    plt.savefig(os.path.join(savePath, fname))
    plt.close(fig)

    return