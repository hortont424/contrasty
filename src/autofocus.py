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

    image = image.convert("L")

    mf = cl.mem_flags
    input = numpy.asarray(image).astype(numpy.uint8)
    output = numpy.zeros((image.size[1], image.size[0])).astype(numpy.uint8)

    inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

    contrastFilter.program.contrastFilter(clQueue, [image.size[0] * image.size[1]], None, inputBuffer, outputBuffer, numpy.uint32(image.size[0]), numpy.uint32(image.size[1])).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    outputImage = Image.fromarray(output)

    outputImage.show()

    return outputImage

    #lumaImage = image.convert("L")
    #lumaPixels = lumaImage.load()
    #contrastImage = Image.new("L", lumaImage.size)
    #contrastPixels = contrastImage.load()
    #
    #width, height = lumaImage.size
    #kernel = gaussianKernel1D(size)
    #
    #for x in range(width):
    #    for y in range(height):
    #        convolveValue = 0.0
    #        convolveCount = 0.0
    #
    #        for (kx, kv) in kernel:
    #            cx = x + kx
    #            if cx > 0 and cx < width and cx != x:
    #                convolveValue += kv * abs(lumaPixels[cx, y] - lumaPixels[x, y])
    #                convolveCount += kv
    #
    #        contrastPixels[x, y] = convolveValue / convolveCount
    #
    #for x in range(width):
    #    for y in range(height):
    #        convolveValue = 0.0
    #        convolveCount = 0.0
    #
    #        for (ky, kv) in kernel:
    #            cy = y + ky
    #            if cy > 0 and cy < height and cy != y:
    #                convolveValue += kv * abs(contrastPixels[x, cy] - contrastPixels[x, y])
    #                convolveCount += kv
    #
    #        contrastPixels[x, y] = (convolveValue / convolveCount)
    #
    #return contrastImage