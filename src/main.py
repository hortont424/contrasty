#!/usr/bin/env python -Wall

from PIL import Image

import autofocus

def main():
    notInFocus = Image.open("/Users/hortont/Desktop/focus/1/1.jpg")
    inFocus = Image.open("/Users/hortont/Desktop/focus/1/7.jpg")

    notInFocusFiltered = autofocus.contrastFilter(notInFocus)
    notInFocusFiltered.show()

if __name__ == '__main__':
    main()