"""
Extrema (min/max) operators.

This module provides a set of operators dealing with maxima and minima of a
function. New operators linked to the notion of dynamics are also provided.
"""

# Contributor: Serge BEUCHER

import mamba

def minima(imIn, imOut, h=1, grid=mamba.DEFAULT_GRID):
    """
    Computes the minima of 'imIn' using a dual build operation and puts the 
    result in 'imOut'. When 'h' is equal to 1 (default value), the operator
    provides the minima of 'imIn'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = mamba.imageMb(imIn)
    if imIn.getDepth() == 8:
        mamba.addConst(imIn, h, imWrk)
        mamba.hierarDualBuild(imIn, imWrk, grid=grid)
        mamba.sub(imWrk, imIn, imWrk)
    else:
        mamba.ceilingAddConst(imIn, h, imWrk)
        mamba.dualBuild(imIn, imWrk, grid=grid)
        mamba.floorSub(imWrk, imIn, imWrk)
    mamba.threshold(imWrk, imOut, 1, mamba.computeMaxRange(imIn)[1])

def maxima(imIn, imOut, h=1, grid=mamba.DEFAULT_GRID):
    """
    Computes the maxima of 'imIn' using a build operation and puts the result in
    'imOut'. When 'h' is equal to 1 (default value), the operator provides the
    maxima of 'imIn'.
    
    Grid used by the build operation can be specified by 'grid'.
    
    Only works with with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = mamba.imageMb(imIn)
    if imIn.getDepth() == 8:
        mamba.subConst(imIn, h, imWrk)
        mamba.hierarBuild(imIn, imWrk, grid=grid)
        mamba.sub(imIn, imWrk, imWrk)
    else:
        mamba.floorSubConst(imIn, h, imWrk)
        mamba.build(imIn, imWrk, grid=grid)
        mamba.floorSub(imIn, imWrk, imWrk)
    mamba.threshold(imWrk, imOut, 1, mamba.computeMaxRange(imIn)[1])

def minDynamics(imIn, imOut, h, grid=mamba.DEFAULT_GRID):
    """
    Extracts the minima of 'imIn' with a dynamics higher or equal to 'h'
    and puts the result in 'imOut'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = mamba.imageMb(imIn)
    if imIn.getDepth() == 8:
        mamba.addConst(imIn, h, imWrk)
        mamba.hierarDualBuild(imIn, imWrk, grid=grid)
        mamba.sub(imWrk, imIn, imWrk)
    else:
        mamba.ceilingAddConst(imIn, h, imWrk)
        mamba.dualBuild(imIn, imWrk, grid=grid)
        mamba.floorSub(imWrk, imIn, imWrk)
    mamba.threshold(imWrk, imOut, h, mamba.computeMaxRange(imIn)[1])
    
def maxDynamics(imIn, imOut, h, grid=mamba.DEFAULT_GRID):
    """
    Extracts the maxima of 'imIn' with a dynamics higher or equal to 'h'
    and puts the result in 'imOut'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = mamba.imageMb(imIn)
    if imIn.getDepth() == 8:
        mamba.subConst(imIn, h, imWrk)
        mamba.hierarBuild(imIn, imWrk, grid=grid)
        mamba.sub(imIn, imWrk, imWrk)
    else:
        mamba.floorSubConst(imIn, h, imWrk)
        mamba.build(imIn, imWrk, grid=grid)
        mamba.floorSub(imIn, imWrk, imWrk)
    mamba.threshold(imWrk, imOut, h, mamba.computeMaxRange(imIn)[1])

def deepMinima(imIn, imOut, h, grid=mamba.DEFAULT_GRID):
    """
    Computes the minima of the dual reconstruction of image 'imIn' by 
    imIn + h and puts the result in 'imOut'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = mamba.imageMb(imIn)
    if imIn.getDepth() == 8:
        mamba.addConst(imIn, h, imWrk)
        mamba.hierarDualBuild(imIn, imWrk, grid=grid)
    else:
        mamba.ceilingAddConst(imIn, h, imWrk)
        mamba.dualBuild(imIn, imWrk, grid=grid)
    minima(imWrk, imOut, 1, grid=grid)

def highMaxima(imIn, imOut, h, grid=mamba.DEFAULT_GRID):
    """
    Computes the maxima of the reconstruction of image 'imIn' by imIn - h
    and puts the result in 'imOut'.

    Grid used by the build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = mamba.imageMb(imIn)
    if imIn.getDepth() == 8:
        mamba.subConst(imIn, h, imWrk)
        mamba.hierarBuild(imIn, imWrk, grid=grid)
    else:
        mamba.floorSubConst(imIn, h, imWrk)
        mamba.build(imIn, imWrk, grid=grid)
    maxima(imWrk, imOut, 1, grid=grid)
    
def maxPartialBuild(imIn, imMask, imOut, grid=mamba.DEFAULT_GRID):
    """
    Performs the partial reconstruction of 'imIn' with its maxima which are
    contained in the binary mask 'imMask'. The result is put in 'imOut'.
    
    'imIn' and 'imOut' must be different and greyscale images.
    """
    
    imWrk = mamba.imageMb(imIn, 1)
    maxima(imIn, imWrk, 1, grid=grid)
    mamba.logic(imMask, imWrk, imWrk, "inf")
    mamba.convertByMask(imWrk, imOut, 0, mamba.computeMaxRange(imIn)[1])
    mamba.logic(imIn, imOut, imOut, "inf")
    mamba.build(imIn, imOut)

def minPartialBuild(imIn, imMask, imOut, grid=mamba.DEFAULT_GRID):
    """
    Performs the partial reconstruction of 'imIn' with its minima which are
    contained in the binary mask 'imMask'. The result is put in 'imOut'.
    
    'imIn' and 'imOut' must be different and greyscale images.
    """
    
    imWrk = mamba.imageMb(imIn, 1)
    minima(imIn, imWrk, 1, grid=grid)
    mamba.logic(imMask, imWrk, imWrk, "inf")
    mamba.convertByMask(imWrk, imOut, mamba.computeMaxRange(imIn)[1], 0)
    mamba.logic(imIn, imOut, imOut, "sup")
    mamba.dualBuild(imIn, imOut)

