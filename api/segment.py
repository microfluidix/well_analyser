

def _crop(imgToCrop:np.ndarray, imgToAnalyze:np.ndarray, maskSize:int,
    wellSize:int, muToPx:float):

    """

    Crop function. Works only on 2D images. The imgToCrop is the to be cropped
    image and imgToAnalyze serves to find the well center.

    Returns:
    - np.ndarray

    """

    (xc, yc) = _getCenter(imgToAnalyze,maskSize,wellSize,muToPx)

    cropDist = maskSize*muToPx

    startx = max(xc-(cropDist//2), 0)
    starty = max(yc-(cropDist//2), 0)

    return imgToCrop[int(startx):int(startx+cropDist),int(starty):int(starty+cropDist)]
