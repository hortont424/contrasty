import math
import sys
import pyopencl as cl
import numpy
import numpy.numarray.nd_image as nd_image

from PIL import Image

from log import logCall

@logCall
def reduceImage(image, clContext, clQueue, buckets):
    if not hasattr(reduceImage, "program"):
        kernelFile = open('src/kernels/reduceImage.cl', 'r')
        reduceImage.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags
    output = numpy.zeros((image.shape[0], image.shape[1] / buckets)).astype(numpy.uint8)
    q = numpy.zeros((image.shape[0], image.shape[1] / buckets)).astype(numpy.uint8)

    imageBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=image)
    outputBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=output)
    qBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=q)

    reduceImage.program.reduceImage(clQueue, [(image.shape[1] / buckets) * image.shape[0]], None, imageBuffer, outputBuffer, qBuffer, numpy.uint32(image.shape[1]), numpy.uint32(image.shape[0]), numpy.uint32(buckets)).wait()

    cl.enqueue_read_buffer(clQueue, outputBuffer, output).wait()

    filtered = nd_image.median_filter(output, size=(51,51))

    return filtered
