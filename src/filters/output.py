import math
import sys
import pyopencl as cl
import numpy

from PIL import Image

def infiniteFocus(images, depth, clContext, clQueue):
    if not hasattr(infiniteFocus, "program"):
        kernelFile = open('src/kernels/infiniteFocus.cl', 'r')
        infiniteFocus.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags

    depth = numpy.asarray(depth).astype(numpy.uint8)
    output = numpy.zeros((images[0].size[1], images[0].size[0])).astype(numpy.uint8)
    depthBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=depth)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

    for currentImage in range(len(images)):
        input = numpy.asarray(images[currentImage]).astype(numpy.uint8)
        inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)

        infiniteFocus.program.infiniteFocus(clQueue, [images[0].size[0] * images[0].size[1]], None, inputBuffer, outputBuffer, depthBuffer, numpy.uint32(images[0].size[0]), numpy.uint32(images[0].size[1]), numpy.uint32(len(images)), numpy.uint32(currentImage)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    outputImage = Image.fromarray(output)

    return outputImage
