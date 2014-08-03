"""
Residual operators.

This module provides a set of functions to perform residual operations.
A residual transformation is built by subtracting two sequences of primitive 
operators to get residues and by computing the supremum of these residues. The
position in the sequence where this maximum occurs is also computed (it is
called associated function and is generally a 32-bit image).
These residues are defined on binary and greytone images. 
"""

# Contributor: Serge BEUCHER

import mamba

def _generateMask_(imIn1, imIn2, imOut):
    #This procedure is used internally by the residues operators. It computes
    #a mask indicating the points in the image where 'imIn1' is greater or equal
    #to 'imIn2' with 'imIn1' strictly positive.
    #Depth of 'imOut' is 1.
    
    imWrk = mamba.imageMb(imOut)
    mamba.generateSupMask(imIn1, imIn2, imOut, False)
    if imIn1.getDepth()==1:
        mamba.negate(imIn1, imWrk)
    else:
        mamba.threshold(imIn1, imWrk, 0, 0)
    mamba.diff(imOut, imWrk, imOut)

def binaryUltimateErosion(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Ultimate erosion of binary image 'imIn'. 'imOut1' contains the ultimate 
    eroded set and 'imOut2' contains the associated function (that is the 
    height of each connected component of the ultimate erosion).
    
    An ultimate erosion is composed of the union of the last connected
    components of the successive erosions of the initial set. The associated
    function provides the size of the corresponding erosion.
    
    Depth of 'imOut1' is 1, depth of 'imOut2' is 32. 

    The operation is fast because it is computed using the distance function
    of 'imIn' (the ultimate erosion is identical to the maxima of this
    distance function).

    The edge is set to 'FILLED' by default.
    """

    imWrk1 = mamba.imageMb(imIn, 32)
    imWrk2 = mamba.imageMb(imIn, 32)
    mamba.computeDistance(imIn, imWrk1, grid=grid, edge=edge)
    mamba.maxima(imWrk1, imOut1, grid=grid)
    mamba.convertByMask(imOut1, imWrk2, 0, mamba.computeMaxRange(imWrk2)[1])
    mamba.logic(imWrk1, imWrk2, imOut2, "inf")

def ultimateErosion(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID):
    """
    General ultimate erosion working on greytone image 'imIn'. 'imOut1'
    contains the ultimate eroded function and 'imOut2' contains the 
    associated function.
    
    This ultimate erosion can be applied to greytone images.

    Depth of 'imOut1' is the same as 'imIn', depth of 'imOut2' is 32. 

    The edge is always set to 'FILLED'.
    """

    maskIm = mamba.imageMb(imIn, 1)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 32)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    i = 0
    mamba.copy(imIn, imWrk1)
    v2 = mamba.computeVolume(imWrk1)
    v1 = v2 + 1
    imOut1.reset()
    imOut2.reset()
    while v1 > v2:
        i += 1
        v1 = v2
        mamba.erode(imWrk1, imWrk2, se=se)
        mamba.build(imWrk1, imWrk2, grid=grid)
        mamba.sub(imWrk1, imWrk2, imWrk2)
        _generateMask_(imWrk2, imOut1, maskIm)
        mamba.convertByMask(maskIm, imWrk3, 0, i)
        mamba.logic(imOut1, imWrk2, imOut1, "sup")
        mamba.logic(imOut2, imWrk3, imOut2, "sup")
        mamba.erode(imWrk1, imWrk1, se=se)
        v2 = mamba.computeVolume(imWrk1)

def binarySkeletonByOpening(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Skeleton by openings (maximal balls skeleton) of binary image 'imIn'.
    'imOut1' contains the skeleton points (centers of maximal balls) and
    'imOut2' contains the associated function (that is the radius of each
    maximal ball included in the initial set.

    The operation is fast because it is computed through the use of the
    distance function of 'imIn' (skeleton points can be obtained by a
    Top Hat transform on the distance function).

    The edge is set to 'FILLED' by default.
    """

    imWrk1 = mamba.imageMb(imIn, 32)
    imWrk2 = mamba.imageMb(imIn, 32)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    mamba.computeDistance(imIn, imWrk1, grid=grid, edge=edge)
    mamba.whiteTopHat(imWrk1, imWrk2, 1, se=se)
    mamba.threshold(imWrk2, imOut1, 1, mamba.computeMaxRange(imWrk2)[1])
    mamba.convertByMask(imOut1, imWrk2, 0, mamba.computeMaxRange(imWrk2)[1])
    mamba.logic(imWrk1, imWrk2, imOut2, "inf")

def skeletonByOpening(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID):
    """
    General skeleton by openings working on greytone image 'imIn'.
    'imOut1' contains the skeleton function and 'imOut2' contains the 
    associated function.
    
    This skeleton corresponds to the centers of maximal cylinders included
    in the set under the graph of the image 'imIn'.
    
    Depth of 'imOut1' is the same as 'imIn', depth of 'imOut2' is 32. 

    The edge is always set to 'FILLED'.
    """

    maskIm = mamba.imageMb(imIn, 1)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 32)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    i = 0
    mamba.copy(imIn, imWrk1)
    v2 = mamba.computeVolume(imWrk1)
    v1 = v2 + 1
    imOut1.reset()
    imOut2.reset()
    while v1 > v2:
        i += 1
        v1 = v2
        mamba.opening(imWrk1, imWrk2, se=se)
        mamba.sub(imWrk1, imWrk2, imWrk2)
        _generateMask_(imWrk2, imOut1, maskIm)
        mamba.convertByMask(maskIm, imWrk3, 0, i)
        mamba.logic(imOut1, imWrk2, imOut1, "sup")
        mamba.logic(imOut2, imWrk3, imOut2, "sup")
        mamba.erode(imWrk1, imWrk1, se=se)
        v2 = mamba.computeVolume(imWrk1)

