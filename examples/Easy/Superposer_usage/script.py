# exampleE9.py
# IN coffee_grains.jpg
# OUT superpose_snap.png

## TITLE #######################################################################
# mambaDisplay.extra superposer usage

## DESCRIPTION #################################################################
# This is a small demonstration of the mambaDisplay.extra superposer
# GUI. It allows you to display two images at the same time in a
# superposed manner.

## SCRIPT ######################################################################
# Importing mamba and mambaDisplay.extra
from mamba import *
import mambaDisplay.extra

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
mambaDisplay.extra.superpose(im, thresh)
