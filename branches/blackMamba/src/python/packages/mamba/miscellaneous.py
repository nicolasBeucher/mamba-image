"""
This module regroups functions/operators that could not be regrouped with other
operators because of their unique nature or other peculiarity. As such, it
regroups some utility functions.
"""

# Contributors: Serge BEUCHER, Nicolas BEUCHER

import mamba
import mamba.core as core
    
# Properties operators #########################################################

def compare(imIn1, imIn2, imOut):
    """
    Compares the two images 'imIn1' and 'imIn2'.
    The comparison is performed pixelwise by scanning the two images from top left
    to bottom right and it stops as soon as a pixel is different in the two images.
    The corresponding pixel in 'imOut' is set to the value of the pixel of 
    'imIn1'.
    
    The function returns a tuple holding the position of the first mismatching 
    pixel. The tuple value is (-1,-1) if the two images are identical.
    
    'imOut' is not reset at the beginning of the comparison.
    
    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    err, x, y =  core.MB_Compare(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    return (x,y)
    
def computeVolume(imIn):
    """
    Computes the volume of the image 'imIn', i.e. the sum of its pixel values.
    The computed integer value is returned by the function.
    
    'imIn' can be a 1-bit, 8-bit or 32-bit image.
    """
    err, volume = core.MB_Volume(imIn.mbIm)
    mamba.raiseExceptionOnError(err)
    return volume
    
def checkEmptiness(imIn):
    """
    Checks if image 'imIn' is empty (i.e. completely black).
    Returns True if so, False otherwise.
    
    'imIn' can be a 1-bit, 8-bit or 32-bit image.
    """
    err, isEmpty = core.MB_Check(imIn.mbIm)
    mamba.raiseExceptionOnError(err)
    return bool(isEmpty)
    
def computeMaxRange(imIn):
    """
    Returns a tuple with the minimum and maximum possible pixel values given the
    depth of image 'imIn'. The values are returned in a tuple holding the 
    minimum and the maximum.
    """
    err, min, max = core.MB_depthRange(imIn.mbIm)
    mamba.raiseExceptionOnError(err)
    return (min, max)

def computeRange(imIn):
    """
    Computes the range, i.e. the minimum and maximum values, of image 'imIn'.
    The values are returned in a tuple holding the minimum and the maximum.
    """
    err, min, max = core.MB_Range(imIn.mbIm)
    mamba.raiseExceptionOnError(err)
    return (min, max)
    
def extractFrame(imIn, threshold):
    """
    Extracts the smallest frame inside the image 'imIn' that includes all the
    pixels whose value is greater or equal to 'threshold'.
    
    'imIn' can be a 8-bit or 32-bit image.
    """
    err, x1, y1, x2, y2 = core.MB_Frame(imIn.mbIm, threshold)
    mamba.raiseExceptionOnError(err)
    return (x1, y1, x2, y2)

# Specific operators ###########################################################
  
def isotropicDistance(imIn, imOut, edge=mamba.FILLED):
    """
    Computes the distance function of a set in 'imIn'. This distance function
    uses dodecagonal erosions and the grid is assumed to be hexagonal.
    The procedure is quite slow but the result is more aesthetic.
    This operator also illustrates how to perform successive dodecagonal
    operations of increasing sizes.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.ERR_BAD_DEPTH)
    imOut.reset()
    oldn = 0
    size = 0
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk1)
    while mamba.computeVolume(imWrk1) != 0:
        mamba.add(imOut, imWrk1, imOut)
        size += 1
        n = int(0.4641*size)
        n += abs(n % 2 - size % 2)
        if (n - oldn) == 1:
            mamba.copy(imWrk1, imWrk2)
            mamba.erode(imWrk1, imWrk1, 1, se=mamba.HEXAGON, edge=edge)
        else:
            mamba.conjugateHexagonalErode(imWrk2, imWrk1, 1, edge=edge)
        oldn = n
    
def computeDistance(imIn, imOut, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Computes for each white pixel of binary 'imIn' the minimum distance to
    reach a connected component boundary while constantly staying in the set. 
    The result is put in 32-bit 'imOut'.
    
    The distance computation will be performed according to the 'grid' (HEXAGONAL
    is 6-Neighbors and SQUARE is 8-Neighbors). 'edge' can be FILLED or EMPTY.
    """

    err = core.MB_Distanceb(imIn.mbIm,imOut.mbIm, grid.id, edge.id)
    mamba.raiseExceptionOnError(err)
    imOut.update()

# Utility operators ############################################################

def drawEdge(imOut, thick=1):
    """
    Draws a frame around the edge of 'imOut' whose value equals the maximum
    range value and whose thickness is given by 'thick' (default 1).
    """
    
    imOut.reset()
    se=mamba.structuringElement([0,1,2,3,4,5,6,7,8], mamba.SQUARE)
    mamba.dilate(imOut, imOut, thick, se=se, edge=mamba.FILLED)

def shift(imIn, imOut, d, amp, fill, grid=mamba.DEFAULT_GRID):
    """
    Shifts image 'imIn' in direction 'd' of the 'grid' over an amplitude of 'amp'.
    The emptied space is filled with 'fill' value. The result is put in 'imOut'.
    
    'grid' value can be HEXAGONAL or SQUARE and is set to DEFAULT_GRID by 
    default.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    """
    err = core.MB_Shift(imIn.mbIm, imOut.mbIm, d, amp, fill, grid.id)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def shiftVector(imIn, imOut, vector, fill):
    """
    Shifts image 'imIn' by 'vector' (tuple with dx,dy).
    The emptied space is filled with 'fill' value.
    The result is put in 'imOut'.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same size and
    depth.
    """
    err = core.MB_ShiftVector(imIn.mbIm, imOut.mbIm, vector[0], vector[1], fill)
    mamba.raiseExceptionOnError(err)
    imOut.update()

def downscale(imIn, imOut):
    """
    Downscale a 32-bit image 'imIn', whom range can go from 0 up to 16M, to a 
    greyscale image 'imOut' of range 0 to 255. This function will ensure
    that the minimum of 'imIn' will be mapped to 0 in 'imOut' and that the
    maximum will be mapped to 255. All other values will be mapped linearly
    between those two.
    """
    
    imWrk = mamba.imageMb(imIn)
    (mi, ma) = computeRange(imIn)
    mamba.subConst(imIn, mi, imWrk)
    mamba.mulConst(imWrk, 255, imWrk)
    mamba.divConst(imWrk, ma-mi, imWrk)
    mamba.copyBytePlane(imWrk, 0, imOut)

