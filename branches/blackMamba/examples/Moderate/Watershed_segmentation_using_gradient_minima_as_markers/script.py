# exampleM3.py
# IN snake.png
# OUT snake_watmin.png

## TITLE #######################################################################
# Watershed segmentation using gradient minima as markers

## DESCRIPTION #################################################################
# In this example, the watershed line is computed on the gradient image
# using its minima as a marker image. The resulting image is then superposed
# to the original to show the possibilities offered by some of the palette
# extra function.

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *
import mambaDisplay

def watershedByGradMinima(imIn, imOut, grid=DEFAULT_GRID):
    """
    Computes the watershed line of imIn using its gradient minima as a marker
    image
    """
    grad = imageMb(imIn, 8)
    marker = imageMb(imIn, 32)
    minbin = imageMb(imIn, 1)
    gradient(imIn, grad)
    minima(grad, minbin, grid=grid)
    label(minbin, marker, grid=grid)
    watershedSegment(grad, marker, grid=grid)
    copyBytePlane(marker, 3, imOut)

# Opening and creating images 
im1 = imageMb('snake.png')
im2 = imageMb(im1)
im3 = imageMb(im1)

# Computing the watershed by minima marker
watershedByGradMinima(im1, im2)

# For a better view the watershed line is superposed on the original image
subConst(im1, 1, im3)
# The watershed line is set to 255 and the basins are empty in im2.
logic(im3, im2, im3, "sup")
# a special palette is created
name = mambaDisplay.tagOneColorPalette(255, (255,0,0))
im3.save("snake_watmin.png", palette=mambaDisplay.getPalette(name))
