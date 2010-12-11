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

    depthBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=depth)

    outputR = numpy.zeros(depth.shape).astype(numpy.uint8)
    outputG = numpy.zeros(depth.shape).astype(numpy.uint8)
    outputB = numpy.zeros(depth.shape).astype(numpy.uint8)
    outputRBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=outputR)
    outputGBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=outputG)
    outputBBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=outputB)

    for currentImage in range(len(images)):
        r, g, b = [a.copy() for a in images[currentImage].transpose(2, 0, 1)]

        rBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=r)
        gBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=g)
        bBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=b)

        infiniteFocus.program.infiniteFocus(clQueue, [depth.size], None, rBuffer, outputRBuffer, depthBuffer, numpy.uint32(currentImage)).wait()
        infiniteFocus.program.infiniteFocus(clQueue, [depth.size], None, gBuffer, outputGBuffer, depthBuffer, numpy.uint32(currentImage)).wait()
        infiniteFocus.program.infiniteFocus(clQueue, [depth.size], None, bBuffer, outputBBuffer, depthBuffer, numpy.uint32(currentImage)).wait()

    cl.enqueue_read_buffer(clQueue, outputRBuffer, outputR).wait()
    cl.enqueue_read_buffer(clQueue, outputGBuffer, outputG).wait()
    cl.enqueue_read_buffer(clQueue, outputBBuffer, outputB).wait()

    rgb = numpy.array((outputR, outputG, outputB)).transpose(1, 2, 0)

    return rgb

@logCall
def anaglyph(image, depth, clContext, clQueue):
    if not hasattr(infiniteFocus, "program"):
        kernelFile = open('src/kernels/anaglyph.cl', 'r')
        anaglyph.program = cl.Program(clContext, kernelFile.read()).build()
        kernelFile.close()

    mf = cl.mem_flags

    depthBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=depth)

    outputR = numpy.zeros(depth.shape).astype(numpy.uint8)
    outputG = numpy.zeros(depth.shape).astype(numpy.uint8)
    outputB = numpy.zeros(depth.shape).astype(numpy.uint8)
    outputRBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=outputR)
    outputGBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=outputG)
    outputBBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=outputB)

    r, g, b = [a.copy() for a in image.transpose(2, 0, 1)]

    rBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=r)
    gBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=g)
    bBuffer = cl.Buffer(clContext, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=b)

    anaglyph.program.anaglyph(clQueue, [depth.size], None, rBuffer, outputRBuffer, depthBuffer, numpy.uint32(image.shape[1]), numpy.uint32(image.shape[0]), numpy.int32(-1)).wait()
    anaglyph.program.anaglyph(clQueue, [depth.size], None, gBuffer, outputGBuffer, depthBuffer, numpy.uint32(image.shape[1]), numpy.uint32(image.shape[0]), numpy.int32(1)).wait()
    anaglyph.program.anaglyph(clQueue, [depth.size], None, bBuffer, outputBBuffer, depthBuffer, numpy.uint32(image.shape[1]), numpy.uint32(image.shape[0]), numpy.int32(1)).wait()

    cl.enqueue_read_buffer(clQueue, outputRBuffer, outputR).wait()
    cl.enqueue_read_buffer(clQueue, outputGBuffer, outputG).wait()
    cl.enqueue_read_buffer(clQueue, outputBBuffer, outputB).wait()

    rgb = numpy.array((outputR, outputG, outputB)).transpose(1, 2, 0)

    return rgb
