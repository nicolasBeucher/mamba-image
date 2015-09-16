"""
Filtering operators.

This module provides a set of functions to perform morphological filtering 
operations such as alternate filters.
"""

import mamba

# contributors: Serge BEUCHER, Nicolas BEUCHER

def alternateFilter(imIn, imOut,n, openFirst, se=mamba.DEFAULT_SE):
    """
    Performs an alternate filter operation of size 'n' on image 'imIn' and puts
    the result in 'imOut'. If 'openFirst' is True, the filter begins with an
    opening, a closing otherwise.
    """
    
    if openFirst:
        mamba.opening(imIn, imOut, n, se=se)
        mamba.closing(imOut, imOut, n, se=se)
    else:
        mamba.closing(imIn, imOut, n, se=se)
        mamba.opening(imOut, imOut, n, se=se)

def fullAlternateFilter(imIn, imOut, n, openFirst, se=mamba.DEFAULT_SE):
    """
    Performs a full alternate filter operation (successive alternate filters of
    increasing sizes, from 1 to 'n') on image 'imIn' and puts the result 
    in 'imOut'. 'n' controls the filter size. If 'openFirst' is True, the filter
    begins with an opening, a closing otherwise.
    """
    
    mamba.copy(imIn, imOut)
    for i in range(1,n+1):
        if openFirst:
            mamba.opening(imOut, imOut, i, se=se)
            mamba.closing(imOut, imOut, i, se=se)
        else:
            mamba.closing(imOut, imOut, i, se=se)
            mamba.opening(imOut, imOut, i, se=se)

def linearAlternateFilter(imIn, imOut, n, openFirst, grid=mamba.DEFAULT_GRID):
    """
    Performs an alternate filter operation on image 'imIn' with openings and
    closings by segments of size 'n' (supremum of openings and infimum of
    closings) and puts the result in 'imOut'. If 'openFirst' is True, the filter
    begins with an opening, a closing otherwise.
    """
    
    if openFirst:
        mamba.supOpen(imIn, imOut, n, grid=grid)
        mamba.infClose(imOut, imOut, n, grid=grid)
    else:
        mamba.infClose(imIn, imOut, n, grid=grid)
        mamba.supOpen(imOut, imOut, n, grid=grid)

def autoMedian(imIn, imOut, n, se=mamba.DEFAULT_SE):
    """
    Morphological automedian filter performed with alternate sequential filters.
    """
    
    oc_im = mamba.imageMb(imIn)
    co_im = mamba.imageMb(imIn)
    imWrk = mamba.imageMb(imIn)
    alternateFilter(imIn, oc_im, n, True, se=se)
    alternateFilter(imIn, co_im, n, False, se=se)
    mamba.copy(imIn, imOut)
    mamba.copy(oc_im, imWrk)
    mamba.logic(co_im, imWrk, imWrk, "sup")
    mamba.logic(imWrk, imOut, imOut, "inf")
    mamba.copy(oc_im, imWrk)
    mamba.logic(co_im, imWrk, imWrk, "inf")
    mamba.logic(imWrk, imOut, imOut, "sup")

