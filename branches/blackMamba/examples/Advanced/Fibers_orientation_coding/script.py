# exampleA23.py
# IN fiber.png
# OUT coded_directions.png

## TITLE #######################################################################
# Fibers orientation coding

## DESCRIPTION #################################################################
# This example shows how to use the directional operators defined in example
# entitled "Directional morphological operators in 12 or 16 directions"
# to detect and code the orientation of fibers. This application is performed in
# two steps. The first step consists in determining the maximum elongation of
# each fiber in a given direction. This is performed by a directional ultimate
# opening. In the second step, the direction which, at each point, corresponds to
# the maximum elongation is given to this point. This example is applied to a
# binary image and on an hexagonal grid (6 directions are encoded).

## SCRIPT ######################################################################
# Importing mamba
import mamba

# The basic operators of example M20 are used again.
def conjugateDirectionalErode(imIn, imOut, d, size,
                              grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
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
    
def directionalErode(imIn, imOut, d, size,
                     grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
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
def conjugateDirectionalDilate(imIn, imOut, d, size,
                               grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
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
    
def directionalDilate(imIn, imOut, d, size,
                      grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
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

# Definition of the linear ultimate opening.
def linearUltimateOpen(imIn, imOut, d, grid=mamba.DEFAULT_GRID):
    """
    This operator performs the ultimate directional opening of the binary image
    'imIn' in direction 'd' and puts the result in the 32-bit image 'imOut'.
    The value of 'imOut' at each point of 'imIn' corresponds to the length of the
    intercept passing through this point.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    
    size = 0
    imOut.reset()
    mamba.copy(imIn, imWrk1)
    while mamba.computeVolume(imWrk1) != 0:
        size += 1
        directionalErode(imWrk1, imWrk1, d, 1, grid=grid, edge=mamba.EMPTY)
        td = (d + mamba.gridNeighbors(grid) - 1) % (mamba.gridNeighbors(grid) * 2) + 1
        directionalDilate(imWrk1, imWrk2, td, size, grid=grid)
        mamba.add(imOut, imWrk2, imOut)

#
def directionalCoding(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Coding of the direction which, at each point of 'imIn', corresponds to the
    direction of the maximal intercept through this point. The result of this
    coding is put in the grey scale image 'imOut'.
    6 directions are coded on the hexagonal grid, 8 on the square one.
    """
    imWrk1 = mamba.imageMb(imIn, 32)
    imWrk2 = mamba.imageMb(imIn, 32)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 8)
    
    imOut.reset()
    imWrk1.reset()
    for i in range(mamba.gridNeighbors(grid=grid)):
        d = i + 1
        linearUltimateOpen(imIn, imWrk2, d, grid=grid)
        mamba.generateSupMask(imWrk2, imWrk1, imWrk3, True)
        mamba.logic(imWrk2, imWrk1, imWrk1, "sup")
        mamba.convertByMask(imWrk3, imWrk4, 0, d)
        mamba.logic(imWrk4, imOut, imOut, "sup")       

# Trying these operators on a fiber image.
# Loading the initial image.
im1 = mamba.imageMb('fiber.png')
# Defining some working images.
im2 = mamba.imageMb(im1)
imbin1 = mamba.imageMb(im1, 1)
# A binary image is defined by a top-hat operator, followed by
# a thresholding and a filtering.
mamba.blackTopHat(im1, im2, 10)
mamba.threshold(im2, imbin1, 50, 255)
mamba.buildClose(imbin1, imbin1, 2)
# The directions encoding is performed.
directionalCoding(imbin1, im2)
# A palette for displaying the 6 possible directions is defined.
dirpal = (0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255)
for i in range(249):
    dirpal = dirpal + (0, 0, 0)
# The result is saved with the palette.
im2.save('coded_directions.png', palette=dirpal)



    
