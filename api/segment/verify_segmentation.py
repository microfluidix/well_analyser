import os
import numpy as np
import matplotlib.pyplot as plt

def verifySegmentationBF(BFimage:np.ndarray, 
    rRegion:np.ndarray, 
    PATH:str, 
    experiment:str, 
    time:str):

    if not os.path.exists(os.path.join(PATH, experiment, 'Spheroid Region Detection')):
        os.makedirs(os.path.join(PATH, experiment, 'Spheroid Region Detection'))
    savePath = os.path.join(PATH, experiment, 'Spheroid Region Detection')

    fig, ax = plt.subplots(1,1, figsize = (10,10))

    plt.imshow(BFimage, cmap='gray', origin = 'lower')
    plt.imshow(rRegion, alpha = 0.1, origin = 'lower')
    plt.savefig(os.path.join(savePath, 'testFrame_%time.jpeg' %round(int(time,0))))
    plt.close(fig)

    return