lenses = {
    "Nikon-50mm-f1.8": (0.0538741, 0.99783)
}

def computeScaleFactor(focalDistance, lens):
    fit = lenses[lens]
    return (fit[0] / focalDistance) + fit[1]

def breathingCorrection(image, focalDistance, lens="Nikon-50mm-f1.8"):
    scaleFactor = computeScaleFactor(focalDistance, lens)
    print focalDistance, scaleFactor
    newSize = tuple([int(round(dim * scaleFactor)) for dim in image.size])
    sizeDifference = [a - b for a, b in zip(newSize, image.size)]
    return image.resize(newSize).crop((int(sizeDifference[0] / 2.0),
                                       int(sizeDifference[1] / 2.0),
                                       image.size[0], image.size[1]))