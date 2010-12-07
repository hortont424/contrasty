import math
import sys
import pyopencl as cl
import numpy

from PIL import Image

from log import *

def mergeImages(images, clContext, clQueue):
    if not hasattr(mergeImages, "program"):
        kernelFile = open('src/mergeImages.cl', 'r')
        mergeImages.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags

    output = numpy.zeros((images[0].size[1], images[0].size[0] * len(images))).astype(numpy.uint8)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

    for currentImage in range(len(images)):
        input = numpy.asarray(images[currentImage]).astype(numpy.uint8)
        inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)

        mergeImages.program.mergeImages(clQueue, [images[0].size[0] * images[0].size[1]], None, inputBuffer, outputBuffer, numpy.uint32(images[0].size[0]), numpy.uint32(images[0].size[1]), numpy.uint32(len(images)), numpy.uint32(currentImage)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    outputImage = Image.fromarray(output)

    return outputImage
