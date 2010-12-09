import math
import sys
import pyopencl as cl
import numpy

from PIL import Image

from log import logCall

@logCall
def infiniteFocus(images, depth, clContext, clQueue):
    if not hasattr(infiniteFocus, "program"):
        kernelFile = open('src/kernels/infiniteFocus.cl', 'r')
        infiniteFocus.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags

    output = numpy.zeros(images[0].shape).astype(numpy.uint8)
    depthBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=depth)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

    for currentImage in range(len(images)):
        image = images[currentImage]
        imageBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=image)

        infiniteFocus.program.infiniteFocus(clQueue, [images[0].size], None, imageBuffer, outputBuffer, depthBuffer, numpy.uint32(images[0].shape[1]), numpy.uint32(images[0].shape[0]), numpy.uint32(len(images)), numpy.uint32(currentImage)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    return output
