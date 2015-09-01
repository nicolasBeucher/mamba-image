# exampleM10.py
# IN particles.png
# OUT particles_nbg.png

## TITLE #######################################################################
# Pixel neighbors counter

## DESCRIPTION #################################################################
# This example shows how to use the hit-or-miss operator along with the
# double structuring element class in Mamba to count the number of neighbors
# set to true each true pixel has.

## SCRIPT ######################################################################
# Importing the mamba package
import mamba

def neighborCounter(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    For each pixel set to true in the binary image 'imIn', this function
    counts its neighbor set to true and puts the result in 'imOut'. The
    neighbors are selected according to 'grid'.
    """

    imWrk = mamba.imageMb(imIn)
    imOut.reset()
    
    for d in mamba.getDirections(grid)[1:]:
        dse = mamba.doubleStructuringElement([],[0,d],grid)
        mamba.hitOrMiss(imIn, imWrk, dse)
        mamba.add(imOut, imWrk, imOut)
    
im = mamba.imageMb("particles.png", 1)
imCount = mamba.imageMb(im, 8)
neighborCounter(im, imCount, mamba.SQUARE)
# Creating a specific palette to see more clearly the possible values
# wich range from 0 to 8 for a square grid.
palette = (0,0,0,255,0,0,0,255,0,255,128,0,0,255,128,255,255,0,0,255,255,128,255,0,0,128,255)+247*(0,0,0)
imCount.save("particles_nbg.png", palette=palette)

