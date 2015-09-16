"""
Erosion and dilation operators.

This module provides a set of functions and class to perform erosions and
dilations. The module contains basic and complex operators that are based
on neighbor comparisons. In particular, it defines the structuring element
class which serve as the base for these operators. The module also contains
distance functions based on erosion.
"""

import mamba
import mamba.core as core

import functools

# Contributors : Nicolas BEUCHER, Michel BILODEAU, Serge BEUCHER

################################################################################
# Structuring elements definitions
################################################################################

class structuringElement:
    """
    This class allows to define simple structuring elements with points belonging
    to the elementary neighborhood of the origin point. Points in use are defined
    by their direction, according to the grid in use (hexagonal or square one).
    All the used directions are put in a in a direction list. The central point 
    (direction 0) may or may not belong to the structuring element.
    
    Example:
    >>>HEXAGON = structuringElement([0,1,2,3,4,5,6], mamba.HEXAGONAL)
    
    defines a structuring element named HEXAGON on the hexagonal grid and containing
    the origin point and all the six neighboring points in directions 1 to 6 of
    the grid.
    """
    
    def __init__(self, directions, grid):
        """
        Structuring element constructor. A structuring element is defined by the 
        couple 'directions' (given in an ordered list) and 'grid'. You cannot
        defines a structuring element that holds a direction more than once.
        
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
        if self.directions_w0.count(0)>0:
            self.directions_w0.remove(0)
            self.has_zero = True
        self.enc_dirs = functools.reduce(lambda x,y: x|(1<<y), self.directions, 0)
        self.enc_dirs_w0 = functools.reduce(lambda x,y: x|(1<<y), self.directions_w0, 0)
        # neighbors defines the max number of neighbor points according to the grid
        # in use
        self.neighbors = mamba.gridNeighbors(grid)
        
    def __repr__(self):
        return "structuringElement("+repr(self.directions)+", mamba."+repr(self.grid)+")"
        
    def __eq__(self, otherSE):
        return (otherSE.getGrid()==self.grid) and (otherSE.getDirections()==self.directions)
    def __ne__(self, otherSE):
        return (otherSE.getGrid()!=self.grid) or (otherSE.getDirections()!=self.directions)
    
    def getGrid(self):
        """
        Returns the grid associated with the structuring element.
        
        Example:
        >>>HEXAGON.getGrid()
        HEXAGONAL
        """
        
        return self.grid
        
    def getDirections(self, withoutZero=False):
        """
        Returns a copy of the directions used by the structuring element.
        If 'withoutZero' is set to True the returned direction list will
        not include direction 0 (useful for some operators, such as erode
        or dilate, where direction 0 modifies the initial conditions).
        
        Example:
        >>>SQUARE3X3.getDirections()
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
        """
        
        if withoutZero:
            return self.directions_w0[:]
        return self.directions[:]
        
    def getEncodedDirections(self, withoutZero=False):
        """
        Returns the directions used by the structuring element encoded in
        a format directly usable with Neighbor functions.
        If 'withoutZero' is set to True the returned encoded direction will
        not include direction 0 (useful for some operators, such as erode
        or dilate, where direction 0 modifies the initial conditions).
        """
        
        if withoutZero:
            return self.enc_dirs_w0
        return self.enc_dirs
        
    def hasZero(self):
        """
        Returns True if the central point (0) is included in the direction list.
        """
        
        return self.has_zero
       
    def rotate(self, step=1):
        """
        Rotates the structuring element 'step' times. When step is positive,
        rotation is clockwise. When step is negative, rotation is counterclockwise.
        When step is equal to zero, there is no rotation.
        
        Example:
        >>>SEGMENT.getDirections()
        [0, 1]
        >>>SEGMENT.rotate().getDirections()
        [0, 2]
        """
        
        ndirs = [mamba.rotateDirection(u, step, self.grid) for u in self.directions]
        o = structuringElement(ndirs, self.grid)
        return o
        
    def transpose(self):
        """
        Structuring element transposition (symmetry around the origin). Basically,
        it corresponds to a 3-steps rotation on an hexagonal grid, a 4-steps on
        a square one.
        
        Example:
        >>>TRIANGLE.getDirections()
        [0, 3, 4]
        >>>TRIANGLE.transpose().getDirections()
        |0, 1, 6]
        """
        
        return self.rotate(self.neighbors//2)

    def setAs(self, se):
        """
        Copies the attributes (directions, grid) of the structuringElement 'se' into
        the structuring element which this method is applied to. This method is
        mainly used to modify the default structuring element.
        
        Example:
        >>>DEFAULT_SE.setAs(SQUARE3X3)
        
        modifies the default structuring element to a square one.
        The erosions and dilations now will be performed with a square.

        Warning! Although it is perfectly allowed, it is not wise to use setAs
        method with other pre-defined structuring elements. For instance, if you
        type:
        
        >>>HEXAGON.setAs(SQUARE3X3)
        
        the structuring element HEXAGON will be superseded by SQUARE3X3.
        This may have unwanted consequences.
        """
        
        self.directions = se.directions
        self.directions_w0 = se.directions_w0
        self.enc_dirs = se.enc_dirs
        self.enc_dirs_w0 = se.enc_dirs_w0
        self.has_zero = se.has_zero
        self.neighbors = se.neighbors
        self.grid = se.grid
              
# Creating the most usual structuring elements
HEXAGON = structuringElement([0,1,2,3,4,5,6], mamba.HEXAGONAL)
SQUARE3X3 = structuringElement([0,1,2,3,4,5,6,7,8], mamba.SQUARE)
TRIANGLE = structuringElement([0,3,4], mamba.HEXAGONAL)
SQUARE2X2 = structuringElement([0,1,2,3], mamba.SQUARE)
TRIPOD = structuringElement([0,1,3,5], mamba.HEXAGONAL)
SEGMENT = structuringElement([0,3], mamba.SQUARE)
DIAMOND = structuringElement([0,1,3,5,7], mamba.SQUARE)
# HEXAGON is set as default
DEFAULT_SE = structuringElement([0,1,2,3,4,5,6], mamba.HEXAGONAL)

################################################################################
# Dilation and erosion functions
################################################################################

def diffNeighbor(imIn, imInout, nb, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Performs a set difference operation between the 'imInout' image pixels and 
    their neighbors according to 'grid' in image 'imIn'. Neighbors are encoded
    in 'nb'. If any considered neighbor point has a value greater than or equal 
	to the center point, this center point point is set to 0.
    The result is put in 'imOut'. 
   
    'grid' value can be HEXAGONAL or SQUARE. 'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit and 32-bit images of same size
    and depth.
    
    'nb' contains the coding of all the selected neighbor points. See the User Manual
    for details.
    """
    err = core.MB_DiffNb(imIn.mbIm, imInout.mbIm, nb, grid.id, edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def infNeighbor(imIn, imInout, nb, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs a minimum operation between the 'imInout' image pixels and their 
    neighbors according to 'grid' in image 'imIn'. Neighbors are encoded in
    'nb'.
    The result is put in 'imOut'.
    
    'grid' value can be HEXAGONAL or SQUARE. 'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    
    'nb' contains the coding of all the selected neighbor points. See the User Manual
    for details.
    """
    err = core.MB_InfNb(imIn.mbIm, imInout.mbIm, nb, grid.id, edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()
    
def supNeighbor(imIn, imInout, nb, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Performs a maximum operation between the 'imInout' image pixels and their 
    neighbors according to 'grid' in image 'imIn'. Neighbors are encoded in
    'nb'.
    The result is put in 'imOut'.
    
    'grid' value can be HEXAGONAL or SQUARE. 'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    
    'nb' contains the coding of all the selected neighbor points. See the User Manual
    for details.
    """
    err = core.MB_SupNb(imIn.mbIm, imInout.mbIm, nb, grid.id, edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def infVector(imIn, imInout, vector, edge=mamba.FILLED):
    """
    Performs a minimum operation between the 'imInout' image pixels and their
    corresponding pixels in image 'imIn' after it has been shifted by
    'vector' (tuple dx,dy). The result is put in 'imOut'.
   
    'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    """
    err = core.MB_InfVector(imIn.mbIm, imInout.mbIm, vector[0], vector[1], edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def supVector(imIn, imInout, vector, edge=mamba.EMPTY):
    """
    Performs a maximum operation between the 'imInout' image pixels and their
    corresponding pixels in image 'imIn' after it has been shifted by
    'vector' (tuple dx,dy). The result is put in 'imOut'.
   
    'edge' value can be EMPTY or FILLED.
    
    If a neighboring point falls outside the image window, its value in the operation
    is defined by 'edge'. If 'edge' is EMPTY, its value is 0. If 'edge' is FILLED,
    its value equals the maximal allowed value according to the depth of 'imIn'
    image.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same size and depth.
    """
    err = core.MB_SupVector(imIn.mbIm, imInout.mbIm, vector[0], vector[1], edge.id)
    mamba.raiseExceptionOnError(err)
    imInout.update()

def dilate(imIn, imOut, n=1, se=DEFAULT_SE, edge=mamba.EMPTY):
    """
    This operator performs a dilation, using the structuring element 'se' (set by
    default as DEFAULT_SE), of image 'imIn' and puts the result in 'imOut'. The 
    operation is repeated 'n' times (default is 1). This operator assumes an 
    'EMPTY' edge by default.
    
    This operator always considers that the origin of the structuring element in
    use is at position 0 even if this point does not belong to it.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    dirs = se.getEncodedDirections(withoutZero=True)
    for i in range(n):
        mamba.copy(imOut, imWrk)
        if not se.hasZero():
            imOut.reset()
        supNeighbor(imWrk, imOut, dirs, grid=se.getGrid(), edge=edge)
    
def doublePointDilate(imIn, imOut, d, n, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    This operator performs a dilation of 'imIn' using a double point as a structuring
    element. To build the double point, the first point is considered in position (0,0)
    and the second is built using a shift 'n' times in the direction 'd' + 180 degrees
    (transposed direction) of 'grid'. The result is put in imOut. The direction
    d is selected according to the grid in use (DEFAULT_GRID).
    
    Note that this operator is just an alias of the operator supFarNeighbor. 
    """
    
    mamba.copy(imIn, imOut)
    mamba.supFarNeighbor(imOut, imOut, d, n, grid=grid, edge=edge)
    
def linearDilate(imIn, imOut, d, n=1, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Dilation by a segment in direction 'd' of image 'imIn',  result in 'imOut'.
    The operation is repeated 'n' times (default is 1).This function will assume
    an EMPTY edge unless specified otherwise using 'edge'. The directions
    are defined according to the grid in use.
    """
    
    mamba.copy(imIn, imOut)
    # Basically its only calling the supNeighbor function in the direction d
    for i in range(n):
        supNeighbor(imOut, imOut, 1<<d, edge=edge, grid=grid)
    
def erode(imIn, imOut, n=1, se=DEFAULT_SE, edge=mamba.FILLED):
    """
    This operator corresponds, for erosion, to the dilation operator. It performs
    an erosion using the default structuring element of image 'imIn' and puts the
    result in 'imOut'. The operation is repeated 'n' times (default is 1). This
    function will assume a FILLED edge unless specified otherwise using 'edge'.
    
    This operator always considers that the origin of the structuring element in
    use is at position 0 even if this point does not belong to it.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    dirs = se.getEncodedDirections(withoutZero=True)
    for i in range(n):
        mamba.copy(imOut, imWrk)
        if not se.hasZero():
            imOut.fill(mamba.computeMaxRange(imIn)[1])
        infNeighbor(imWrk, imOut, dirs, grid=se.getGrid(), edge=edge)
    
def doublePointErode(imIn, imOut, d, n, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    This operation performs an erosion of 'imIn' using a double point as a
    structuring element. To build the double point, the first point is considered
    in position (0,0) and the second is built using a shift 'n' times in the
    conjugate direction 'd' + 180 degrees of 'grid'. The result is put in imOut.
    
    This operator is an alias of the infFarNeighbor operator.
    """
    
    mamba.copy(imIn, imOut)
    mamba.infFarNeighbor(imOut, imOut, d, n, grid=grid, edge=edge)
    
def linearErode( imIn, imOut, d, n=1, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs an erosion in direction 'd' of image 'imIn' and puts the result in
    'imOut'. The operation is repeated 'n' times (default is 1). This function
    will assume a FILLED edge unless specified otherwise using 'edge'.
    """
    
    mamba.copy(imIn, imOut)
    # Basically its only calling the infNeighbor function in the direction d
    for i in range(n):
        infNeighbor(imOut, imOut, 1<<d, grid=grid, edge=edge)

# The following operations are defined on hexagonal grid only    
def conjugateHexagonalErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a conjugate hexagon (hexagon turned by 30 degrees).

    Be aware that the size of operation corresponds to twice the size of the
    regular hexagon: a conjugate hexagon of size 1 is inscribed in a regular
    hexagon of size 2.
    """
    
    mamba.copy(imIn, imOut)
    for i in range(size):
        erode(imOut, imOut, 1, se=TRIPOD, edge=edge)
        erode(imOut, imOut, 1, se=TRIPOD.transpose(), edge=edge)

def conjugateHexagonalDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a conjugate hexagon (hexagon turned by 30 degrees).
    Be aware that the size of operation corresponds to twice the size of the
    regular hexagon: a conjugate hexagon of size 1 is inscribed in a regular
    hexagon of size 2.
    """
    
    mamba.copy(imIn, imOut)
    for i in range(size):
        dilate(imOut, imOut, 1, se=TRIPOD, edge=edge)
        dilate(imOut, imOut, 1, se=TRIPOD.transpose(), edge=edge)

def dodecagonalErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a dodecagon (hexagonal grid). This operation is the result of 
    an hexagonal erosion followed by an erosion by a conjugate hexagon.
    The respective sizes of the hexagon and of the conjugate hexagon are calculated
    in order that the final dodecagon be as isotropic as possible.
    """
    
    n1 = int(0.4641*size)
    n1 += abs(n1 % 2 - size % 2)
    n2 =(size - n1)//2
    conjugateHexagonalErode(imIn, imOut, n2, edge=edge)
    erode(imOut, imOut, n1, se=HEXAGON, edge=edge)
    
def dodecagonalDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a dodecagon (hexagonal grid). This operation is the result of 
    an hexagonal dilation followed by a dilation by a conjugate hexagon.
    The respective sizes of the hexagon and of the conjugate hexagon are calculated
    in order that the final dodecagon be as isotropic as possible.
    """
    
    n1 = int(0.4641*size)
    n1 += abs(n1 % 2 - size % 2)
    n2 =(size - n1)//2
    conjugateHexagonalDilate(imIn, imOut, n2, edge=edge)
    dilate(imOut, imOut, n1, se=HEXAGON, edge=edge)
        
# The following operators are defined on the square grid only
def octogonalErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by an octogon (square grid). This operation is the result of 
    an erosion by a square followed by an erosion by a diamond (conjugate square).
    The respective sizes of the square and of the diamond are calculated in order
    that the final octogon be as isotropic as possible.
    """
    
    n1 = int(0.41421*size + 0.5)
    n2 = size - n1
    erode(imIn, imOut, n1, se=SQUARE3X3, edge=edge)
    erode(imOut, imOut, n2, se=DIAMOND, edge=edge)

def octogonalDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by an octogon (square grid). This operation is the result of 
    a dilation by a square followed by a dilation by a diamond.
    The respective sizes of the square and of the diamond are calculated in order
    that the final octogon be as isotropic as possible.
    """
    
    n1 = int(0.41421*size + 0.5)
    n2 = size - n1
    dilate(imIn, imOut, n1, se=SQUARE3X3, edge=edge)
    dilate(imOut, imOut, n2, se=DIAMOND, edge=edge)

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
  
def isotropicDistance(imIn, imOut, edge=mamba.FILLED):
    """
    Computes the distance function of a set in 'imIn'. This distance function
    uses dodecagonal erosions and the grid is assumed to be hexagonal.
    The procedure is quite slow but the result is more aesthetic.
    This operator also illustrates how to perform successive dodecagonal
    operations of increasing sizes.
    """
    
    if imIn.getDepth() != 1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
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

