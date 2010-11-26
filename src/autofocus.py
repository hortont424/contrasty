import math
import pyopencl as cl
import numpy

from PIL import Image

from log import *

def contrastFilter(image, clContext, clQueue, size=5):
    """
    Return an image with each pixel from *image* replaced by the local contrast in a (*size*, *size*) environment.

    Contrast is determined by a Gaussian-weighted average of the difference between the center pixel and
    each other pixel in the environment.
    """

    if not hasattr(contrastFilter, "program"):
        kernelFile = open('src/contrastFilter.cl', 'r')
        contrastFilter.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    # we're throwing out all sorts of information by converting to greyscale
    image = image.convert("L")

    mf = cl.mem_flags
    input = numpy.asarray(image).astype(numpy.uint8)
    output = numpy.zeros((image.size[1], image.size[0])).astype(numpy.uint8)

    inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

    contrastFilter.program.contrastFilter(clQueue, [image.size[0] * image.size[1]], None, inputBuffer, outputBuffer, numpy.uint32(image.size[0]), numpy.uint32(image.size[1])).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    outputImage = Image.fromarray(output)

    return outputImage
