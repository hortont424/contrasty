import numpy
from PIL import Image

class Image3D(object):
    def __init__(self):
        super(Image3D, self).__init__()

        self.sourceDirectory = None
        self.images = []
        self.depth = None

def PILToNumpy(img):
    return numpy.asarray(img).astype(numpy.uint8)

def NumpyToPIL(img):
    return Image.fromarray(img)