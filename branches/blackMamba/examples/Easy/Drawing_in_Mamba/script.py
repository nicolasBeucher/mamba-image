# exampleE6.py
# OUT draw_line.png draw_square.png draw_circle.png

## TITLE #######################################################################
# Drawing in Mamba

## DESCRIPTION #################################################################
# These examples show some of the drawing functions available in Mamba.

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *

# Creating a default image, 256x256 8-bit image
im = imageMb()

# Drawing a line. The line is drawn according to the given
# 4 value tuple interpreted as (x_start, y_start, x_stop, y_stop).
# So, in our case, the line goes from point (45,163) to point (221,8)
drawLine(im, (45,163,221,8), 180)
im.save("draw_line.png")


im.reset()
# Drawing a square (actually a rectangle) filled with value 160.
# The middle tuple indicates from where to where the square extends
drawSquare(im, (120,15,160,95), 160)
# Drawing another square filled with value 220. Notice that this
# square overlaps the first one. The last drawn is always on top
# of the others
drawSquare(im, (50,80,200,180), 220)
im.save("draw_square.png")

im.reset()
# Drawing an empty circle centered in the middle of the image with a 
# radius of 50 and white (255).
drawCircle(im, (128,128,50), 255)
# Then drawing a filled circle.
drawFillCircle(im, (128,128,20), 255)
im.save("draw_circle.png")

