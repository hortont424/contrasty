import math

from image import *
from log import logCall

lenses = {
    "Nikon-50mm-f1.8": (0.0538741, 0.99783)
}

def computeScaleFactor(focalDistance, lens):
    fit = lenses[lens]
    return (fit[0] / focalDistance) + fit[1]

@logCall
def breathingCorrection(image, focalDistance, lens="Nikon-50mm-f1.8"):
    image = NumpyToPIL(image)

    scaleFactor = computeScaleFactor(focalDistance, lens)

    newSize = tuple([int(round(dim * (1.0 / scaleFactor))) for dim in image.size])
    cropSize = tuple([int(round(dim * (1.0 / computeScaleFactor(1.0, "Nikon-50mm-f1.8")))) for dim in image.size])

    offset = [int(math.ceil((newSize[0] - cropSize[0]) / 2.0)), int(math.ceil((newSize[1] - cropSize[1]) / 2.0))]

    return PILToNumpy(image.resize(newSize).crop((
        offset[0], offset[1],
        offset[0] + cropSize[0], offset[1] + cropSize[1]
        )).copy())