# exampleM13.py
# IN wheel.png
# OUT wheel_teeth.png

## TITLE #######################################################################
# Counting and marking teeth of a notched wheel

## DESCRIPTION #################################################################
# This example shows how a very simple transformation (opening here) can solve
# a problem of detection and counting of the teeth of a notched wheel when it is 
# associated to a preliminary selection of the zone where these teeth should be.

## SCRIPT ######################################################################
# Importing mamba
import mamba
import mambaDisplay

im = mamba.imageMb("wheel.png", 1)
im1 = mamba.imageMb(im, 1)
im2 = mamba.imageMb(im, 1)

# Opening of image
mamba.opening(im, im1, 3)
# Selection of the outside region
mamba.negate(im1, im2)
mamba.removeEdgeParticles(im2, im1)
mamba.diff(im2, im1, im2)
# Extracting the wheel teeth
mamba.logic(im, im2, im2, "inf")
# Cleaning the image
mamba.opening(im2, im2)
# Counting and marking each tooth
mamba.thinD(im2, im1)
nb_teeth = mamba.computeVolume(im1)
print("Number of teeth: %d" % (nb_teeth))
mamba.dilate(im1, im1, 3, mamba.SQUARE3X3)
im1.convert(8)
im8 = mamba.imageMb(im, 8)
mamba.convert(im, im8)
mamba.subConst(im8, 1, im8)
mamba.logic(im8, im1, im8, "sup")
name = mambaDisplay.tagOneColorPalette(255, (0,0,255))
im8.save('wheel_teeth.png', palette=mambaDisplay.getPalette(name))
