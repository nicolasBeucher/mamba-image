# exampleE8.py
# IN snake.png
# OUT dynamicThreshold_snap.png

## TITLE #######################################################################
# mambaDisplay.extra Dynamic thresholder usage

## DESCRIPTION #################################################################
# This is a small demonstration of the mambaDisplay.extra dynamic thresholder
# GUI. It allows you to search manually for the best threshold value.

## SCRIPT ######################################################################
# Importing mamba and mambaDisplay.extra
from mamba import *
import mambaDisplay.extra

# Opening an image
im = imageMb('snake.png')

# Calling the dynamic threshold GUI
# This will block script progression until user hit the close button
# You can change the threshold values by using keys q, s, w and x. Of course
# the display can be zoom in or out and has most of the functionalities
# available in the standard mamba display.
tvals = mambaDisplay.extra.dynamicThreshold(im)

# The value obtained can be then used to compute a binary
# image with the threshold value (upper and lower threshold)
thresh = imageMb(im, 1)
threshold(im, thresh, *tvals)
