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
    input = numpy.asarray(image).astype(numpy.uint8)
    output = numpy.zeros((image.size[1], image.size[0])).astype(numpy.uint8)

    while len(numpy.flatnonzero(output)) < (image.size[0] * image.size[1]) - 1:
        output = numpy.zeros((image.size[1], image.size[0])).astype(numpy.uint8)

        inputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=input)
        outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)

        fillImage.program.fillImage(clQueue, [image.size[0] * image.size[1]], None, inputBuffer, outputBuffer, numpy.uint32(image.size[0]), numpy.uint32(image.size[1])).wait()

        cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

        input = output

    output = nd_image.grey_opening(nd_image.grey_closing(output, size=(9,9)), size=(9,9))

    outputImage = Image.fromarray(output)

    return outputImage
