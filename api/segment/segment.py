

def _crop(imgToCrop:np.ndarray,
    imgToAnalyze:np.ndarray,
    maskSize:int,
    wellSize:int,
    muToPx:float):

    """

    Crop function. Works only on 2D images. The imgToCrop is the to be cropped
    image and imgToAnalyze serves to find the well center.

    Returns:
    - np.ndarray

    """

    assert len(imgToCrop.shape) == 2

    (xc, yc) = _getCenter(imgToAnalyze,maskSize,wellSize,muToPx)

    cropDist = maskSize*muToPx

    startx = max(xc-(cropDist//2), 0)
    starty = max(yc-(cropDist//2), 0)

    return imgToCrop[int(startx):int(startx+cropDist),int(starty):int(starty+cropDist)]

def _makeCircMask(maskSize:int,
    wellSize:int,
    muToPx:float):

    """

    Makes a donut mask for future convolution.

    Returns:
    - np.ndarray

    """

    cropDist = maskSize*muToPx

    X = np.arange(cropDist)
    Y = X

    X, Y = np.meshgrid(X, Y)

    mask = ((np.sqrt((X-cropDist//2)**2 + (Y-cropDist//2)**2) > (wellSize*muToPx)//2 - 10*muToPx) &
            (np.sqrt((X-cropDist//2)**2 + (Y-cropDist//2)**2) < (wellSize*muToPx)//2 + 10*muToPx))

    return mask.astype(np.int)


def _getCenter(imgToAnalyze:np.ndarray, maskSize:int, wellSize:int,
    muToPx:float):

    """

    Find the well center of an image.

    Returns:
    - tuple

    """

    mask = _makeCircMask(maskSize,wellSize,muToPx)

    conv = cv2.filter2D(imgToAnalyze, cv2.CV_32F, mask)

    return unravel_index(conv.argmin(), conv.shape)


def _centerSelect(imToCrop:np.ndarray, wellDiameter:int, marginDistance:int,
    umToPx:float):

    """

    Function to take image, find the well center,
    throw away all the points beyond the marginDistance.

    Returns:
    - np.ndarray

    """

    img = _crop(imToCrop, imToCrop, wellDiameter, wellDiameter, umToPx)

    mask = _makeDiskMask(wellDiameter, wellDiameter-marginDistance, umToPx)
    t = np.zeros(np.shape(mask))
    a, b = np.shape(img)
    t[:a, :b] = img
    #combine pour gerer les crops de forme non carree

    finalIm = np.multiply(t, mask)
    finalIm[finalIm == 0] = np.max(finalIm)

    return gaussian_filter(finalIm, sigma=5)


def _makeDiskMask(maskSize:int, diskSize:int, umToPx:float):

    """

    Makes a circular mask of given radius.

    Returns:
    - np.ndarray

    """

    cropDist = maskSize*umToPx

    X = np.arange(cropDist)
    Y = X
    X, Y = np.meshgrid(X, Y)

    mask = (np.sqrt((X-cropDist//2)**2 + (Y-cropDist//2)**2) < (diskSize*umToPx)//2)

    return mask.astype(np.int)
