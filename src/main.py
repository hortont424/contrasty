#!/usr/bin/env python -Wall

from PIL import Image

import autofocus

def main():
    image = Image.new("RGBA", (100, 100))

    filteredImage = autofocus.contrastFilter(image)

if __name__ == '__main__':
    main()