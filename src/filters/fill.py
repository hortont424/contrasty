import math
import sys
import pyopencl as cl
import numpy
import numpy.numarray.nd_image as nd_image

from PIL import Image

from log import logCall

@logCall
def fillImage(image, clContext, clQueue):
    if not hasattr(fillImage, "program"):
        kernelFile = open('src/kernels/fillImage.cl', 'r')
        fillImage.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags
    output = numpy.zeros(image.shape).astype(numpy.uint8)

    while len(numpy.flatnonzero(output)) < (image.size) - 1:
        output = numpy.zeros(image.shape).astype(numpy.uint8)

        imageBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=image)
        outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

        fillImage.program.fillImage(clQueue, [image.size], None, imageBuffer, outputBuffer, numpy.uint32(image.shape[1]), numpy.uint32(image.shape[0])).wait()

        cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

        image = output

    output = nd_image.grey_opening(nd_image.grey_closing(output, size=(9,9)), size=(9,9))

    return output