def ultimateOpening(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID):
    """
    Ultimate opening of image 'imIn'. 'imOut1' contains the ultimate 
    opening whereas 'imOut2' contains the granulometric function.
    
    Ultimate opening is obtained by using successive openings by hexagons or
    squares as primitive functions depending of the grid in use.
    
    Depth of 'imOut1' is the same as 'imIn', depth of 'imOut2' is 32. 
    """

    maskIm = mamba.imageMb(imIn, 1)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 32)
    imWrk4 = mamba.imageMb(imIn)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    i = 0
    mamba.copy(imIn, imWrk1)
    v2 = mamba.computeVolume(imWrk1)
    mamba.copy(imWrk1, imWrk4)
    v1 = v2 + 1
    imOut1.reset()
    imOut2.reset()
    if grid == mamba.HEXAGONAL:
        dilation = mamba.largeHexagonalDilate
    else:
        dilation = mamba.largeSquareDilate
    while v1 > v2:
        i += 1
        v1 = v2
        mamba.erode(imWrk4, imWrk4, se=se)
        dilation(imWrk4, imWrk2, i)
        mamba.sub(imWrk1, imWrk2, imWrk1)
        _generateMask_(imWrk1, imOut1, maskIm)
        mamba.convertByMask(maskIm, imWrk3, 0, i)
        mamba.logic(imOut1, imWrk1, imOut1, "sup")
        mamba.logic(imOut2, imWrk3, imOut2, "sup")
        v2 = mamba.computeVolume(imWrk4)
        mamba.copy(imWrk2, imWrk1)
        
def ultimateIsotropicOpening(imIn, imOut1, imOut2, step =1, grid=mamba.DEFAULT_GRID):
    """
    Ultimate opening of image 'imIn' with more isotropic structuring elements.
    Dodecagons are used on hexagonal grid, octogons on square grid. 'imOut1' 
    contains the ultimate opening whereas 'imOut2' contains the granulometric
    function. 'step' is the increment of the size of the openings. Its default
    value is 1 but it can be increased to reduce the computation time.

    Depth of 'imOut1' is the same as 'imIn', depth of 'imOut2' is 32. 
    """

    maskIm = mamba.imageMb(imIn, 1)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 32)
    i = 0
    mamba.copy(imIn, imWrk1)
    v2 = mamba.computeVolume(imWrk1)
    v1 = v2 + 1
    imOut1.reset()
    imOut2.reset()
    if grid == mamba.HEXAGONAL:
        iso_dilation = mamba.largeDodecagonalDilate
        iso_erosion = mamba.largeDodecagonalErode
    else:
        iso_dilation = mamba.largeOctogonalDilate
        iso_erosion = mamba.largeOctogonalErode
    while v1 > v2:
        i += step
        v1 = v2
        iso_erosion(imWrk1, imWrk2, i)
        v2 = mamba.computeVolume(imWrk2)
        iso_dilation(imWrk2, imWrk2, i)
        mamba.sub(imWrk1, imWrk2, imWrk1)
        _generateMask_(imWrk1, imOut1, maskIm)
        mamba.convertByMask(maskIm, imWrk3, 0, i)
        mamba.logic(imOut1, imWrk1, imOut1, "sup")
        mamba.logic(imOut2, imWrk3, imOut2, "sup")
        mamba.copy(imWrk2, imWrk1)

