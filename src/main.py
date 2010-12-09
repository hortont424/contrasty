#!/usr/bin/env python -Wall

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

    for root, dirs, files in os.walk(options.input):
        for name in files:
            filenameMatches = re.match("([0-9]+)\.(?:jpg|jpeg)", name.lower())

            if not filenameMatches:
                continue

            index = int(filenameMatches.groups(0)[0])
            filename = os.path.join(root, name)
            tags = readEXIFData(filename)

            # we're throwing out all sorts of information by converting to greyscale
            image = PILToNumpy(Image.open(filename).convert("L"))

            images[index] = (filename, image, tags)

    # 906x600 keeps aspect ratio better... should figure size from input size

    filtered = [PILToNumpy(NumpyToPIL(filters.contrastFilter(images[n][1], clContext, clQueue)).resize((800,600))) for n in range(1, 1 + len(images))]
    merged = filters.mergeImages(filtered, clContext, clQueue)
    reduced = filters.reduceImage(merged, clContext, clQueue, len(filtered))
    depth = filters.fillImage(reduced, clContext, clQueue)

    image3D = Image3D()
    image3D.sourceDirectory = options.input
    image3D.images = [PILToNumpy(NumpyToPIL(images[n][1]).resize((800,600))) for n in range(1, 1 + len(images))]
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

def main():
    parser = OptionParser()
    parser.add_option("-g", "--generate", dest="generate", action="store_true", default=False,
                      help="Generate a 3D image from a set of 2D images")
    parser.add_option("-f", "--infinite-focus", dest="infiniteFocus", action="store_true", default=False,
                      help="Generate a 2D image with a small virtual aperture from a 3D image")
    parser.add_option("-o", "--output", dest="output",
                      help="Write output to file")
    (options, args) = parser.parse_args()

    if not len(args) is 1:
        print "Too many input arguments: ", args
        sys.exit(os.EX_USAGE)

    options.input = args[0]

    if options.generate:
        cmdDenerate(options)
    elif options.infiniteFocus:
        cmdInfiniteFocus(options)

if __name__ == '__main__':
    main()