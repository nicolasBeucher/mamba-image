"""
Geodesic operators.

This module provides a set of functions to perform geodesic computations.
It includes build and dualbuild operations, geodesic erosion and dilation ...
"""

# Contributors: Serge BEUCHER, Nicolas BEUCHER

import mamba
import mamba.core as core

def upperGeodesicDilate(imIn, imMask, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Performs an upper geodesic dilation of image 'imIn' above 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the dilation.
    'se' specifies the type of structuring element used to perform the 
    computation (DEFAULT_SE by default). 
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    mamba.logic(imIn, imMask, imOut, "sup")
    if imIn.getDepth() == 1:
        for i in range(n):
            mamba.diff(imOut, imMask, imOut)
            mamba.dilate(imOut, imOut, se=se)
            mamba.logic(imMask, imOut, imOut, "sup")
    else:
        imWrk1 = mamba.imageMb(imIn)
        imWrk2 = mamba.imageMb(imIn, 1)
        for i in range(n):
            mamba.generateSupMask(imOut, imMask, imWrk2, True)
            mamba.convertByMask(imWrk2, imWrk1, 0, mamba.computeMaxRange(imWrk1)[1])
            mamba.logic(imOut, imWrk1, imOut, "inf")
            mamba.dilate(imOut, imOut, se=se)
            mamba.logic(imOut, imMask, imOut, "sup")

def lowerGeodesicDilate(imIn, imMask, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Performs a lower geodesic dilation of image 'imIn' below 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the dilation.
    'se' specifies the type of structuring element used to perform the 
    computation (DEFAULT_SE by default). 
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    mamba.logic(imIn, imMask, imOut, "inf")
    for i in range(n):
        mamba.dilate(imOut, imOut, se=se)
        mamba.logic(imMask, imOut, imOut, "inf")

def geodesicDilate(imIn, imMask, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    This operator is simply an alias of lowerGeodesicDilate. It is kept for
    compatibility reasons.
    """
    
    lowerGeodesicDilate(imIn, imMask, imOut, n, se=se)
    
        
def upperGeodesicErode(imIn, imMask, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Performs a upper geodesic erosion of image 'imIn' above 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the erosion.
    'se' specifies the type of structuring element used to perform the 
    computation (DEFAULT_SE by default).
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    mamba.logic(imIn, imMask, imOut, "sup")
    for i in range(n):
        mamba.erode(imOut, imOut, se=se)
        mamba.logic(imOut, imMask, imOut, "sup")

def lowerGeodesicErode(imIn, imMask, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Performs a lower geodesic erosion of image 'imIn' under 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the erosion.
    'se' specifies the type of structuring element used to perform the 
    computation (DEFAULT_SE by default).

    The binary lower geodesic erosion is realised using the fact that the
    dilation is the dual operation of the erosion.
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    if imIn.getDepth() == 1:
        mamba.diff(imMask, imIn, imOut)
        lowerGeodesicDilate(imOut, imMask, imOut, n, se=se)
        mamba.diff(imMask, imOut, imOut)
    else:
        imWrk1 = mamba.imageMb(imIn)
        imWrk2 = mamba.imageMb(imIn, 1)
        mamba.logic(imIn, imMask, imOut, "inf")
        for i in range(n):
            mamba.generateSupMask(imOut, imMask, imWrk2, False)
            mamba.convertByMask(imWrk2, imWrk1, 0, mamba.computeMaxRange(imWrk1)[1])
            mamba.logic(imOut, imWrk1, imOut, "sup")
            mamba.erode(imOut, imOut, se=se)
            mamba.logic(imOut, imMask, imOut, "inf")
 
def geodesicErode(imIn, imMask, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    This transformation is identical to the previous version and it has been
    kept for compatibilty purposes.
    
    Note that the binary and the greytone operators are different.
    """
    
    if imIn.getDepth() == 1:
        lowerGeodesicErode(imIn, imMask, imOut, n, se=se)
    else:
        upperGeodesicErode(imIn, imMask, imOut, n, se=se)

def buildNeighbor(imMask, imInout, d, grid=mamba.DEFAULT_GRID):
    """
    Builds image 'imInout' in direction 'd' according to 'grid' using 'imMask'
    as a mask (the propagation is performed only in 'd' direction).
    
    The function also returns the volume of the image 'imInout' after the
    build operation.
    
    'grid' value can be HEXAGONAL or SQUARE.
    """
    err,volume = core.MB_BldNb(imMask.mbIm,imInout.mbIm,d, grid.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()
    return volume
    
def dualbuildNeighbor(imMask, imInout, d, grid=mamba.DEFAULT_GRID):
    """
    Dual builds image 'imInout' in direction 'd' according to 'grid' using 
    'imMask' as a mask (the propagation is performed only in 'd' direction).
    
    The function also returns the volume of the image 'imInout' after the
    build operation.
    
    'grid' value can be HEXAGONAL or SQUARE.
    """
    err,volume = core.MB_DualBldNb(imMask.mbIm,imInout.mbIm,d, grid.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()
    return volume

def build(imMask, imInout, grid=mamba.DEFAULT_GRID):
    """
    Builds image 'imInout' using 'imMask' as a mask. This operator performs the
    geodesic reconstruction of 'imInout' inside the mask image and puts the
    result in the same image.
    
    This operator uses a recursive implementation of the reconstruction.
    
    This function will use the mamba default grid unless specified otherwise in
    'grid'.
    """
    
    vol = 0
    prec_vol = -1
    dirs = mamba.getDirections(grid, True)
    while(prec_vol!=vol):
        prec_vol = vol
        for d in dirs:
            vol = buildNeighbor(imMask, imInout, d, grid)

def dualBuild(imMask, imInout, grid=mamba.DEFAULT_GRID):
    """
    Builds (dual build) image 'imInout' using 'imMask' as a mask. This operator
    performs the geodesic dual reconstruction (by erosions) of 'imInout' inside
    the mask image and puts the result in the same image.
    
    This operator uses a recursive implementation of the reconstruction.
    
    This function will use the mamba default grid unless specified otherwise in
    'grid'.
    """
    
    vol = 0
    prec_vol = -1
    dirs = mamba.getDirections(grid, True)
    while(prec_vol!=vol):
        prec_vol = vol
        for d in dirs:
            vol = dualbuildNeighbor(imMask, imInout, d, grid)
            
def hierarBuild(imMask, imInout, grid=mamba.DEFAULT_GRID):
    """
    Builds image 'imInout' using 'imMask' as a mask. This function only
    works with greyscale and 32-bit images and uses a hierarchical queue algorithm to
    compute the result.
    
    'grid' will set the number of neighbors considered by the algorithm 
    (HEXAGONAL is 6-Neighbors and SQUARE is 8-Neighbors).
    
    This function is identical to build but it is faster.
    """
    
    err = core.MB_HierarBld(imMask.mbIm, imInout.mbIm, grid.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()
    
def hierarDualBuild(imMask, imInout, grid=mamba.DEFAULT_GRID):
    """
    Builds (dual build) image 'imInout' using 'imMask' as a mask. This function 
    works with greyscale and 32-bit images and uses a hierarchical queue 
    algorithm to compute the result.
    
    'grid' will set the number of neighbors considered by the algorithm 
    (HEXAGONAL is 6-Neighbors and SQUARE is 8-Neighbors).
    
    This function is identical to dualBuild but it is faster.
    """
    
    err = core.MB_HierarDualBld(imMask.mbIm, imInout.mbIm, grid.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def closeHoles(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Close holes in image 'imIn' and puts the result in 'imOut'. This operator
    works on binary and greytone images. In this case, however, it should be 
    used cautiously.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.negate(imIn, imIn)
    mamba.drawEdge(imWrk)
    mamba.logic(imIn, imWrk, imWrk, "inf")
    build(imIn, imWrk, grid=grid)
    mamba.negate(imIn, imIn)
    mamba.negate(imWrk, imOut)

def removeEdgeParticles(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Removes particles (connected components) touching the edge in image 'imIn'.
    The resulting image is put in image 'imOut'.
    Although this operator may be used with greytone images, it should be
    considered with caution.
    """
    
    imWrk = mamba.imageMb(imIn)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    mamba.dilate(imWrk, imWrk, se=se, edge=mamba.FILLED)
    mamba.logic(imIn, imWrk, imWrk, "inf")
    build(imIn, imWrk, grid=grid)
    mamba.diff(imIn, imWrk, imOut)

def geodesicDistance(imIn, imMask, imOut, se=mamba.DEFAULT_SE):
    """
    Computes the geodesic distance function of a set in 'imIn'. This distance
    function uses successive geodesic erosions of 'imIn' performed in the geodesic
    space defined by 'imMask'. The result is stored in 'imOut'. Be sure to use an 
    image of sufficient depth as output.
    
    This geodesic distance is quite slow as it is performed by successive geodesic
    erosions.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    imOut.reset()
    imWrk = mamba.imageMb(imIn)
    mamba.logic(imIn, imMask, imWrk, "inf")
    while mamba.computeVolume(imWrk) != 0:
        mamba.add(imOut, imWrk, imOut)
        lowerGeodesicErode(imWrk, imMask, imWrk, se=se)
    