def ultimateBuildOpening(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID):
    """
    Ultimate opening  by build of image 'imIn'. 'imOut1' contains the ultimate
    opening whereas 'imOut2' contains the granulometric function.
    
    This ultimate opening is obtained by using successive openings by build.
    
    Depth of 'imOut1' is the same as 'imIn', depth of 'imOut2' is 32. 
    """

    maskIm = mamba.imageMb(imIn, 1)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 32)
    imWrk4 = mamba.imageMb(imIn)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    i = 0
    mamba.copy(imIn, imWrk1)
    v2 = mamba.computeVolume(imWrk1)
    mamba.copy(imWrk1, imWrk4)
    v1 = v2 + 1
    imOut1.reset()
    imOut2.reset()
    while v1 > v2:
        i += 1
        v1 = v2
        mamba.erode(imWrk4, imWrk4, se=se)
        mamba.copy(imWrk4, imWrk2)
        mamba.hierarBuild(imWrk1, imWrk2, grid=mamba.DEFAULT_GRID)
        mamba.sub(imWrk1, imWrk2, imWrk1)
        _generateMask_(imWrk1, imOut1, maskIm)
        mamba.convertByMask(maskIm, imWrk3, 0, i)
        mamba.logic(imOut1, imWrk1, imOut1, "sup")
        mamba.logic(imOut2, imWrk3, imOut2, "sup")
        v2 = mamba.computeVolume(imWrk4)
        mamba.copy(imWrk2, imWrk1)
         
def _initialQuasiDist_(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID):
    """
    Computes the initial quasi-distance. For internal use only. The resulting
    quasi-distance is not lipchitzian (see MM documentation for details).
    """
    
    maskIm = mamba.imageMb(imIn, 1)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 32)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    i = 0
    mamba.copy(imIn, imWrk1)
    v2 = mamba.computeVolume(imWrk1)
    v1 = v2 + 1
    imOut1.reset()
    imOut2.reset()
    while v1 > v2:
        i += 1
        v1 = v2
        mamba.erode(imWrk1, imWrk2, se=se)
        mamba.sub(imWrk1, imWrk2, imWrk1)
        _generateMask_(imWrk1, imOut1, maskIm)
        mamba.convertByMask(maskIm, imWrk3, 0, i)
        mamba.logic(imOut1, imWrk1, imOut1, "sup")
        mamba.logic(imOut2, imWrk3, imOut2, "sup")
        mamba.copy(imWrk2, imWrk1)
        v2 = mamba.computeVolume(imWrk1)
       
def quasiDistance(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID):
    """
    Quasi-distance of image 'imIn'. 'imOut1' contains the residues image
    and 'imOut2' contains the quasi-distance (associated function).
    
    The quasi-distance of a greytone image is made of a patch of distance
    functions of some almost flat regions in the image. When the image is a
    simple indicator function of a set, the quasi-distance and the distance
    function are identical.

    Depth of 'imOut1' is the same as 'imIn', depth of 'imOut2' is 32.
    """

    imWrk1 = mamba.imageMb(imIn, 32)
    imWrk2 = mamba.imageMb(imIn, 32)
    imWrk3 = mamba.imageMb(imIn, 32)
    maskIm = mamba.imageMb(imIn, 1) 
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    _initialQuasiDist_(imIn, imOut1, imOut2, grid=grid)
    mamba.copy(imOut2, imWrk1)
    v1 = mamba.computeVolume(imOut2)
    v2 = v1 + 1
    while v2 > v1:
        v2 = v1
        mamba.erode(imWrk1, imWrk2, se=se)
        mamba.sub(imWrk1, imWrk2, imWrk2)
        mamba.threshold(imWrk2, maskIm, 2, mamba.computeMaxRange(imWrk2)[1])
        mamba.convertByMask(maskIm, imWrk3, 0, mamba.computeMaxRange(imWrk3)[1])
        mamba.logic(imWrk2, imWrk3, imWrk2, "inf")
        mamba.subConst(imWrk2, 1, imWrk3)
        mamba.logic(imWrk2, imWrk3, imWrk2, "inf") # Patch non saturated subtraction
        mamba.sub(imWrk1, imWrk2, imWrk1)
        v1 = mamba.computeVolume(imWrk1)
    mamba.copy(imWrk1, imOut2)

def fullRegularisedGradient(imIn, imOut1, imOut2, grid=mamba.DEFAULT_GRID, maxSize=16):
    """
    Full regularised morphological gradient of image 'imIn'. This operator
    is a residual transform which uses the regularised gradient of size i as
    a residue. The range of sizes i is limited to 16 by default, as beyond this
    value, the residue is most of the time equal to 0.
    
    Warning! 'imOut2' is a greyscale image (depth equal to 8).
    """

    imWrk = mamba.imageMb(imIn)
    maskIm = mamba.imageMb(imIn, 1) 
    imOut1.reset()
    imOut2.reset()
    for i in range(1, maxSize + 1):
        mamba.regularisedGradient(imIn, imWrk, i, grid=grid)
        _generateMask_(imWrk, imOut1, maskIm)
        mamba.logic(imOut1, imWrk, imOut1, "sup")
        mamba.convertByMask(maskIm, imWrk, 0, i)
        mamba.logic(imOut2, imWrk, imOut2, "sup")
 
