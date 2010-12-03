#!/usr/bin/env python -Wall

import os
import sys
import pyopencl as cl

from PIL import Image, ImageFilter

import autofocus
import breathing
import perlEXIF

def main():
    clContext = cl.Context(dev_type=cl.device_type.GPU)

    # Output device(s) being used for computation
    print "Running on:"
    for dev in clContext.get_info(cl.context_info.DEVICES):
        print "   ",
        print dev.get_info(cl.device_info.VENDOR),
        print dev.get_info(cl.device_info.NAME)
    print

    # Load and compile the OpenCL kernel
    clQueue = cl.CommandQueue(clContext)

    for root, dirs, files in os.walk("/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/1"):
        for name in files:
            if name == ".DS_Store" or name == "mask.jpg":
                continue

            filename = os.path.join(root, name)

            tags = perlEXIF.readEXIFData(filename)

            input = Image.open(filename)
            input = breathing.breathingCorrection(input, float(tags["FocusDistance"].split(" ")[0]))
            input.save(os.path.basename(filename))

            #output = autofocus.contrastFilter(input, clContext, clQueue, size=20)
            #output.save(os.path.basename(filename))



if __name__ == '__main__':
    main()