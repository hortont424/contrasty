import math

from log import logCall

lenses = {
    "Nikon-50mm-f1.8": (0.0538741, 0.99783)
}

def computeScaleFactor(focalDistance, lens):
    fit = lenses[lens]
    return (fit[0] / focalDistance) + fit[1]

@logCall
def breathingCorrection(image, focalDistance, lens="Nikon-50mm-f1.8"):
    scaleFactor = computeScaleFactor(focalDistance, lens)
    print focalDistance, scaleFactor
    newSize = tuple([int(round(dim * (1.0 / scaleFactor))) for dim in image.size])
    cropSize = tuple([int(round(dim * (1.0 / computeScaleFactor(1.0, "Nikon-50mm-f1.8")))) for dim in image.size])

    print newSize, cropSize

    sizeDifference = [a - b for a, b in zip(newSize, image.size)]

    return PILToNumpy(NumpyToPIL(image).resize(newSize).crop((
        (newSize[0] - cropSize[0]) / 2, (newSize[1] - cropSize[1]) / 2,
        newSize[0] - ((newSize[0] - cropSize[0]) / 2), newSize[1] - ((newSize[1] - cropSize[1]) / 2)
        )))