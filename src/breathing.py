import math

lenses = {
    "Nikon-50mm-f1.8": (0.0538741, 0.99783)
}

def computeScaleFactor(focalDistance, lens):
    fit = lenses[lens]
    return (fit[0] / focalDistance) + fit[1]

def breathingCorrection(image, focalDistance, lens="Nikon-50mm-f1.8"):
    scaleFactor = computeScaleFactor(focalDistance, lens)
    print focalDistance, scaleFactor
    newSize = tuple([int(round(dim * (1.0 / math.sqrt(scaleFactor)))) for dim in image.size])
    sizeDifference = [a - b for a, b in zip(newSize, image.size)]

    return image.resize(newSize).crop((
        newSize[0]-800,newSize[1]-600,newSize[0],newSize[1]
        ))