# exampleE9.py
# IN coffee_grains.jpg
# OUT superpose_snap.png

## TITLE #######################################################################
# mambaExtra superposer usage

## DESCRIPTION #################################################################
# This is a small demonstration of the mambaExtra superposer
# GUI. It allows you to display two images at the same time in a
# superposed manner.

## SCRIPT ######################################################################
# Importing the mamba module and of course the mambaExtra module
from mamba import *
import mamba.extra

# Opening an image
im = imageMb('coffee_grains.jpg')
# To create a superposable image we will generate a binary threshold image
thresh = imageMb(im, 1)
threshold(im, thresh, 0, 128)

# Calling the superposer GUI
# This will block script progression until user hit the close button
# You can change the color in the legend.
# Of course the display can be zoom in or out and has most of the 
# functionalities available in the standard mamba display.
mamba.extra.superpose(im, thresh)
