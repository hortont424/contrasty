import math
import sys
import pyopencl as cl
import numpy

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

    # we're throwing out all sorts of information by converting to greyscale
    image = image.convert("L")

    mf = cl.mem_flags
    input = numpy.asarray(image).astype(numpy.uint8)
    output = numpy.zeros((image.size[1], image.size[0])).astype(numpy.uint8)
    gaussian = numpy.asarray(generateKernel(size)).astype(numpy.float32)

    inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)
    gaussianBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=gaussian)

    contrastFilter.program.contrastFilter(clQueue, [image.size[0] * image.size[1]], None, inputBuffer, outputBuffer, gaussianBuffer, numpy.uint32(image.size[0]), numpy.uint32(image.size[1]), numpy.uint32(size)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    outputImage = Image.fromarray(output)

    return outputImage
