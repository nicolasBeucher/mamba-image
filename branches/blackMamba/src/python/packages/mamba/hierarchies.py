"""
Hierarchical segmentation operators.

This module provides a set of functions to perform hierarchical segmentation
operations. This module contains the waterfalls algorithm and various hierarchical
operators (enhanced waterfalls, standard hierarchy and P algorithm).
"""

# Contributor: Serge BEUCHER, Nicolas BEUCHER

import mamba

def hierarchy(imIn, imMask, imOut, grid=mamba.DEFAULT_GRID):
    """
    Construction of a hierarchical image from image 'imIn' and with 'imMask'.
    The binary image 'imMask' controls the dual reconstruction (propagation)
    of 'imIn'.
    This operator is mainly used to build hierarchical images from valued
    watershed images.
    The hierarchical image is put in 'imOut'.
    """
    
    imWrk = mamba.imageMb(imIn)
    if mamba.checkEmptiness(imIn):
        mamba.copy(imIn, imOut)
    else:
        mamba.convertByMask(imMask, imWrk, 255, 0)
        mamba.logic(imIn, imWrk, imWrk, "sup")
        mamba.hierarDualBuild(imIn, imWrk)
        mamba.copy(imWrk, imOut)

def hierarchicalLevel(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Computes the next hierarchical level of image 'imIn' in the
    waterfalls transformation and puts the result in 'imOut'.
    This operation makes sure that the next hierarchical level is embedded
    in the previous one.
    'imIn' must be a valued watershed image.
    """
    
    imWrk0 = mamba.imageMb(imIn)
    imWrk1 = mamba.imageMb(imIn, 1)
    imWrk2 = mamba.imageMb(imIn, 1)
    imWrk3 = mamba.imageMb(imIn, 1)
    imWrk4 = mamba.imageMb(imIn, 32)
    mamba.threshold(imIn,imWrk1, 0, 0)
    mamba.negate(imWrk1, imWrk2)
    hierarchy(imIn, imWrk2, imWrk0, grid=grid)
    mamba.minima(imWrk0, imWrk2, grid=grid)
    mamba.label(imWrk2, imWrk4, grid=grid)
    mamba.watershedSegment(imWrk0, imWrk4, grid=grid)
    mamba.copyBytePlane(imWrk4, 3, imWrk0)
    mamba.threshold(imWrk0, imWrk2, 0, 0)
    mamba.diff(imWrk1, imWrk2, imWrk3)
    mamba.build(imWrk1, imWrk3)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    mamba.dilate(imWrk3, imWrk1, 1, se)
    mamba.diff(imWrk2, imWrk1, imWrk1)
    mamba.logic(imWrk1, imWrk3, imWrk1, "sup")
    mamba.convertByMask(imWrk1, imWrk0, 255, 0)
    mamba.logic(imIn, imWrk0, imOut, "inf")

def waterfalls(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Classical waterfall algorithm. All the hierarchical levels of greyscale
    image 'imIn' (which must be a valued watershed) are computed.
    'imOut' contains all these hierarchies which are embedded, so that
    hierarchy i is simply obtained by a threshold at [i+1, 255].
    This transformation returns the number of hierarchical levels.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn, 1)
    mamba.copy(imIn, imWrk1)
    imOut.reset()
    nbLevels = 0
    mamba.threshold(imWrk1, imWrk3, 1, 255)
    while mamba.computeVolume(imWrk3) != 0:
        mamba.add(imOut, imWrk3, imOut)
        hierarchicalLevel(imWrk1, imWrk2, grid=grid)
        mamba.threshold(imWrk2, imWrk3, 1, 255)
        mamba.copy(imWrk2, imWrk1)
        nbLevels += 1
    return nbLevels

def enhancedWaterfalls(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Enhanced waterfall algorithm. Compared to the classical waterfalls
    algorithm, this one adds the contours of the watershed transform which are
    above the hierarchical image associated to the next level of hierarchy. This
    waterfalls transform also ends to an empty set. All the hierarchical levels
    of image 'imIn' (which is a valued watershed) are computed. 'imOut' contains
    all these hierarchies which are embedded, so that hierarchy i is simply 
    obtained by a threshold [i+1, 255] of image 'imOut'.
    'imIn' and 'imOut' must be greyscale images. 'imIn' and 'imOu't must be 
    different.
    This transformation returns the number of hierarchical levels.    
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 1)
    imWrk5 = mamba.imageMb(imIn, 32)   
    mamba.copy(imIn, imWrk1)
    imOut.reset()
    nbLevels = 0
    mamba.threshold(imWrk1, imWrk4, 1, 255)
    flag = not(mamba.checkEmptiness(imWrk4))
    while flag:
        mamba.add(imOut, imWrk4, imOut)
        hierarchy(imWrk1, imWrk4, imWrk2, grid=grid)
        mamba.valuedWatershed(imWrk2, imWrk3, grid=grid)
        mamba.threshold(imWrk3, imWrk4, 1, 255)
        flag = not(mamba.checkEmptiness(imWrk4))
        hierarchy(imWrk3, imWrk4, imWrk2, grid=grid)
        mamba.generateSupMask(imWrk2, imWrk1, imWrk4, strict=True)
        mamba.convertByMask(imWrk4, imWrk3, 255, 0)
        mamba.logic(imWrk1, imWrk3, imWrk3, "inf")
        mamba.label(imWrk4, imWrk5, grid=grid)
        mamba.watershedSegment(imWrk3, imWrk5, grid=grid)
        mamba.copyBytePlane(imWrk5, 3, imWrk1)
        mamba.logic(imWrk1, imWrk3, imWrk1, "inf")
        mamba.threshold(imWrk1, imWrk4, 1, 255)
        nbLevels += 1
    return nbLevels
    
def standardSegment(imIn, imOut, gain=2.0, grid=mamba.DEFAULT_GRID):
    """
    General standard segmentation. This algorithm keeps the contours of the 
    watershed transform which are above or equal to the hierarchical image 
    associated to the next level of hierarchy when the altitude of the contour
    is multiplied by a 'gain' factor (default is 2.0). This transform also ends 
    by idempotence. All the hierarchical levels of image 'imIn'(which is a 
    valued watershed) are computed. 'imOut' contains all these hierarchies which
    are embedded, so that hierarchy i is simply obtained by a threshold
    [i+1, 255] of image 'imOut'.
    'imIn' and 'imOut' must be greyscale images. 'imIn' and 'imOut' must be
    different.
    This transformation returns the number of hierarchical levels.    
    """
    
    imWrk0 = mamba.imageMb(imIn)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 1)
    imWrk5 = mamba.imageMb(imIn, 1)
    imWrk6 = mamba.imageMb(imIn, 32)    
    mamba.copy(imIn, imWrk1)
    mamba.mulRealConst(imIn, gain, imWrk6)
    mamba.floorSubConst(imWrk6, 1, imWrk6)
    mamba.threshold(imWrk6, imWrk4, 255, mamba.computeMaxRange(imWrk6)[1])  
    mamba.copyBytePlane(imWrk6, 0, imWrk0)
    mamba.convert(imWrk4, imWrk2)
    mamba.logic(imWrk0, imWrk2, imWrk0, "sup")
    mamba.logic(imWrk0, imWrk1, imWrk0, "sup")
    imOut.reset()
    nbLevels = 0
    mamba.threshold(imWrk1, imWrk4, 1, 255)
    flag = not(mamba.checkEmptiness(imWrk4))
    while flag:
        hierarchy(imWrk1, imWrk4, imWrk2, grid=grid)
        mamba.add(imOut, imWrk4, imOut)
        mamba.valuedWatershed(imWrk2, imWrk3, grid=grid)
        mamba.threshold(imWrk3, imWrk5, 1, 255)
        flag = not(mamba.checkEmptiness(imWrk5))
        hierarchy(imWrk3, imWrk5, imWrk2, grid=grid)
        mamba.generateSupMask(imWrk0, imWrk2, imWrk5, strict=False)
        mamba.logic(imWrk4, imWrk5, imWrk4, "inf")
        mamba.convertByMask(imWrk4, imWrk3, 0, 255)
        mamba.logic(imWrk1, imWrk3, imWrk3, "inf")
        mamba.negate(imWrk4, imWrk4)
        mamba.label(imWrk4, imWrk6, grid=grid)
        mamba.watershedSegment(imWrk3, imWrk6, grid=grid)
        mamba.copyBytePlane(imWrk6, 3, imWrk3)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        mamba.logic(imWrk1, imWrk3, imWrk1, "inf")
        mamba.threshold(imWrk1, imWrk4, 1, 255)
        nbLevels += 1
    return nbLevels

def segmentByP(imIn, imOut, gain=2.0, grid=mamba.DEFAULT_GRID):
    """
    General segmentation by P algorithm. This algorithm keeps or reintroduces
    the contours of the initial watershed transform which are above or equal to
    the hierarchical image associated to the next level of hierarchy when the
    altitude of the contour is multiplied by a 'gain' factor (default is 2.0).
    This transform also ends by idempotence. All the hierarchical levels of
    image 'imIn' (which is a valued watershed) are computed. 'imOut' contains all
    these hierarchies which are embedded, so that hierarchy i is simply obtained
    by a threshold [i+1, 255] of image imOut.
    'imIn' and 'imOut' must be greyscale images. 'imIn' and 'imOut' must be
    different.
    This transformation returns the number of hierarchical levels.    
    """
    
    imWrk0 = mamba.imageMb(imIn)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 1)
    imWrk5 = mamba.imageMb(imIn, 32)    
    mamba.copy(imIn, imWrk1)
    mamba.mulRealConst(imIn, gain, imWrk5)
    mamba.floorSubConst(imWrk5, 1, imWrk5)
    mamba.threshold(imWrk5, imWrk4, 255, mamba.computeMaxRange(imWrk5)[1])  
    mamba.copyBytePlane(imWrk5, 0, imWrk0)
    mamba.convert(imWrk4, imWrk2)
    mamba.logic(imWrk0, imWrk2, imWrk0, "sup")
    mamba.logic(imWrk0, imWrk1, imWrk0, "sup")
    imOut.reset()
    nbLevels = 0
    mamba.threshold(imWrk1, imWrk4, 1, 255)
    flag = not(mamba.checkEmptiness(imWrk4))
    while flag:
        hierarchy(imWrk1, imWrk4, imWrk2, grid=grid)
        mamba.add(imOut, imWrk4, imOut)
        mamba.valuedWatershed(imWrk2, imWrk3, grid=grid)
        mamba.threshold(imWrk3, imWrk4, 1, 255)
        flag = not(mamba.checkEmptiness(imWrk4))
        hierarchy(imWrk3, imWrk4, imWrk2, grid=grid)
        mamba.generateSupMask(imWrk0, imWrk2, imWrk4, strict=False)
        mamba.convertByMask(imWrk4, imWrk3, 0, 255)
        mamba.logic(imWrk1, imWrk3, imWrk3, "inf")
        mamba.negate(imWrk4, imWrk4)
        mamba.label(imWrk4, imWrk5, grid=grid)
        mamba.watershedSegment(imWrk3, imWrk5, grid=grid)
        mamba.copyBytePlane(imWrk5, 3, imWrk3)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        mamba.logic(imWrk1, imWrk3, imWrk1, "inf")
        mamba.threshold(imWrk1, imWrk4, 1, 255)
        nbLevels += 1
    return nbLevels
    
def generalSegment(imIn, imOut, gain=2.0, offset=1, grid=mamba.DEFAULT_GRID):
    """
    General segmentation algorithm. This algorithm is controlled by two
    parameters: the 'gain' (identical to the gain used in standard and P
    segmentation) and a new one, the 'offset'. The 'offset' indicates which
    level of hierarchy is compared to the current hierarchical image.
    The 'offset' is relative to the current hierarchical level. If 'offset' is
    equal to 1, this operator corresponds to the standard segmentation, if
    'offset' is equal to 255 (this value stands for the infinity), the operator
    is equivalent to P algorithm.
    Image 'imOut' contains all these hierarchies which are embedded.
    'imIn' and 'imOut' must be greyscale images. 'imIn' and 'imOut' must be
    different.
    This transformation returns the number of hierarchical levels.    
    """
    
    imWrk0 = mamba.imageMb(imIn)
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 1)
    imWrk5 = mamba.imageMb(imIn, 1)
    imWrk6 = mamba.imageMb(imIn, 32)    
    mamba.copy(imIn, imWrk1)
    mamba.mulRealConst(imIn, gain, imWrk6)
    mamba.floorSubConst(imWrk6, 1, imWrk6)
    mamba.threshold(imWrk6, imWrk4, 255, mamba.computeMaxRange(imWrk6)[1])  
    mamba.copyBytePlane(imWrk6, 0, imWrk0)
    mamba.convert(imWrk4, imWrk2)
    mamba.logic(imWrk0, imWrk2, imWrk0, "sup")
    mamba.logic(imWrk0, imWrk1, imWrk0, "sup")
    imOut.reset()
    nbLevels = 0
    mamba.threshold(imWrk1, imWrk4, 1, 255)
    flag = not(mamba.checkEmptiness(imWrk4))
    while flag:
        nbLevels += 1
        hierarchy(imWrk1, imWrk4, imWrk2, grid=grid)
        mamba.add(imOut, imWrk4, imOut)
        v = max(nbLevels - offset, 0) + 1
        mamba.threshold(imOut, imWrk4, v, 255)
        mamba.valuedWatershed(imWrk2, imWrk3, grid=grid)
        mamba.threshold(imWrk3, imWrk5, 1, 255)
        flag = not(mamba.checkEmptiness(imWrk5))
        hierarchy(imWrk3, imWrk5, imWrk2, grid=grid)
        mamba.generateSupMask(imWrk0, imWrk2, imWrk5, strict=False)
        mamba.logic(imWrk4, imWrk5, imWrk4, "inf")
        mamba.convertByMask(imWrk4, imWrk3, 0, 255)
        mamba.logic(imWrk1, imWrk3, imWrk3, "inf")
        mamba.negate(imWrk4, imWrk4)
        mamba.label(imWrk4, imWrk6, grid=grid)
        mamba.watershedSegment(imWrk3, imWrk6, grid=grid)
        mamba.copyBytePlane(imWrk6, 3, imWrk3)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        mamba.logic(imWrk1, imWrk3, imWrk1, "inf")
        mamba.threshold(imWrk1, imWrk4, 1, 255)
    return nbLevels
    
def extendedSegment(imIn, imTest, imOut, offset=255, grid=mamba.DEFAULT_GRID):
    """
    Extended (experimental) segmentation algorithm. This algorithm is controlled
    by image 'imTest'. The current hierarchical image is compared to image
    'imTest'. This image must be a greyscale image. The 'offset' indicates which
    level of hierarchy is compared to the current hierarchical image.
    The 'offset' is relative to the current hierarchical level (by default,
    'offset' is equal to 255, so that the initial segmentation is used).
    Image 'imOut' contains all these hierarchies which are embedded.
    'imIn', 'imTest' and 'imOut' must be greyscale images.
    'imIn', 'imTest' and 'imOut' must be different.
    This transformation returns the number of hierarchical levels.    
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 1)
    imWrk5 = mamba.imageMb(imIn, 1)
    imWrk6 = mamba.imageMb(imIn, 32)    
    mamba.copy(imIn, imWrk1)
    imOut.reset()
    nbLevels = 0
    mamba.threshold(imWrk1, imWrk4, 1, 255)
    flag = not(mamba.checkEmptiness(imWrk4))
    while flag:
        nbLevels += 1
        hierarchy(imWrk1, imWrk4, imWrk2, grid=grid)
        mamba.add(imOut, imWrk4, imOut)
        v = max(nbLevels - offset, 0) + 1
        mamba.threshold(imOut, imWrk4, v, 255)
        mamba.valuedWatershed(imWrk2, imWrk3, grid=grid)
        mamba.threshold(imWrk3, imWrk5, 1, 255)
        flag = not(mamba.checkEmptiness(imWrk5))
        hierarchy(imWrk3, imWrk5, imWrk2, grid=grid)
        mamba.generateSupMask(imTest, imWrk2, imWrk5, strict=False)
        mamba.logic(imWrk4, imWrk5, imWrk4, "inf")
        mamba.convertByMask(imWrk4, imWrk3, 0, 255)
        mamba.logic(imWrk1, imWrk3, imWrk3, "inf")
        mamba.negate(imWrk4, imWrk4)
        mamba.label(imWrk4, imWrk6, grid=grid)
        mamba.watershedSegment(imWrk3, imWrk6, grid=grid)
        mamba.copyBytePlane(imWrk6, 3, imWrk3)
        mamba.logic(imWrk1, imWrk2, imWrk1, "sup")
        mamba.logic(imWrk1, imWrk3, imWrk1, "inf")
        mamba.threshold(imWrk1, imWrk4, 1, 255)
    return nbLevels
    
