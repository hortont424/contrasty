import math
from PIL import Image

from log import *

def gaussianFunction(x, sigma):
    """
    Return the Gaussian function evaluated at x.
    """
    return math.exp(-0.5 * (x * x) / (sigma * sigma))

def gaussianKernel1D(d):
    """
    Generate a one-dimensional Gaussian kernel.
    """
    r = int(math.floor(d / 2.0))
    sigma = (1.0 / 3.0) * r + (1.0 / 6.0)
    print [(x, gaussianFunction(x, sigma)) for x in range(-r, r + 1)]
    return [(x, gaussianFunction(x, sigma)) for x in range(-r, r + 1)]

# TODO: This is far too slow as implemented in Python; this should be rewritten in C and called from here.
# Also, during the rewrite, we should implement 2D convolution instead of 2 1D convolutions, since I'm not
# positive that that works here.

@logCall
def contrastFilter(image, size=5):
    """
    Return an image with each pixel from *image* replaced by the local contrast in a (*size*, *size*) environment.

    Contrast is determined by a Gaussian-weighted average of the difference between the center pixel and
    each other pixel in the environment.
    """

    lumaImage = image.convert("L")
    lumaPixels = lumaImage.load()
    contrastImage = Image.new("L", lumaImage.size)
    contrastPixels = contrastImage.load()

    width, height = lumaImage.size
    kernel = gaussianKernel1D(size)

    for x in range(width):
        for y in range(height):
            convolveValue = 0.0
            convolveCount = 0.0

            for (kx, kv) in kernel:
                cx = x + kx
                if cx > 0 and cx < width and cx != x:
                    convolveValue += kv * abs(lumaPixels[cx, y] - lumaPixels[x, y])
                    convolveCount += kv

            contrastPixels[x, y] = convolveValue / convolveCount

    for x in range(width):
        for y in range(height):
            convolveValue = 0.0
            convolveCount = 0.0

            for (ky, kv) in kernel:
                cy = y + ky
                if cy > 0 and cy < height and cy != y:
                    convolveValue += kv * abs(contrastPixels[x, cy] - contrastPixels[x, y])
                    convolveCount += kv

            contrastPixels[x, y] = (convolveValue / convolveCount)

    return contrastImage