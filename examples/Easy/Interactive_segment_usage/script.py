# exampleE11.py
# IN snake.png
# OUT interseg_snap.png

## TITLE #######################################################################
# mambaDisplay.extra interactive segment usage

## DESCRIPTION #################################################################
# This is a small demonstration of the mambaDisplay.extra interactive
# segmentation GUI. It allows you to segment an image using the watershed
# algorithm (processing the gradient image) with user-defined markers. Its
# behavior is very similar to the magic selection you can find in image
# processing programs such as GIMP.

## SCRIPT ######################################################################
# Importing mamba and mambaDisplay.extra
from mamba import *
import mambaDisplay.extra

# Opening an image
im = imageMb('snake.png')
# The 32-bit image in which the segmentation result will be placed
imSeg = imageMb(im, 32)

# Calling the interactive segmentation GUI
#
# This will block script progression until you hit the close button.
# To create a marker simply click on the image. If you do that
# while pressing the control button on your keyboard, the marker
# will be a line between your previous click on the new one (creating a
# unique marker). The function return the list of markers.
#
# Of course the display can be zoom in or out and has most of the 
# functionalities available in the standard mamba display.
print(mambaDisplay.extra.interactiveSegment(im, imSeg))
