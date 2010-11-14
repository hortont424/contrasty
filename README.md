Introduction
------------

Contrasty uses local contrast detection to construct an approximate depth dimension given a sequence of images taken with varying focal distances. Basically, it uses information gleaned from having a shallow depth-of-field to recreate
the scene being photographed in faux-3D.

Contrasty also implements three mechanisms for visualizing the recreated scene:

1. OpenGL depth viewer
2. Anaglyph images
3. Fake tilt-shift images

Dependencies
------------

* Python 2.6+
* PIL

Usage
-----

    ./contrasty.py --generate image1.jpg image2.jpg image3.jpg -o image.cty
    ./contrasty.py --view image.cty
    ./contrasty.py --anaglyph image.cty -o red-and-blue.jpg
    ./contrasty.py --tilt-shift image.cty <TILT-SHIFT PARAMS?!?> -o blurry-boats.jpg
