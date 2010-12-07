import math
import sys
import pyopencl as cl
import numpy

from PIL import Image

from log import *

def reduceImages(image1, image2, clContext, clQueue): # TODO: take all images, run multiple shots through
    if not hasattr(reduceImages, "program"):
        kernelFile = open('src/reduceImages.cl', 'r')
        reduceImages.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    # we're throwing out all sorts of information by converting to greyscale
    image1 = image1.convert("L")
    image2 = image2.convert("L")

    mf = cl.mem_flags
    input1 = numpy.asarray(image1).astype(numpy.uint8)
    input2 = numpy.asarray(image2).astype(numpy.uint8)
    output = numpy.zeros((image1.size[1], image1.size[0])).astype(numpy.uint8)

    input1Buffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input1)
    input2Buffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input2)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

    reduceImages.program.reduceImages(clQueue, [image1.size[0] * image1.size[1]], None, input1Buffer, input2Buffer, outputBuffer, numpy.uint32(image1.size[0]), numpy.uint32(image1.size[1])).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    outputImage = Image.fromarray(output)

    return outputImage
