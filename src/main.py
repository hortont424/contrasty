#!/usr/bin/env python

import os
import sys
import re
import numpy
import pyopencl as cl
import cPickle as pickle

from optparse import OptionParser # deprecated in Python 2.7...
from PIL import Image

from log import *
from perlEXIF import *
from image import *

import filters

def setupOpenCL():
    clContext = cl.Context(dev_type=cl.device_type.CPU)

    # Output device(s) being used for computation
    devices = "OpenCL on: "
    for dev in clContext.get_info(cl.context_info.DEVICES):
        devices += re.sub("\s+", " ", dev.get_info(cl.device_info.NAME)) + " "

    log(devices, priority=Priority.LOW)

    # Load and compile the OpenCL kernel
    clQueue = cl.CommandQueue(clContext)

    return (clContext, clQueue)

@logCall
def cmdGenerate(options):
    clContext, clQueue = setupOpenCL()
    images = {}

    if not os.path.isdir(options.input):
        print options.input, "is not a valid input directory"
        sys.exit(os.EX_NOINPUT)

    outputPrefix = os.path.splitext(options.output)[0]

    for root, dirs, files in os.walk(options.input):
        for name in files:
            filenameMatches = re.match("([0-9]+)\.(?:jpg|jpeg)", name.lower())

            if not filenameMatches:
                continue

            index = int(filenameMatches.groups(0)[0])
            filename = os.path.join(root, name)
            tags = readEXIFData(filename)

            image = PILToNumpy(Image.open(filename))
            bcImage = filters.breathingCorrection(image, float(tags["FocusDistance"].split(" ")[0]))

            NumpyToPIL(bcImage).save("{0}-bc-{1}.jpg".format(outputPrefix, index))

            images[index] = (filename, bcImage, tags)

    # we're throwing out all sorts of information by converting to greyscale
    filtered = [filters.contrastFilter(PILToNumpy(NumpyToPIL(images[n][1]).convert("L")), clContext, clQueue) for n in range(1, 1 + len(images))]
    merged = filters.mergeImages(filtered, clContext, clQueue)
    reduced = filters.reduceImage(merged, clContext, clQueue, len(filtered))
    depth = filters.fillImage(reduced, clContext, clQueue)

    for i, filteredImage in enumerate(filtered):
        NumpyToPIL(filteredImage).save("{0}-filtered-{1}.jpg".format(outputPrefix, i))

    NumpyToPIL(merged).save("{0}-merged.jpg".format(outputPrefix))
    Image.eval(NumpyToPIL(reduced), lambda x: x * (255 / len(filtered))).save("{0}-reduced.jpg".format(outputPrefix))
    Image.eval(NumpyToPIL(depth), lambda x: x * (255 / len(filtered))).save("{0}-depth.jpg".format(outputPrefix))
    NumpyToPIL(depth).save("{0}-rawdepth.jpg".format(outputPrefix))

    image3D = Image3D()
    image3D.sourceDirectory = options.input
    image3D.images = [images[n][1] for n in range(1, 1 + len(images))]
    image3D.depth = depth

    if options.output:
        outputFile = open(options.output, "w")

        if not outputFile:
            print "Failed to open output file!"
            sys.exit(os.EX_OSFILE)

        pickle.dump(image3D, outputFile)
    else:
        print "No output file specified, discarding."

@logCall
def cmdInfiniteFocus(options):
    clContext, clQueue = setupOpenCL()

    inputFile = open(options.input, "r")

    if not inputFile:
        print "Failed to open input file!"
        sys.exit(os.EX_OSFILE)

    image3D = pickle.load(inputFile)

    o = filters.infiniteFocus(image3D.images, image3D.depth, clContext, clQueue)

    if options.output:
        NumpyToPIL(o).save(options.output)
    else:
        print "No output file specified, discarding."

def cmdViewerDrawCallback(img, depth):
    from OpenGL.GL import glBegin, glColor4f, glVertex3f, glEnd

    def cb():
        glBegin(GL_POINTS)
        for idx, val in numpy.ndenumerate(PILToNumpy(NumpyToPIL(img).convert("L"))):
            glColor4f(float(val) / 255.0, float(val) / 255.0, float(val) / 255.0, 1.0)
            glVertex3f(idx[1], img.shape[0] - idx[0], float(depth[idx[0],idx[1]]))
        glEnd()

    return cb

@logCall
def cmdViewer(options):
    import viewer

    prefix = os.path.splitext(options.input)[0]

    # depends on --infinite-focus having already been run!
    img = PILToNumpy(Image.open("{0}-inf.jpg".format(prefix)).resize((800,600)))
    depth = PILToNumpy(Image.open("{0}-rawdepth.jpg".format(prefix)).resize((800,600)))
    v = viewer.Viewer(cmdViewerDrawCallback(img, depth))

@logCall
def cmdAnaglyph(options):
    clContext, clQueue = setupOpenCL()

    prefix = os.path.splitext(options.input)[0]

    img = PILToNumpy(Image.open("{0}-inf.jpg".format(prefix)))
    depth = PILToNumpy(Image.open("{0}-depth.jpg".format(prefix)))

    o = filters.anaglyph(img, depth, clContext, clQueue)

    if options.output:
        NumpyToPIL(o).save(options.output)
    else:
        print "No output file specified, discarding."

def main():
    parser = OptionParser()
    parser.add_option("-g", "--generate", dest="generate", action="store_true", default=False,
                      help="Generate a 3D image from a set of 2D images")
    parser.add_option("-f", "--infinite-focus", dest="infiniteFocus", action="store_true", default=False,
                      help="Generate a 2D image with a small virtual aperture from a 3D image")
    parser.add_option("-v", "--view", dest="viewer", action="store_true", default=False,
                      help="Show the 3D image in an OpenGL view")
    parser.add_option("-a", "--anaglyph", dest="anaglyph", action="store_true", default=False,
                      help="Generate an anaglyph 3D image from a 3D image")
    parser.add_option("-o", "--output", dest="output",
                      help="Write output to file")
    (options, args) = parser.parse_args()

    if not len(args) is 1:
        print "Too many input arguments: ", args
        sys.exit(os.EX_USAGE)

    options.input = args[0]

    if options.generate:
        cmdGenerate(options)
    elif options.infiniteFocus:
        cmdInfiniteFocus(options)
    elif options.viewer:
        cmdViewer(options)
    elif options.anaglyph:
        cmdAnaglyph(options)

if __name__ == '__main__':
    main()
