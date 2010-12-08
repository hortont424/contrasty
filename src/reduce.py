import math
import sys
import pyopencl as cl
import numpy
import numpy.numarray.nd_image

from PIL import Image

from log import *

def reduceImage(image, clContext, clQueue, buckets):
    if not hasattr(reduceImage, "program"):
        kernelFile = open('src/reduceImage.cl', 'r')
        reduceImage.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags
    input = numpy.asarray(image).astype(numpy.uint8)
    output = numpy.zeros((image.size[1], image.size[0] / buckets)).astype(numpy.uint8)
    q = numpy.zeros((image.size[1], image.size[0] / buckets)).astype(numpy.uint8)

    inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)
    qBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=q)

    reduceImage.program.reduceImage(clQueue, [(image.size[0] / buckets) * image.size[1]], None, inputBuffer, outputBuffer, qBuffer, numpy.uint32(image.size[0]), numpy.uint32(image.size[1]), numpy.uint32(buckets)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    filtered = numpy.numarray.nd_image.grey_opening(output, size=(3,3))

    outputImage = Image.fromarray(filtered)

    return outputImage
