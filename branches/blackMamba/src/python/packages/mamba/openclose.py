"""
Opening and closing operators.

This module provides a set of functions to perform opening and closing 
operations. All the closing and opening operation defined in this module
use erosion, dilation and build functions with user-defined edge settings.
The functions define a default edge which can be changed (see the modules
erodil and geodesy).
"""

# Contributors: Serge BEUCHER, Nicolas, BEUCHER, Michel BILODEAU

import mamba

def opening(imIn, imOut, n=1, se=mamba.DEFAULT_SE, edge=mamba.FILLED):
    """
    Performs an opening operation on image 'imIn' and puts the result in 'imOut'.
    'n' controls the size of the opening and 'se' the structuring element used.
    
    The default edge is set to 'FILLED'. Note that the edge setting operates in the
    erosion only.
    """
   
    mamba.erode(imIn, imOut, n, se=se, edge=edge)
    mamba.dilate(imOut, imOut, n, se=se.transpose())

def closing(imIn, imOut, n=1, se=mamba.DEFAULT_SE, edge=mamba.FILLED):
    """
    Performs a closing operation on image 'imIn' and puts the result in 'imOut'.
    'n' controls the size of the closing and 'se' the structuring element used.
    
    The default edge is set to 'FILLED'. If 'edge' is set to 'EMPTY', the operation
    is slightly modified to avoid errors (non extensivity).
    """
    
    imWrk = mamba.imageMb(imIn)
    if edge==mamba.EMPTY:
        mamba.copy(imIn, imWrk)
    mamba.dilate(imIn, imOut, n, se=se)
    mamba.erode(imOut, imOut, n, se=se.transpose(), edge=edge)
    if edge==mamba.EMPTY:
        mamba.logic(imOut, imWrk, imOut, "sup")

def buildOpen(imIn, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Performs an opening by reconstruction operation on image 'imIn' and puts the
    result in 'imOut'. 'n' controls the size of the opening.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk)
    mamba.erode(imIn, imOut, n, se=se)
    mamba.build(imWrk, imOut, grid=se.getGrid())

def buildClose(imIn, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Performs a closing by dual reconstruction operation on image 'imIn' and puts
    the result in 'imOut'. 'n' controls the size of the closing.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk)
    mamba.dilate(imIn, imOut, n, se=se)
    mamba.dualBuild(imWrk, imOut, grid=se.getGrid())

def linearOpen(imIn, imOut, dir, n, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs an opening by a segment of size 'n' in direction 'dir'.
    
    'edge' is set to 'FILLED' by default. 
    """
    
    mamba.linearErode(imIn, imOut, dir, n, edge=edge, grid=grid)
    mamba.linearDilate(imOut, imOut, mamba.transposeDirection(dir, grid=grid), n, grid=grid)
    
def linearClose(imIn, imOut, dir, n, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs a closing by a segment of size 'n' in direction 'dir'.
    
    If 'edge' is set to 'EMPTY', the operation must be modified to remain extensive.
    """
    
    imWrk = mamba.imageMb(imIn)
    if edge==mamba.EMPTY:
        mamba.copy(imIn, imWrk)
    mamba.linearDilate(imIn, imOut, dir, n, grid=grid)
    mamba.linearErode(imOut, imOut, mamba.transposeDirection(dir, grid=grid), n, edge=edge, grid=grid)
    if edge==mamba.EMPTY:
        mamba.logic(imOut, imWrk, imOut, "sup")
   
def supOpen(imIn, imOut, n, grid=mamba.DEFAULT_GRID):
    """
    Performs the supremum of directional openings. A white particle is preserved
    (but not entirely) if its length is larger than 'n' in at least one direction.
    
    This operator is an opening. The image edge is set to 'EMPTY' in order to 
    take into account particles touching the edge (they are considered as entirely
    included in the image window).

    When square grid is used, the size in oblique directions are reduced to be
    similar to the horizontal and vertical size.    
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk1.reset()
    if grid == mamba.SQUARE:
        size = int((1.4142 * n + 1)/2)
        linearOpen(imIn, imWrk2, 2, size, edge=mamba.EMPTY, grid=grid)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        linearOpen(imIn, imWrk2, 4, size, edge=mamba.EMPTY, grid=grid)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        d = 4
    else:
        d = 6
    for i in range(1, d, 2):
        linearOpen(imIn, imWrk2, i, n, edge=mamba.EMPTY, grid=grid)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
    mamba.copy(imWrk1, imOut)
    
def infClose(imIn, imOut, n, grid=mamba.DEFAULT_GRID):
    """
    Performs the infimum of directional closings. A black particle is preserved
    if its length is larger than 'n' in at least one direction.
    
    This operator is a closing. The image edge is set to 'FILLED' in order to 
    take into account particles touching the edge (they are supposed not to 
    extend outside the image window).
    
    When square grid is used, the size in oblique directions are reduced to be
    similar to the horizontal and vertical size.    
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk1.fill(mamba.computeMaxRange(imIn)[1])
    if grid == mamba.SQUARE:
        size = int((1.4142 * n + 1)/2)
        linearClose(imIn, imWrk2, 2, size, grid=grid)
        mamba.logic(imWrk1, imWrk2, imWrk1, "inf")
        linearClose(imIn, imWrk2, 4, size, grid=grid)
        mamba.logic(imWrk1, imWrk2, imWrk1, "inf")
        d = 4
    else:
        d = 6
    for i in range(1, d, 2):
        linearClose(imIn, imWrk2, i, n, grid=grid)
        mamba.logic(imWrk1, imWrk2, imWrk1, "inf")
    mamba.copy(imWrk1, imOut)
    

