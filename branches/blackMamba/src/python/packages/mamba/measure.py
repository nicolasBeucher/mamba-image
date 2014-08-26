"""
Measure operators.

This module provides a set of functions which perform measure
operations on an image. Measures include volume, range, area ...
"""

# Contributors: Serge BEUCHER, Nicolas BEUCHER

import mamba
import mamba.core as core

import math

def computeVolume(imIn):
    """
    Computes the volume of the image 'imIn', i.e. the sum of its pixel values.
    The computed integer value is returned by the function.
    
    'imIn' can be a 1-bit, 8-bit or 32-bit image.
    """
    err, volume = core.MB_Volume(imIn.mbIm)
    mamba.raiseExceptionOnError(err)
    return volume

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

def computeArea(imIn, scale=(1.0, 1.0)):
    """
    Calculates the area of the binary image 'imIn'. 'scale' is a tuple 
    containing the horizontal scale factor (distance between two adjacent 
    horizontal points) and the vertical scale factor (distance between two 
    successive lines) of image 'imIn' (default is 1.0 for both). The result is
    a float (when default values are used, the result value is identical to the
    computeVolume operator).
    
    Note that, with hexagonal grid, the "scale' default values do not correspond
    to an isotropic grid (where triangles would be equilateral).
    
    Beware, if the input image 'imIn' is not a binary image, the function raises
    an error.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    a = scale[0]*scale[1]*mamba.computeVolume(imIn)
    return a

def computeDiameter(imIn, dir, scale=(1.0, 1.0), grid=mamba.DEFAULT_GRID):
    """
    Computes the diameter (diametral variation) of binary image 'imIn' in 
    direction 'dir'. 'scale' is a tuple defining the horizontal and vertical
    scale factors (default is 1.0).
    
    Beware, if the input image 'imIn' is not a binary image, the function raises
    an error.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    if dir == 0:
        return 0.0
    dir = ((dir - 1)%(mamba.gridNeighbors(grid)//2)) +1
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk)
    mamba.diffNeighbor(imIn, imWrk, 1<<dir, grid=grid)
    if grid == mamba.HEXAGONAL:
        l = scale[1]
        if dir != 2:
            l = 2*l*scale[0]/math.sqrt(scale[0]*scale[0] + 4*scale[1]*scale[1])
    else:
        if dir == 1:
            l = scale[0]
        elif dir == 3:
            l = scale[1]
        else:
            l = scale[0]*scale[1]/math.sqrt(scale[0]*scale[0] + scale[1]*scale[1])
    l = l*mamba.computeVolume(imWrk)
    return l

def computePerimeter(imIn, scale=(1.0, 1.0), grid=mamba.DEFAULT_GRID):
    """
    Computes the perimeter of all particles in binary image 'imIn' according
    to the Cauchy-Crofton formula. 'scale' is a tuple defining the horizontal
    and vertical scale factors (default is 1.0).
    
    The edge of the image is always set to 'EMPTY'.
    
    Beware, if the input image 'imIn' is not a binary image, the function raises
    an error.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    p = 0.
    for i in range(1, mamba.gridNeighbors(grid)//2 + 1):
        p += computeDiameter(imIn, i, scale=scale, grid=grid)
    p = 2*math.pi*p/mamba.gridNeighbors(grid)
    return p
    
def computeConnectivityNumber(imIn, grid=mamba.DEFAULT_GRID):
    """
    Computes the connectivity number (Euler_Poincare constant) of image 'ImIn'.
    The result is an integer number.
    
    Beware, if the input image 'imIn' is not a binary image, the function raises
    an error.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    imWrk  = mamba.imageMb(imIn)
    if grid == mamba.HEXAGONAL:
        dse = mamba.doubleStructuringElement([1,6],[0],mamba.HEXAGONAL)
        mamba.hitOrMiss(imIn, imWrk, dse)
        n = mamba.computeVolume(imWrk)
        dse = mamba.doubleStructuringElement([1],[0,2],mamba.HEXAGONAL)
        mamba.hitOrMiss(imIn, imWrk, dse)
        n = n - mamba.computeVolume(imWrk)
    else:
        dse = mamba.doubleStructuringElement([3,4,5],[0],mamba.SQUARE)
        mamba.hitOrMiss(imIn, imWrk, dse)
        n = mamba.computeVolume(imWrk)
        dse = mamba.doubleStructuringElement([4],[0,3,5],mamba.SQUARE)
        mamba.hitOrMiss(imIn, imWrk, dse)
        n = n - mamba.computeVolume(imWrk)
        dse = mamba.doubleStructuringElement([3,5],[0,4],mamba.SQUARE)
        mamba.hitOrMiss(imIn, imWrk, dse)
        n = n + mamba.computeVolume(imWrk)
    return n

def computeComponentsNumber(imIn, grid=mamba.DEFAULT_GRID):
    """
    Computes the number of connected components in image 'imIn'. The result is
    an integer value.
    """
    
    imWrk =  mamba.imageMb(imIn, 32)
    return  mamba.label(imIn, imWrk, grid=grid)
    

def computeFeretDiameters(imIn, scale=(1.0, 1.0)):
    """
    Computes the global Feret diameters (horizontal and vertical) of binary 
    image 'imIn' and returns the result in a tuple (hDf, vDf). These diameters 
    correspond to the horizontal and vertical dimensions of the smallest 
    bonding box containing all the particles of 'imIn'
    """
    
    s = mamba.extractFrame(imIn, 1)
    return (scale[0]*(s[2]-s[0]), scale[1]*(s[3]-s[1]))

