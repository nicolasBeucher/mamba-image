"""
Opening and closing operators.

This module provides a set of functions to perform opening and closing 
operations. All the closing and opening operation defined in this module
use erosion, dilation and build functions with user-defined edge settings.
The functions define a default edge which can be changed (see the modules
erodil3D and geodesy3D).
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

def opening3D(imIn, imOut, n=1, se=m3D.CUBOCTAHEDRON1, edge=mamba.FILLED):
    """
    Performs an opening operation on 3D image 'imIn' and puts the result
    in 'imOut'. 'n' controls the size of the opening and 'se' the
    structuring element used.
    
    The default edge is set to 'FILLED'. Note that the edge setting
    operates in the erosion only.
    """
   
    m3D.erode3D(imIn, imOut, n, se=se, edge=edge)
    m3D.dilate3D(imOut, imOut, n, se=se.transpose())

def closing3D(imIn, imOut, n=1, se=m3D.CUBOCTAHEDRON1, edge=mamba.FILLED):
    """
    Performs a closing operation on 3D image 'imIn' and puts the result
    in 'imOut'. 'n' controls the size of the closing and 'se' the
    structuring element used.
    
    The default edge is set to 'FILLED'. If 'edge' is set to 'EMPTY', the
    operation is slightly modified to avoid errors (non extensivity).
    """
    
    imWrk = m3D.image3DMb(imIn)
    if edge==mamba.EMPTY:
        m3D.copy3D(imIn, imWrk)
    m3D.dilate3D(imIn, imOut, n, se=se)
    m3D.erode3D(imOut, imOut, n, se=se.transpose(), edge=edge)
    if edge==mamba.EMPTY:
        m3D.logic3D(imOut, imWrk, imOut, "sup")

def buildOpen3D(imIn, imOut, n=1, se=m3D.CUBOCTAHEDRON1):
    """
    Performs an opening by reconstruction operation on 3D image 'imIn' and
    puts the result in 'imOut'. 'n' controls the size of the opening.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.copy3D(imIn, imWrk)
    m3D.erode3D(imIn, imOut, n, se=se)
    m3D.build3D(imWrk, imOut, grid=se.getGrid())

