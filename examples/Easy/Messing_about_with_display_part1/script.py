# exampleE2.py
# IN snake.png
# OUT display.png

## TITLE #######################################################################
# Messing about with display, part 1 : activation

## DESCRIPTION #################################################################
# This example shows you how to activate the display and presents some of the 
# options related to the display. This example is meant to be replayed inside a 
# Python console. If you run directly this script, nothing will happen.

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *
import mambaDisplay

# Loading an image
im = imageMb('snake.png')

# Activating the display. This will make a window appear
im.show()

# You can deactivate the display at all time by either
# - Closing the window
# - Calling the appropriate method like this
im.hide()

# Reactivate it
im.show()

# You can update the display (if your image changed) by calling the following
# method
im.update()
# This action is automatically performed by every Mamba functions so it is 
# likely you will not have to use it on your own

# The two last methods related to display allow you to freeze/unfreeze the 
# display to prevent mamba updating it but keeping the window visible.
im.freeze() # <- the display is no longer updated
im.unfreeze() # <- the display will be updated (and returns to what the
# image looks like if there were modifications)

# Sometimes, you will have lots of images opened and displayed making it quite
# messy on your desktop and thus very difficult to read and analyze. To make 
# sure displays are properly organised you can call the following function
mambaDisplay.tidyDisplays()
# The function does not do miracles (like increasing your screen resolution) so
# don't have too much expectations

