"""
Erosion and dilation 3D operators.

This module provides a set of functions and class to perform erosions and
dilations. The module contains basic and complex operators that are based
on neighbor comparisons. In particular it defines the 3D structuring element
class which serves as the base for these operators. The module also contains
distance functions based on erosion.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

################################################################################
# Structuring elements definitions
################################################################################

class structuringElement3D:
    
    def __init__(self, directions, grid):
        """
        Structuring element constructor. A structuring element is defined by the 
        couple 'directions' (given in an ordered list) and 'grid'. You cannot
        define a structuring element that holds a direction more than once.
        
        You can look at the predefined structuring elements to get examples of
        how to make yours.
        """
        
        self.grid = grid
        xx = {}
        for d in directions:
            xx[d] = 1
        self.directions = list(xx.keys()) # This is actually a trick to 
                                          # remove duplicate from the direction
                                          # list
        self.directions.sort()
        self.directions_w0 = self.directions[:]
        self.has_zero = False
        while self.directions_w0.count(0)>0:
            self.directions_w0.remove(0)
            self.has_zero = True
        # neighbors defines the max number of neighbor points according to the grid
        # in use
        self.neighbors = grid.maxNeighbors()
        
    def __repr__(self):
        return "structuringElement3D("+repr(self.directions)+", "+repr(self.grid)+")"
        
    def __eq__(self, otherSE):
        return (otherSE.getGrid()==self.grid) and (otherSE.getDirections()==self.directions)
    def __ne__(self, otherSE):
        return (otherSE.getGrid()!=self.grid) or (otherSE.getDirections()!=self.directions)
            
    def getGrid(self):
        """
        Returns the grid associated with the structuring element.
        
        Example:
        >>>CUBOCTAHEDRON1.getGrid()
        mamba3D.FACE_CENTER_CUBIC
        """
        
        return self.grid
        
    def getDirections(self, withoutZero=False):
        """
        Returns a copy of the directions used by the structuring element.
        if 'withoutZero' is set to True the returned direction list will
        not include direction 0 (useful for some operators, such as erode
        or dilate, where direction 0 modifies the initial conditions).
        """
        
        if withoutZero:
            return self.directions_w0[:]
        return self.directions[:]
        
    def hasZero(self):
        """
        Returns True if the central point (0) is included in the direction list.
        """
        
        return self.has_zero
        
    def transpose(self):
        """
        Structuring element transposition (symmetry around the origin).
        """
        ndirs = [self.grid.getTranDir(d) for d in self.directions]
        o = structuringElement3D(ndirs, self.grid)
        return o
        
# Creating the most usual structuring elements
CUBOCTAHEDRON3 = structuringElement3D([0,1,3,5,7,9,10,11,12,13,14,15,16] , m3D.CENTER_CUBIC)
CUBOCTAHEDRON2 = structuringElement3D([0,1,2,3,4,5,6,7,8,9,10,12,14,16,18,19,21,23,25] , m3D.CUBIC)
CUBOCTAHEDRON1 = structuringElement3D([0,1,2,3,4,5,6,7,8,9,10,11,12] , m3D.FACE_CENTER_CUBIC)
CUBE2X2X2 = structuringElement3D([0,1,2,3,9,10,11,12] , m3D.CUBIC)
CUBE3X3X3 = structuringElement3D(list(range(27)) , m3D.CUBIC)
        
################################################################################
# Dilation and erosion functions
################################################################################

def dilate3D(imIn, imOut, n=1, se=CUBOCTAHEDRON1, edge=mamba.EMPTY):
    """
    This operator performs a dilation, using the structuring element 'se' (set
    by default as CUBOCTAHEDRON1), of 3D image 'imIn' and puts the result in 
    'imOut'. The operation is repeated 'n' times (default is 1). This operator
    assumes an 'EMPTY' edge by default.
    
    This operator always considers that the origin of the structuring element
    in use is at position 0 even if this point does not belong to it.
    """
    
    (width,height,length) = imIn.getSize()
    depth = imIn.getDepth()
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    zext = se.grid.getZExtension()
    imWrk = m3D.image3DMb(width, height, length+zext*2, depth)
    if edge==mamba.EMPTY:
        for i in range(zext):
            imWrk[i].reset()
            imWrk[length+zext*2-1-i].reset()
    else:
        value = mamba.computeMaxRange(imIn[0])[1]
        for i in range(zext):
            imWrk[i].fill(value)
            imWrk[length+zext*2-1-i].fill(value)
    
    m3D.copy3D(imIn, imOut)
    
    dirs = se.getDirections(withoutZero=True)
    for size in range(n):
        m3D.copy3D(imOut, imWrk, 0, 1)
        if not se.hasZero():
            imOut.reset()
        for i in range(length):
            dirs_enc = se.grid.getEncodedDirs(dirs,i)
            mamba.supNeighbor(imWrk[i], imOut[i], dirs_enc[-1], grid=se.grid.get2DGrid(), edge=edge)
            mamba.supNeighbor(imWrk[i+1], imOut[i], dirs_enc[0], grid=se.grid.get2DGrid(), edge=edge)
            mamba.supNeighbor(imWrk[i+2], imOut[i], dirs_enc[1], grid=se.grid.get2DGrid(), edge=edge)
    
def linearDilate3D(imIn, imOut, d, n=1, grid=m3D.DEFAULT_GRID3D, edge=mamba.EMPTY):
    """
    Dilation by a segment in direction 'd' of 3D image 'imIn', result in 'imOut'.
    The operation is repeated 'n' times (default is 1).This function will assume
    an EMPTY edge unless specified otherwise using 'edge'. The directions
    are defined according to the grid in use.
    """
    
    se = m3D.structuringElement3D([0,d], grid)
    m3D.copy3D(imIn, imOut)
    m3D.dilate3D(imOut, imOut, n, se=se, edge=edge)

def erode3D(imIn, imOut, n=1, se=CUBOCTAHEDRON1, edge=mamba.FILLED):
    """
    This operator performs an erosion, using the structuring element 'se' (set
    by default as CUBOCTAHEDRON1), of 3D image 'imIn' and puts the result in 
    'imOut'. The operation is repeated 'n' times (default is 1). This operator
    assumes a 'FILLED' edge by default.
    
    This operator always considers that the origin of the structuring element
    in use is at position 0 even if this point does not belong to it.
    """
    
    (width,height,length) = imIn.getSize()
    depth = imIn.getDepth()
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    zext = se.grid.getZExtension()
    imWrk = m3D.image3DMb(width, height, length+zext*2, depth)
    if edge==mamba.EMPTY:
        for i in range(zext):
            imWrk[i].reset()
            imWrk[length+zext*2-1-i].reset()
    else:
        value = mamba.computeMaxRange(imIn[0])[1]
        for i in range(zext):
            imWrk[i].fill(value)
            imWrk[length+zext*2-1-i].fill(value)
    
    m3D.copy3D(imIn, imOut)
    
    dirs = se.getDirections(withoutZero=True)
    for size in range(n):
        m3D.copy3D(imOut, imWrk, 0, 1)
        if not se.hasZero():
            imOut.fill(m3D.computeMaxRange3D(imIn)[1])
        for i in range(length):
            dirs_enc = se.grid.getEncodedDirs(dirs,i)
            mamba.infNeighbor(imWrk[i], imOut[i], dirs_enc[-1], grid=se.grid.get2DGrid(), edge=edge)
            mamba.infNeighbor(imWrk[i+1], imOut[i], dirs_enc[0], grid=se.grid.get2DGrid(), edge=edge)
            mamba.infNeighbor(imWrk[i+2], imOut[i], dirs_enc[1], grid=se.grid.get2DGrid(), edge=edge)
    
def linearErode3D( imIn, imOut, d, n=1, grid=m3D.DEFAULT_GRID3D, edge=mamba.FILLED):
    """
    Performs an erosion in direction 'd' of 3D image 'imIn' and puts the
    result in 'imOut'. The operation is repeated 'n' times (default is 1).
    This function will assume a FILLED edge unless specified otherwise using
    'edge'.
    """
    
    se = m3D.structuringElement3D([0,d], grid)
    m3D.copy3D(imIn, imOut)
    m3D.erode3D(imOut, imOut, n, se=se, edge=edge)
    
def erodeByCylinder3D(imInOut, height, section):
    """
    Erodes 3D image 'imInOut' using a cylinder with an hexagonal section of size 
    2x'section' and a height of 2x'height'. The image is modified by this
    function. The edge is always set to FILLED.
    """
    
    l = len(imInOut)
    for im in imInOut:
        mamba.erode(im, im, section, se=mamba.HEXAGON)
    provIm3D = m3D.image3DMb(imInOut)
    for i in range(l):
        mamba.copy(imInOut[i], provIm3D[i])
        for j in range(max(0,i-height), min(l,i+height+1)):
            mamba.logic(provIm3D[i], imInOut[j], provIm3D[i], "inf")
    m3D.copy3D(provIm3D, imInOut)
        
def dilateByCylinder3D(imInOut, height, section):
    """
    Dilates 3D image 'imInOut' using a cylinder with an hexagonal section of size 
    2x'section' and a height of 2x'height'. The image is modified by this
    function. The edge is always set to EMPTY.
    """
    
    l = len(imInOut)
    for im in imInOut:
        mamba.dilate(im, im, section, se=mamba.HEXAGON)
    provIm3D = m3D.image3DMb(imInOut)
    for i in range(l):
        mamba.copy(imInOut[i], provIm3D[i])
        for j in range(max(0,i-height), min(l,i+height+1)):
            mamba.logic(provIm3D[i], imInOut[j], provIm3D[i], "sup")
    m3D.copy3D(provIm3D, imInOut)

def computeDistance3D(imIn, imOut, grid=m3D.DEFAULT_GRID3D, edge=mamba.EMPTY):
    """
    Computes for each white pixel of binary 3D 'imIn' the minimum distance to
    reach a connected component boundary while constantly staying in the set. 
    The result is put in 32-bit 'imOut'.
    
    The distance computation will be performed according to the 'grid' (CUBIC
    is 26-Neighbors and FACE_CENTER_CUBIC is 12-Neighbors, CENTER_CUBIC is
    unsupported by this operator). 'edge' can be FILLED or EMPTY.
    """
    err = core.MB3D_Distanceb(imIn.mb3DIm, imOut.mb3DIm, grid.getCValue(), edge.id)
    mamba.raiseExceptionOnError(err)

