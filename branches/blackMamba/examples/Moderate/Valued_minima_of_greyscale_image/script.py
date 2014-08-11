# exampleM2.py
# IN snake.png
# OUT snake_valmin.png

## TITLE #######################################################################
# Valued minima of a greyscale image

## DESCRIPTION #################################################################
# This example is a small variation of the minima function found in the
# mamba extrema module. It shows that there are various possibilities
# to attain the same result in Mamba.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
import mambaDisplay

def valuedMinima(imIn, imOut, h=1, grid=DEFAULT_GRID):
    """
    Computes the valued minima of 'imIn' using a dual build operation and 
    puts the result in 'imOut'.
    
    'h' can be used to define the minima depth. Grid used by the dual build 
    operation can be specified by 'grid'.
    
    Only works with greyscale images as input and output.
    """
    
    imWrk = imageMb(imIn)
    imWrk_bin = imageMb(imIn, 1)
    copy(imIn, imWrk)
    addConst(imWrk, h, imWrk)
    hierarDualBuild(imIn, imWrk, grid=grid)
    sub(imWrk, imIn, imWrk)
    threshold(imWrk, imWrk_bin, 1, computeMaxRange(imIn)[1])
    mul(imWrk_bin, imIn, imOut)

# Opening and creating images 
im1 = imageMb('snake.png')
im2 = imageMb(im1)

# Computing the valued minima
valuedMinima(im1, im2)

im2.save("snake_valmin.png", palette=mambaDisplay.getPalette("rainbow"))