def buildClose3D(imIn, imOut, n=1, se=m3D.CUBOCTAHEDRON1):
    """
    Performs a closing by dual reconstruction operation on 3D image 'imIn'
    and puts the result in 'imOut'. 'n' controls the size of the closing.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.copy3D(imIn, imWrk)
    m3D.dilate3D(imIn, imOut, n, se=se)
    m3D.dualBuild3D(imWrk, imOut, grid=se.getGrid())

def linearOpen3D(imIn, imOut, dir, n, grid=m3D.DEFAULT_GRID3D, edge=mamba.FILLED):
    """
    Performs an opening by a segment of size 'n' in direction 'dir'.
    
    'edge' is set to 'FILLED' by default. 
    """
    
    m3D.linearErode3D(imIn, imOut, dir, n, edge=edge, grid=grid)
    m3D.linearDilate3D(imOut, imOut, m3D.transposeDirection3D(dir, grid=grid), n, grid=grid)
    
def linearClose3D(imIn, imOut, dir, n, grid=m3D.DEFAULT_GRID3D, edge=mamba.FILLED):
    """
    Performs a closing by a segment of size 'n' in direction 'dir'.
    
    If 'edge' is set to 'EMPTY', the operation must be modified to
    remain extensive.
    """
    
    imWrk = m3D.image3DMb(imIn)
    if edge==mamba.EMPTY:
        m3D.copy3D(imIn, imWrk)
    m3D.linearDilate3D(imIn, imOut, dir, n, grid=grid)
    m3D.linearErode3D(imOut, imOut, m3D.transposeDirection3D(dir, grid=grid), n, edge=edge, grid=grid)
    if edge==mamba.EMPTY:
        m3D.logic3D(imOut, imWrk, imOut, "sup")
   
def supOpen3D(imIn, imOut, n, grid=m3D.DEFAULT_GRID3D):
    """
    Performs the supremum of directional openings. A white particle is preserved
    (but not entirely) if its length is larger than 'n' in at least one direction.
    
    This operator is an opening. The image edge is set to 'EMPTY' in order to 
    take into account particles touching the edge (they are considered as entirely
    included in the image window).

    When square grid is used, the size in oblique directions are reduced to be
    similar to the horizontal and vertical size.    
    """
    
    imWrk1 = m3D.image3DMb(imIn)
    imWrk2 = m3D.image3DMb(imIn)
    imWrk1.reset()
    # Default grid is a proxy for an actual grid
    if grid == m3D.CUBIC:
        # First neighbors located at a sqrt(2) distance from the center
        size = int((1.4142 * n + 1)/2)
        for d in [2,4,10,12,14,16]:
            linearOpen3D(imIn, imWrk2, d, size, grid, edge=mamba.EMPTY)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "sup")
        # First neighbors located at a sqrt(3) distance from the center
        size = int((1.7320 * n + 1)/2)
        for d in [11,13,15,17]:
            linearOpen3D(imIn, imWrk2, d, size, grid, edge=mamba.EMPTY)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "sup")
        # Finally neighbors located at a 1 distance from the center
        size = n
        for d in [1,3,9]:
            linearOpen3D(imIn, imWrk2, d, size, grid, edge=mamba.EMPTY)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "sup")
    elif grid == m3D.FACE_CENTER_CUBIC:
        for d in [1,3,5,7,8,9]:
            linearOpen3D(imIn, imWrk2, d, n, grid, edge=mamba.EMPTY)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "sup")
    else:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_PARAMETER)
    m3D.copy3D(imWrk1, imOut)
    
def infClose3D(imIn, imOut, n, grid=m3D.DEFAULT_GRID3D):
    """
    Performs the infimum of directional closings. A black particle is preserved
    if its length is larger than 'n' in at least one direction.
    
    This operator is a closing. The image edge is set to 'FILLED' in order to 
    take into account particles touching the edge (they are supposed not to 
    extend outside the image window).
    
    When square grid is used, the size in oblique directions are reduced to be
    similar to the horizontal and vertical size.    
    """
    
    imWrk1 = m3D.image3DMb(imIn)
    imWrk2 = m3D.image3DMb(imIn)
    imWrk1.fill(m3D.computeMaxRange3D(imIn)[1])
    # Default grid is a proxy for an actual grid
    if grid == m3D.CUBIC:
        # First neighbors located at a sqrt(2) distance from the center
        size = int((1.4142 * n + 1)/2)
        for d in [2,4,10,12,14,16]:
            linearClose3D(imIn, imWrk2, d, size, grid)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "inf")
        # First neighbors located at a sqrt(3) distance from the center
        size = int((1.7320 * n + 1)/2)
        for d in [11,13,15,17]:
            linearClose3D(imIn, imWrk2, d, size, grid)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "inf")
        # Finally neighbors located at a 1 distance from the center
        size = n
        for d in [1,3,9]:
            linearClose3D(imIn, imWrk2, d, size, grid)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "inf")
    elif grid == m3D.FACE_CENTER_CUBIC:
        for d in [1,3,5,7,8,9]:
            linearClose3D(imIn, imWrk2, d, n, grid)
            m3D.logic3D(imWrk1, imWrk2, imWrk1, "inf")
    else:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_PARAMETER)
    m3D.copy3D(imWrk1, imOut)
    
def openByCylinder3D(imInOut, height, section):
    """
    Opening using the dilation and erosion by a cylinder.
    """
    
    m3D.erodeByCylinder3D(imInOut, height, section)
    m3D.dilateByCylinder3D(imInOut, height, section)
    
def closeByCylinder3D(imInOut, height, section):
    """
    Closing using the dilation and erosion by a cylinder.
    """
    
    m3D.dilateByCylinder3D(imInOut, height, section)
    m3D.erodeByCylinder3D(imInOut, height, section)
