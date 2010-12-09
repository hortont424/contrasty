#!/usr/bin/env python -Wall

import os
import sys
import re
import pyopencl as cl

from PIL import Image, ImageFilter

from filters import *

import perlEXIF

imagesDir = "/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/3"

def main():
    clContext = cl.Context(dev_type=cl.device_type.CPU)

    # Output device(s) being used for computation
    print "Running on:"
    for dev in clContext.get_info(cl.context_info.DEVICES):
        print "   ",
        print dev.get_info(cl.device_info.VENDOR),
        print dev.get_info(cl.device_info.NAME)
    print

    # Load and compile the OpenCL kernel
    clQueue = cl.CommandQueue(clContext)

    images = {}

    for root, dirs, files in os.walk(imagesDir):
        for name in files:
            filenameMatches = re.match("([0-9]+)\.(?:jpg|jpeg)", name.lower())

            if not filenameMatches:
                continue

            index = int(filenameMatches.groups(0)[0])
            filename = os.path.join(root, name)
            tags = perlEXIF.readEXIFData(filename)
            image = Image.open(filename)

            images[index] = (filename, image, tags)

    filtered = [contrastFilter(images[n][1], clContext, clQueue).resize((800,600)) for n in range(1, 1 + len(images))]
    c = mergeImages(filtered, clContext, clQueue)
    r = reduceImage(c, clContext, clQueue, len(filtered))
    f = fillImage(r, clContext, clQueue)
    o = infiniteFocus([images[n][1].resize((800,600)).convert("L") for n in range(1, 1 + len(images))], f, clContext, clQueue)

    o.show()
    o.save("asdf.jpg")

if __name__ == '__main__':
    main()