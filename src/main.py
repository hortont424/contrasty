#!/usr/bin/env python -Wall

import os
import sys
import re
import pyopencl as cl

from PIL import Image, ImageFilter

import autofocus
import breathing
import reduce
import merge
import fill
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
            image = Image.open(filename)#.resize((800,600))

            images[index] = (filename, image, tags)

    #for (filename, image, tags) in [images[key] for key in sorted(images.iterkeys())]:
    #    input = image.copy()
    #    #input = breathing.breathingCorrection(input, float(tags["FocusDistance"].split(" ")[0]))
    #    #input.save(os.path.basename(filename))
    #
    #    output = autofocus.contrastFilter(input, clContext, clQueue, size=20)
    #    output.save(os.path.basename(filename))

    filtered = [autofocus.contrastFilter(images[n][1], clContext, clQueue, size=20).resize((800,600)) for n in range(1, 1 + len(images))]
    c = merge.mergeImages(filtered, clContext, clQueue)
    r = reduce.reduceImage(c, clContext, clQueue, len(filtered))
    f = fill.fillImage(r, clContext, clQueue)

    f.show()
    f.save("asdf.jpg")

if __name__ == '__main__':
    main()