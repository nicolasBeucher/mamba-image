# exampleM20.py
# IN ferrite.png
# OUT oriented_fibers.png

## TITLE #######################################################################
# Directional morphological operators in 12 or 16 directions

## DESCRIPTION #################################################################
# These transformations use linear structuring elements defined on standard or
# conjugate directions of the grid in use. These operators (erosion, dilation,
# opening, closing) are often useful to increase the accuracy of the detection
# and extraction of oriented objects in an image. The following operators can be
# used on an hexagonal grid (12 directions are available) or on a square one (16
# directions are defined). The directions coding is the same in both cases:
# direction 1 corresponds to the same direction as in the grid in use (12 o'clock
# for the square grid and 1 o'clock for the hexagonal one), the numbering
# increasing clockwise up to 12 or 16.

## SCRIPT ######################################################################
# Importing mamba
import mamba
import mambaDisplay.extra as mE

# This operator is used by the general directional erosion.
def conjugateDirectionalErode(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs the erosion of image 'imIn' in the conjugate direction 'd' of the
    grid and puts the result in image 'imOut'. The images can be binary, greyscale
    or 32-bit images. 'size' is a multiple of the distance between two adjacent
    points in the conjugate directions. 'edge' is set to FILLED by default (can
    be changed).
    Note that this operator is not equivalent to successive erosions by a doublet
    of points.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)

    j3 = mamba.transposeDirection(d, grid=grid)
    j2 = mamba.rotateDirection(d, grid=grid)
    j1 = mamba.transposeDirection(j2, grid=grid)
    val = mamba.computeMaxRange(imIn)[1] * int(edge == mamba.FILLED)
    for i in range(size):
        mamba.copy(imOut, imWrk1)
        mamba.copy(imOut, imWrk2)
        mamba.linearErode(imWrk1, imWrk1, d, n=1, grid=grid, edge=edge)
        mamba.shift(imWrk1, imWrk1, j1, 1, val, grid=grid)
        mamba.logic(imWrk1, imOut, imWrk1, "inf")
        mamba.linearErode(imWrk2, imWrk2, j2, n=1, grid=grid, edge=edge)
        mamba.shift(imWrk2, imWrk2, j3, 1, val, grid=grid)
        mamba.logic(imWrk2, imOut, imWrk2, "inf")
        mamba.logic(imWrk1, imWrk2, imOut, "sup")
    
def directionalErode(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    General directional erosion of image 'imIn', result in 'imOut'. The images
    can have any format. The direction 'd' is coded clockwise from 1 to 12 or
    16. Direction 1 corresponds to 60 degrees on the hexagonal grid and 90
    degrees on the square grid. 'size' corresponds to twice the normal size
    when standard directions are used. 'edge' is set to FILLED by default.
    """
    
    if (d & 1) == 0:
        conjugateDirectionalErode(imIn, imOut, d/2, size, grid=grid, edge=edge)
    else:
        mamba.linearErode(imIn, imOut, (d+1)/2, size*2, grid=grid, edge=edge) 

# similar operators are defined for the dilation.
def conjugateDirectionalDilate(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Performs the dilation of image 'imIn' in the conjugate direction 'd' of the
    grid and puts the result in image 'imOut'. The images can be binary, greyscale
    or 32-bit images. 'size' is a multiple of the distance between two adjacent
    points in the conjugate directions. 'edge' is set to EMPTY by default (can
    be changed).
    Note that the linear structuring element is not connected. Points connecting
    adjacent points in the conjugate directions are not present. This is normal
    if we want to insure that the result is identical when we iterate n size 1
    operations to get a size n one (the same remark applies to the erosion).
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    
    j3 = mamba.transposeDirection(d, grid=grid)
    j2 = mamba.rotateDirection(d, grid=grid)
    j1 = mamba.transposeDirection(j2, grid=grid)
    val = mamba.computeMaxRange(imIn)[1] * int(edge == mamba.FILLED)
    for i in range(size):
        mamba.copy(imOut, imWrk1)
        mamba.copy(imOut, imWrk2)
        mamba.linearDilate(imWrk1, imWrk1, d, 1, grid=grid, edge=edge)
        mamba.shift(imWrk1, imWrk1, j1, 1, val, grid=grid)
        mamba.logic(imWrk1, imOut, imWrk1, "sup")
        mamba.linearDilate(imWrk2, imWrk2, j2, 1, grid=grid, edge=edge)
        mamba.shift(imWrk2, imWrk2, j3, 1, val, grid=grid)
        mamba.logic(imWrk2, imOut, imWrk2, "sup")
        mamba.logic(imWrk1, imWrk2, imOut, "inf")
    
def directionalDilate(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    General directional dilation of image 'imIn', result in 'imOut'. The images
    can have any format. The direction 'd' is coded clockwise from 1 to 12 or
    16. Direction 1 corresponds to 60 degrees on the hexagonal grid and 90
    degrees on the square grid. 'size' corresponds to twice the normal size
    when standard directions are used. 'edge' is set to EMPTY by default.
    """
    
    if (d & 1) == 0:
        conjugateDirectionalDilate(imIn, imOut, d/2, size, grid=grid, edge=edge)
    else:
        mamba.linearDilate(imIn, imOut, (d+1)/2, size*2, grid=grid, edge=edge) 

def directionalOpen(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Directional opening of image 'imIn' defined by combining an erosion in
    direction 'd' followed by a dilation in the transposed direction (which
    depends on the grid in use). Result is put in 'imOut'.
    """
    
    directionalErode(imIn, imOut, d, size, grid=grid, edge=edge)
    j = (d + mamba.gridNeighbors(grid=grid) - 1) % (mamba.gridNeighbors(grid=grid) * 2) + 1
    directionalDilate(imOut, imOut, j, size, grid=grid)

def directionalClose(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Directional closing of image 'imIn' defined by combining a dilation in
    direction 'd' followed by an erosion in the transposed direction (which
    depends on the grid in use). Result is put in 'imOut'.
    If 'edge' is set to 'EMPTY', the operation must be modified to remain extensive.
    """
    
    imWrk = mamba.imageMb(imIn)
    if edge==mamba.EMPTY:
        mamba.copy(imIn, imWrk)
    directionalDilate(imIn, imOut, d, size, grid=grid, edge=edge)
    j = (d + mamba.gridNeighbors(grid=grid) - 1) % (mamba.gridNeighbors(grid=grid) * 2) + 1
    directionalErode(imOut, imOut, j, size, grid=grid)
    if edge==mamba.EMPTY:
        mamba.logic(imOut, imWrk, imOut, "sup")

# Trying these operators on a fibers image.
# Loading the initial image.
im1 = mamba.imageMb('ferrite.png')
# Defining some working images.
im2 = mamba.imageMb(im1)
imbin1 = mamba.imageMb(im1, 1)
# Performing a directional opening of size 30 in direction 6.
# This should select fibers with a length greater than 60 in
# direction 165 degrees approximately (a square grid is used).
directionalOpen(im1, im2, 6, 30, grid=mamba.SQUARE)
# The markers (obtained by a simple threshold) of the corresponding
# fibers are superposed to the original image (some filtering is
# performed by removing fibers cutting the edges).
mamba.threshold(im2, imbin1, 100, 255)
mamba.removeEdgeParticles(imbin1, imbin1)
# The same operation is performed once again on the thresholded
# image to verify the markers sizes.
directionalOpen(imbin1, imbin1, 6, 30, grid=mamba.SQUARE)
# displaying the result.
mE.superpose(im1, imbin1)
