import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas

from matplotlib_scalebar.scalebar import ScaleBar


def verifySegmentationBF(
    BFimage: np.ndarray, 
    rRegion: np.ndarray, 
    sobelMasked: np.ndarray,
    imThresh: np.ndarray,
    PATH: str, m: int, t: int, label:int
):

    if not os.path.exists(os.path.join(PATH, str(m))):
        os.makedirs(os.path.join(PATH, str(m)))
    savePath = os.path.join(PATH, str(m))

    fname = f"{int(m):02d}t{int(t):03d}.jpeg"

    fig, ax = plt.subplots(1, 3, figsize=(10, 10))

    plt.imshow(BFimage, cmap="gray", origin="lower")

    ax[0].imshow(BFimage, cmap="gray", origin="lower")
    ax[0].axis("off")

    ax[1].imshow(imThresh, cmap="viridis", origin="lower")
    ax[1].axis("off")

    ax[2].imshow(BFimage, cmap="gray", origin="lower")
    ax[2].imshow(rRegion, alpha = 0.3, origin="lower")
    ax[2].axis("off")
    
    scalebar = ScaleBar(0.33, units="um")
    plt.gca().add_artist(scalebar)
    plt.savefig(os.path.join(savePath, fname))
    plt.close(fig)

    return

def verify_OT1_segmentation(
    Fluoimage: np.ndarray, 
    well_frame: pandas.DataFrame,
    PATH: str, 
    m: int, 
    t: int
):

    if not os.path.exists(os.path.join(PATH, str(m))):
        os.makedirs(os.path.join(PATH, str(m)))
    savePath = os.path.join(PATH, str(m))

    fname = f"{int(m):02d}t{int(t):03d}.jpeg"

    fig, _ = plt.subplots(1, 1, figsize=(10, 10))

    plt.imshow(Fluoimage, cmap="gray", origin="lower")
    plt.axis("off")

    plt.scatter(
        well_frame["x"],
        well_frame["y"]
    )

    scalebar = ScaleBar(0.33, units="um")
    plt.gca().add_artist(scalebar)
    plt.savefig(os.path.join(savePath, fname))
    plt.close(fig)

    return


def verify_OT1_state(
    BFimage: np.ndarray,
    Fluoimage: np.ndarray,
    well_frame: pandas.DataFrame,
    PATH: str,
    m: int,
    t: int,
):

    if not os.path.exists(os.path.join(PATH, str(m))):
        os.makedirs(os.path.join(PATH, str(m)))
    savePath = os.path.join(PATH, str(m))

    fname = f"verif_seg_m{int(m):02d}t{int(t):03d}.jpeg"

    colors = ["tab:blue", "tab:red"]

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].imshow(BFimage, cmap="gray", origin="lower")
    ax[0].plot(well_frame["spheroid_center_x"].unique(),
        well_frame["spheroid_center_y"].unique(),
        'go')
    ax[0].scatter(
        well_frame["x"],
        well_frame["y"],
        c=well_frame["state"].apply(lambda x: colors[x]),
    )
    ax[0].axis("off")

    ax[1].imshow(Fluoimage, cmap="gray", origin="lower")
    ax[1].scatter(
        well_frame["x"],
        well_frame["y"],
        c=well_frame["state"].apply(lambda x: colors[x]),
    )
    ax[1].axis("off")
    scalebar = ScaleBar(0.33, units="um")

    plt.gca().add_artist(scalebar)
    plt.savefig(os.path.join(savePath, fname))
    plt.close(fig)

    return True
