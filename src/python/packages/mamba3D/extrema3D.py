"""
Extrema (min/max) 3D operators.

This module provides a set of operators dealing with maxima and minima of a
function. New operators linked to the notion of dynamics are also provided.
"""

# Contributors: Nicolas BEUCHER

import mamba3D as m3D
import mamba

def minima3D(imIn, imOut, h=1, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the minima of 'imIn' using a dual build operation and puts the 
    result in 'imOut'.
    
    'h' can be used to define the minima depth. Grid used by the dual build 
    operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit as input. 'imOut' must be binary.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.addConst3D(imIn, h, imWrk)
    m3D.dualBuild3D(imIn, imWrk, grid=grid)
    m3D.sub3D(imWrk, imIn, imWrk)
    m3D.threshold3D(imWrk, imOut, 1, mamba.computeMaxRange(imIn[0])[1])

def maxima3D(imIn, imOut, h=1, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the maxima of 'imIn' using a build operation and puts the
    result in 'imOut'.
    
    'h' can be used to define the maxima height. Grid used by the build
    operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit as input. 'imOut' must be binary.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.subConst3D(imIn, h, imWrk)
    m3D.build3D(imIn, imWrk, grid=grid)
    m3D.sub3D(imIn, imWrk, imWrk)
    m3D.threshold3D(imWrk, imOut, 1, mamba.computeMaxRange(imIn[0])[1])
    
def minDynamics3D(imIn, imOut, h, grid=m3D.DEFAULT_GRID3D):
    """
    Extracts the minima of 'imIn' with a dynamics higher or equal to 'h'
    and puts the result in 'imOut'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = m3D.image3DMb(imIn)
    if imIn.getDepth() == 8:
        m3D.addConst3D(imIn, h, imWrk)
        m3D.dualBuild3D(imIn, imWrk, grid=grid)
        m3D.sub3D(imWrk, imIn, imWrk)
    else:
        m3D.ceilingAddConst3D(imIn, h, imWrk)
        m3D.dualBuild3D(imIn, imWrk, grid=grid)
        m3D.floorSub3D(imWrk, imIn, imWrk)
    m3D.threshold3D(imWrk, imOut, h, mamba.computeMaxRange(imIn[0])[1])
    
def maxDynamics3D(imIn, imOut, h, grid=m3D.DEFAULT_GRID3D):
    """
    Extracts the maxima of 'imIn' with a dynamics higher or equal to 'h'
    and puts the result in 'imOut'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = m3D.image3DMb(imIn)
    if imIn.getDepth() == 8:
        m3D.subConst3D(imIn, h, imWrk)
        m3D.build3D(imIn, imWrk, grid=grid)
        m3D.sub3D(imIn, imWrk, imWrk)
    else:
        m3D.floorSubConst3D(imIn, h, imWrk)
        m3D.build3D(imIn, imWrk, grid=grid)
        m3D.floorSub3D(imIn, imWrk, imWrk)
    m3D.threshold3D(imWrk, imOut, h, mamba.computeMaxRange(imIn[0])[1])

def deepMinima3D(imIn, imOut, h, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the minima of the dual reconstruction of image 'imIn' by 
    imIn + h and puts the result in 'imOut'.
    
    Grid used by the dual build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = m3D.image3DMb(imIn)
    if imIn.getDepth() == 8:
        m3D.addConst3D(imIn, h, imWrk)
    else:
        m3D.ceilingAddConst3D(imIn, h, imWrk)
    m3D.dualBuild3D(imIn, imWrk, grid=grid)
    minima3D(imWrk, imOut, 1, grid=grid)

def highMaxima3D(imIn, imOut, h, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the maxima of the reconstruction of image 'imIn' by imIn - h
    and puts the result in 'imOut'.

    Grid used by the build operation can be specified by 'grid'.
    
    Only works with 8-bit or 32-bit images as input. 'imOut' must be binary.
    """
    
    imWrk = m3D.image3DMb(imIn)
    if imIn.getDepth() == 8:
        m3D.subConst3D(imIn, h, imWrk)
    else:
        m3D.floorSubConst3D(imIn, h, imWrk)
    m3D.build3D(imIn, imWrk, grid=grid)
    m3D.maxima3D(imWrk, imOut, 1, grid=grid)
    
def maxPartialBuild3D(imIn, imMask, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Performs the partial reconstruction of 'imIn' with its maxima which are
    contained in the binary mask 'imMask'. The result is put in 'imOut'.
    
    'imIn' and 'imOut' must be different and greyscale images.
    """
    
    imWrk = m3D.image3DMb(imIn, 1)
    maxima3D(imIn, imWrk, 1, grid=grid)
    m3D.logic3D(imMask, imWrk, imWrk, "inf")
    m3D.convertByMask3D(imWrk, imOut, 0, mamba.computeMaxRange(imIn[0])[1])
    m3D.logic3D(imIn, imOut, imOut, "inf")
    m3D.build3D(imIn, imOut)

def minPartialBuild3D(imIn, imMask, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Performs the partial reconstruction of 'imIn' with its minima which are
    contained in the binary mask 'imMask'. The result is put in 'imOut'.
    
    'imIn' and 'imOut' must be different and greyscale images.
    """
    
    imWrk = m3D.image3DMb(imIn, 1)
    minima3D(imIn, imWrk, 1, grid=grid)
    m3D.logic3D(imMask, imWrk, imWrk, "inf")
    m3D.convertByMask3D(imWrk, imOut, mamba.computeMaxRange(imIn[0])[1], 0)
    m3D.logic3D(imIn, imOut, imOut, "sup")
    m3D.dualBuild3D(imIn, imOut)

