#!/usr/bin/env python -Wall

import pyopencl as cl

from PIL import Image, ImageFilter

import autofocus

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

    inFocus = Image.open("/Volumes/MCP/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/1/7.jpg")
    inFocusFiltered = autofocus.contrastFilter(inFocus, clContext, clQueue, size=20)

if __name__ == '__main__':
    main()