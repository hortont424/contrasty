import math
import sys
import pyopencl as cl
import numpy
import numpy.numarray.nd_image as nd_image

from PIL import Image

from log import logCall

def generateKernel(d):
    r = int(math.floor(d / 2.0))
    sinvsq = 36.0 / ((1.0 + 2.0 * r) * (1.0 + 2.0 * r))
    return [math.exp(-0.5 * (x * x) * sinvsq) for x in range(r)]

@logCall
def contrastFilter(image, clContext, clQueue, size=41):
    """
    Return an image with each pixel from *image* replaced by the local contrast in a (*size*, *size*) environment.

    Contrast is determined by a Gaussian-weighted average of the difference between the center pixel and
    each other pixel in the environment.
    """

    if not hasattr(contrastFilter, "program"):
        kernelFile = open('src/kernels/contrastFilter.cl', 'r')
        contrastFilter.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    if not size % 2:
        print "{0} is not an odd integer".format(size)

    mf = cl.mem_flags

    output = numpy.zeros(image.shape).astype(numpy.uint8)
    gaussian = numpy.asarray(generateKernel(size)).astype(numpy.float32)

    imageBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=image)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)
    gaussianBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=gaussian)

    contrastFilter.program.contrastFilter(clQueue, [image.size], None, imageBuffer, outputBuffer, gaussianBuffer, numpy.uint32(image.shape[1]), numpy.uint32(image.shape[0]), numpy.uint32(size)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    filtered = nd_image.maximum_filter(output, size=(82, 82)) # highly dependent on feature size/image resolution

    return filtered