def simpleLevelling(imIn, imMask, imOut, grid=mamba.DEFAULT_GRID):
    """
    Performs a simple levelling of image 'imIn' controlled by image 'imMask'
    and puts the result in 'imOut'. This operation is composed of two
    geodesic reconstructions. This filter tends to level regions in the 
    image of homogeneous grey values.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mask_im = mamba.imageMb(imIn, 1)
    mamba.logic(imIn, imMask, imWrk1, "inf")
    mamba.build(imIn, imWrk1, grid=grid)
    mamba.logic(imIn, imMask, imWrk2, "sup")
    mamba.dualBuild(imIn, imWrk2, grid=grid)
    mamba.generateSupMask(imIn, imMask, mask_im, False)
    mamba.convertByMask(mask_im, imOut, 0, mamba.computeMaxRange(imIn)[1])
    mamba.logic(imOut, imWrk1, imWrk1, "inf")
    mamba.negate(imOut, imOut)
    mamba.logic(imOut, imWrk2, imOut, "inf")
    mamba.logic(imWrk1, imOut, imOut, "sup")

def strongLevelling(imIn, imOut, n, eroFirst, grid=mamba.DEFAULT_GRID):
    """
    Strong levelling of 'imIn', result in 'imOut'. 'n' defines the size of the
    erosion and dilation of 'imIn' in the operation. If 'eroFirst' is true, the
    operation starts with an erosion, it starts with a dilation otherwise.
    
    This filter is stronger (more efficient) that simpleLevelling. However, the
    order of the initial operations (erosion and dilation) matters.    
    """
    
    imWrk = mamba.imageMb(imIn)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    if eroFirst:
        mamba.erode(imIn, imWrk, n, se=se)
        mamba.build(imIn, imWrk, grid=grid)
        mamba.dilate(imIn, imOut, n, se=se)
        mamba.dualBuild(imWrk, imOut, grid=grid)
    else:
        mamba.dilate(imIn, imWrk, n, se=se)
        mamba.dualBuild(imIn, imWrk, grid=grid)
        mamba.erode(imIn, imOut, n, se=se)
        mamba.build(imWrk, imOut, grid=grid)

def largeHexagonalAlternateFilter(imIn, imOut, start, end, step, openFirst):
    """
    Fast full alternate hexagonal filter of image 'imIn'. The initial size
    is equal to 'start', the final one is bounded by 'end' (this size is not
    taken into account), the increment of size is 'step'. If 'openFirst' is
    true, the filter starts with on opening. It starts with a closing otherwise.
    The result is put in 'imOut'.
    This operation is efficient if most of the sizes used in the filter are
    greater than 5. If it is not the case, the 'fullAlternateFilter' should
    be used instead.    
    """
    
    prev = 0
    mamba.copy(imIn, imOut)
    if openFirst:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeHexagonalErode(imOut, imOut, t1)
            mamba.largeHexagonalDilate(imOut, imOut, t2)
            prev = i
        mamba.largeHexagonalErode(imOut, imOut, prev)
    else:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeHexagonalDilate(imOut, imOut, t1)
            mamba.largeHexagonalErode(imOut, imOut, t2)
            prev = i
        mamba.largeHexagonalDilate(imOut, imOut, prev)

def largeDodecagonalAlternateFilter(imIn, imOut, start, end, step, openFirst):
    """
    Fast full alternate dodecagonal filter of image 'imIn'. The initial size
    is equal to 'start', the final one is bounded by 'end' (this size is not
    taken into account), the increment of size is 'step'. If 'openFirst' is
    true, the filter starts with on opening. It starts with a closing otherwise.
    The result is put in 'imOut'.
    """
    
    prev = 0
    mamba.copy(imIn, imOut)
    if openFirst:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeDodecagonalErode(imOut, imOut, t1)
            mamba.largeDodecagonalDilate(imOut, imOut, t2)
            prev = i
        mamba.largeDodecagonalErode(imOut, imOut, prev)
    else:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeDodecagonalDilate(imOut, imOut, t1)
            mamba.largeDodecagonalErode(imOut, imOut, t2)
            prev = i
        mamba.largeDodecagonalDilate(imOut, imOut, prev)

def largeSquareAlternateFilter(imIn, imOut, start, end, step, openFirst):
    """
    Fast full alternate square filter of image 'imIn'. The initial size
    is equal to 'start', the final one is bounded by 'end' (this size is not
    taken into account), the increment of size is 'step'. If 'openFirst' is
    true, the filter starts with on opening. It starts with a closing otherwise.
    The result is put in 'imOut'.
    This operation is efficient if most of the sizes used in the filter are
    greater than 5. If it is not the case, the 'fullAlternateFilter' should
    be used instead (with a SQUARE structuring element).    
    """
    
    prev = 0
    mamba.copy(imIn, imOut)
    if openFirst:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeSquareErode(imOut, imOut, t1)
            mamba.largeSquareDilate(imOut, imOut, t2)
            prev = i
        mamba.largeSquareErode(imOut, imOut, prev)
    else:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeSquareDilate(imOut, imOut, t1)
            mamba.largeSquareErode(imOut, imOut, t2)
            prev = i
        mamba.largeSquareDilate(imOut, imOut, prev)

def largeOctogonalAlternateFilter(imIn, imOut, start, end, step, openFirst):
    """
    Fast full alternate octogonal filter of image 'imIn'. The initial size
    is equal to 'start', the final one is limited by 'end' (this size is not
    taken into account), the increment of size is 'step'. If 'openFirst' is
    true, the filter starts with on opening. It starts with a closing otherwise.
    The result is put in 'imOut'.
    """
    
    prev = 0
    mamba.copy(imIn, imOut)
    if openFirst:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeOctogonalErode(imOut, imOut, t1)
            mamba.largeOctogonalDilate(imOut, imOut, t2)
            prev = i
        mamba.largeOctogonalErode(imOut, imOut, prev)
    else:
        for i in range(start, end, step):
            t1 = i + prev
            t2 = 2 * i
            mamba.largeOctogonalDilate(imOut, imOut, t1)
            mamba.largeOctogonalErode(imOut, imOut, t2)
            prev = i
        mamba.largeOctogonalDilate(imOut, imOut, prev)

