import PIL

from log import *

@logCall()
def contrastFilter(image, size=3):
    """
    Return an image with each pixel from *image* replaced by the local contrast in a (*size*, *size*) environment.

    Contrast is determined by a distance-weighted average of the difference between the center pixel and
    each other pixel in the environment.
    """

    log("Something happened here!!", priority=Priority.LOW)