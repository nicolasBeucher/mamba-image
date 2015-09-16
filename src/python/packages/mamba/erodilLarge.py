"""
Large erosion and dilation operators.

This module provides a set of functions performing erosions and
dilations with large structuring elements. These operators are to be prefered
to the standard ones when working with large structuring elements.
"""
# Contributor: Serge BEUCHER

import mamba
import mamba.core as core

def _sizeSplit(size):
    # This internal function splits the size of the structuring element into a list of
    # successive and decreasing sizes (except the first one). Successive erosions
    # or dilations by double points produce an erosion or dilation by a segment
    # of length 'size'.
   
    sizeList=[]
    incr=1
    while size>incr:
        sizeList.append(incr)
        size=size-incr
        incr=2*incr
    sizeList.append(size)
    sizeList.reverse()
    return sizeList

# Elementary operators for large structuring elements

def infFarNeighbor(imIn, imInout, nb, amp, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs a minimum operation between the 'imInout' image pixels and their 
    neighbor 'nb' at distance 'amp' according to 'grid' in image 'imIn'. The result
    is put in 'imInOut'. 
   
    'grid' value can be HEXAGONAL or SQUARE. 'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imInOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    """
    err = core.MB_InfFarNb(imIn.mbIm, imInout.mbIm, nb, amp, grid.id, edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def supFarNeighbor(imIn, imInout, nb, amp, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Performs a maximum operation between the 'imInout' image pixels and their 
    neighbor 'nb' at distance 'amp' according to 'grid' in image 'imIn'. The result
    is put in 'imInOut'. 
   
    'grid' value can be HEXAGONAL or SQUARE. 'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imInOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    """
    err = core.MB_SupFarNb(imIn.mbIm, imInout.mbIm, nb, amp, grid.id, edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def largeLinearErode(imIn, imOut, dir, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Erosion by a large segment in direction 'dir' in a reduced number of iterations.
    Uses the erosions by doublets of points (supposed to be faster, thanks to
    an enhanced shift operator).
    """
    
    mamba.copy(imIn, imOut)
    for i in _sizeSplit(size):
        infFarNeighbor(imOut, imOut, dir, i, grid=grid, edge=edge)

def largeLinearDilate(imIn, imOut, dir, size, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Dilation by a large segment in direction 'dir' in a reduced number of iterations.
    Uses the dilations by doublets of points (supposed to be faster, thanks to
    an enhanced shift operator).
    """
    
    mamba.copy(imIn, imOut)
    for i in _sizeSplit(size):
        supFarNeighbor(imOut, imOut, dir, i, grid=grid, edge=edge)

# Operations with large hexagons
def largeHexagonalErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by large hexagons using erosions by large segments and the Steiner
    decomposition property of the hexagon.
    Edge effects are corrected by erosions with transposed decompositions
    combined with inf operations (see documentation for further details).
    
    This operator is quite complex to avoid edge effects.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    sizemax = min(imIn.getSize())//2
    # If size larger than sizemax, the operation must be iterated to prevent edge effects.
    n = size
    mamba.copy(imIn, imOut)
    while n > 0:
        s = min(n, sizemax)
        largeLinearErode(imOut, imWrk1, 6, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imWrk1, imWrk1, 4, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imOut, imWrk2, 4, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imWrk2, imWrk2, 6, s, grid=mamba.HEXAGONAL, edge=edge)
        mamba.logic(imWrk1, imWrk2, imWrk1, "inf")
        largeLinearErode(imWrk1, imWrk2, 2, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imOut, imWrk1, 1, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imWrk1, imWrk1, 3, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imOut, imOut, 3, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearErode(imOut, imOut, 1, s, grid=mamba.HEXAGONAL, edge=edge)
        mamba.logic(imWrk1, imOut, imWrk1, "inf")
        largeLinearErode(imWrk1, imOut, 5, s, grid=mamba.HEXAGONAL, edge=edge)
        mamba.logic(imOut, imWrk2, imOut, "inf")
        n = n - s
        
def largeHexagonalDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by large hexagons using dilations by large segments and the Steiner
    decomposition property of the hexagon.
    Edge effects are corrected by dilations with transposed decompositions
    combined with sup operators.
    
    This operator is quite complex to avoid edge effects.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    sizemax = min(imIn.getSize())//2
    # If size larger than sizemax, the operation must be iterated to prevent edge effects.
    n = size
    mamba.copy(imIn, imOut)
    while n >  0:
        s = min(n, sizemax)
        largeLinearDilate(imOut, imWrk1, 6, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imWrk1, imWrk1, 4, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imOut, imWrk2, 4, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imWrk2, imWrk2, 6, s, grid=mamba.HEXAGONAL, edge=edge)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        largeLinearDilate(imWrk1, imWrk2, 2, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imOut, imWrk1, 1, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imWrk1, imWrk1, 3, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imOut, imOut, 3, s, grid=mamba.HEXAGONAL, edge=edge)
        largeLinearDilate(imOut, imOut, 1, s, grid=mamba.HEXAGONAL, edge=edge)
        mamba.logic(imWrk1, imOut, imWrk1, "sup")
        largeLinearDilate(imWrk1, imOut, 5, s, grid=mamba.HEXAGONAL, edge=edge)
        mamba.logic(imOut, imWrk2, imOut, "sup")
        n = n - s
    
# Operations with large squares
def largeSquareErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a large square using erosions by large segments and the Steiner
    decomposition property of the square.
    
    No edge effects are likely to happen with a square structuring element.
    """
    
    largeLinearErode(imIn, imOut, 1, size, grid=mamba.SQUARE, edge=edge)
    largeLinearErode(imOut, imOut, 3, size, grid=mamba.SQUARE, edge=edge)
    largeLinearErode(imOut, imOut, 5, size, grid=mamba.SQUARE, edge=edge)
    largeLinearErode(imOut, imOut, 7, size, grid=mamba.SQUARE, edge=edge)

def largeSquareDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a large square using dilations by large segments and the Steiner
    decomposition property of the square.
    
    No edge effects are likely to happen with a square structuring element.
    """
    
    largeLinearDilate(imIn, imOut, 1, size, grid=mamba.SQUARE, edge=edge)
    largeLinearDilate(imOut, imOut, 3, size, grid=mamba.SQUARE, edge=edge)
    largeLinearDilate(imOut, imOut, 5, size, grid=mamba.SQUARE, edge=edge)
    largeLinearDilate(imOut, imOut, 7, size, grid=mamba.SQUARE, edge=edge)

# Operations with large dodecagons
def _sparseConjugateHexagonErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a conjugate hexagon. The structuring element used by this operation
    is not complete. Some holes appear inside the structuring element. Therefore, this
    operation should not be used to obtain true conjugate hexagons dilations (for
    internal use only).
    """

    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    val = mamba.computeMaxRange(imIn)[1]*int(edge==mamba.FILLED)
    for i in _sizeSplit(size):
        mamba.copy(imOut, imWrk1)
        j = 2*i
        infFarNeighbor(imWrk1, imOut, 1, j, grid=mamba.SQUARE, edge=edge)
        mamba.shift(imWrk1, imWrk2, 2, i, val, grid=mamba.HEXAGONAL)
        infFarNeighbor(imWrk2, imOut, 4, i, grid=mamba.HEXAGONAL, edge=edge)
        infFarNeighbor(imWrk2, imOut, 6, i, grid=mamba.HEXAGONAL, edge=edge)
        infFarNeighbor(imWrk1, imOut, 5, j, grid=mamba.SQUARE, edge=edge)
        mamba.shift(imWrk1, imWrk2, 5, i, val, grid=mamba.HEXAGONAL)
        infFarNeighbor(imWrk2, imOut, 1, i, grid=mamba.HEXAGONAL, edge=edge)
        infFarNeighbor(imWrk2, imOut, 3, i, grid=mamba.HEXAGONAL, edge=edge)
        j = 3*i//2
        infFarNeighbor(imWrk1, imOut, 2, j, grid=mamba.HEXAGONAL, edge=edge)
        infFarNeighbor(imWrk1, imOut, 5, j, grid=mamba.HEXAGONAL, edge=edge)
        
def _sparseConjugateHexagonDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a conjugate hexagon. The structuring element used by this operation
    is not complete. Some holes appear inside the structuring element. Therefore, this
    operation should not be used to obtain true conjugate hexagons dilations (for
    internal use only).
    """   

    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    val = mamba.computeMaxRange(imIn)[1]*int(edge!=mamba.EMPTY)
    for i in _sizeSplit(size):
        mamba.copy(imOut, imWrk1)
        j = 2*i
        supFarNeighbor(imWrk1, imOut, 1, j, grid=mamba.SQUARE, edge=edge)
        mamba.shift(imWrk1, imWrk2, 2, i, val, grid=mamba.HEXAGONAL)
        supFarNeighbor(imWrk2, imOut, 4, i, grid=mamba.HEXAGONAL, edge=edge)
        supFarNeighbor(imWrk2, imOut, 6, i, grid=mamba.HEXAGONAL, edge=edge)
        supFarNeighbor(imWrk1, imOut, 5, j, grid=mamba.SQUARE, edge=edge)
        mamba.shift(imWrk1, imWrk2, 5, i, val, grid=mamba.HEXAGONAL)
        supFarNeighbor(imWrk2, imOut, 1, i, grid=mamba.HEXAGONAL, edge=edge)
        supFarNeighbor(imWrk2, imOut, 3, i, grid=mamba.HEXAGONAL, edge=edge)
        j = 3*i//2
        supFarNeighbor(imWrk1, imOut, 2, j, grid=mamba.HEXAGONAL, edge=edge)
        supFarNeighbor(imWrk1, imOut, 5, j, grid=mamba.HEXAGONAL, edge=edge)
  
def largeDodecagonalErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by large dodecacagons (hexagonal grid). Basically, it is the same 
    operation as the previous one where classical erosions have been replaced
    by erosions by large structuring elements, and where a "partial" erosion by
    a conjugate hexagon is used.
    """

    n1 = int(0.4641*size)
    n1 += abs(n1 % 2 - size % 2)
    n2 =(size - n1)//2
    _sparseConjugateHexagonErode(imIn, imOut, n2, edge=edge)   
    largeHexagonalErode(imOut, imOut, n1, edge=edge)   
    
def largeDodecagonalDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by large dodecacagons (hexagonal grid). Basically, it is the same 
    operation as the previous one where classical dilations have been replaced
    by dilations by large structuring elements, and where a "partial" dilation by
    a conjugate hexagon is used.
    """

    n1 = int(0.4641*size)
    n1 += abs(n1 % 2 - size % 2)
    n2 =(size - n1)//2
    _sparseConjugateHexagonDilate(imIn, imOut, n2, edge=edge)   
    largeHexagonalDilate(imOut, imOut, n1, edge=edge)   

# Operations with large octogons    
def _sparseDiamondDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a large diamond (conjugate square) on square grid. This diamond
    is not completely filled. It is for internal use only.
    """

    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    for i in _sizeSplit(size):
        mamba.copy(imOut, imWrk)
        supFarNeighbor(imWrk, imOut, 1, i, grid=mamba.SQUARE, edge=edge)
        supFarNeighbor(imWrk, imOut, 3, i, grid=mamba.SQUARE, edge=edge)
        supFarNeighbor(imWrk, imOut, 5, i, grid=mamba.SQUARE, edge=edge)
        supFarNeighbor(imWrk, imOut, 7, i, grid=mamba.SQUARE, edge=edge)

def _sparseDiamondErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a large diamond (conjugate square) on square grid. This diamond
    is not completely filled. It is for internal use only.
    """

    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    for i in _sizeSplit(size):
        mamba.copy(imOut, imWrk)
        infFarNeighbor(imWrk, imOut, 1, i, grid=mamba.SQUARE, edge=edge)
        infFarNeighbor(imWrk, imOut, 3, i, grid=mamba.SQUARE, edge=edge)
        infFarNeighbor(imWrk, imOut, 5, i, grid=mamba.SQUARE, edge=edge)
        infFarNeighbor(imWrk, imOut, 7, i, grid=mamba.SQUARE, edge=edge)
         
def largeOctogonalErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a large octogon (square grid). This operation uses erosions
    by large squares and large diamonds previously defined.
    """

    n1 = int(0.41421*size + 0.5)
    n2 = size - n1
    largeSquareErode(imIn, imOut, n1, edge=edge)
    _sparseDiamondErode(imOut, imOut, n2, edge=edge)

def largeOctogonalDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a large octogon (square grid). This operation uses dilations
    by large squares and large diamonds previously defined.
    """

    n1 = int(0.41421*size + 0.5)
    n2 = size - n1
    largeSquareDilate(imIn, imOut, n1, edge=edge)
    _sparseDiamondDilate(imOut, imOut, n2, edge=edge)

