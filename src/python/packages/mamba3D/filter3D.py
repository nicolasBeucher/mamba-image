"""
Filtering operators.

This module provides a set of functions to perform morphological filtering 
operations such as alternate filters.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba

def alternateFilter3D(imIn, imOut,n, openFirst, se=m3D.CUBOCTAHEDRON1):
    """
    Performs an alternate filter operation of size 'n' on 3D image 'imIn'
    and puts the result in 'imOut'. If 'openFirst' is True, the filter
    begins with an opening, a closing otherwise.
    """
    
    if openFirst:
        m3D.opening3D(imIn, imOut, n, se=se)
        m3D.closing3D(imOut, imOut, n, se=se)
    else:
        m3D.closing3D(imIn, imOut, n, se=se)
        m3D.opening3D(imOut, imOut, n, se=se)

def fullAlternateFilter3D(imIn, imOut, n, openFirst, se=m3D.CUBOCTAHEDRON1):
    """
    Performs a full alternate filter operation (successive alternate filters of
    increasing sizes, from 1 to 'n') on 3D image 'imIn' and puts the result 
    in 'imOut'. 'n' controls the filter size. If 'openFirst' is True, the filter
    begins with an opening, a closing otherwise.
    """
    
    m3D.copy3D(imIn, imOut)
    for i in range(1,n+1):
        if openFirst:
            m3D.opening3D(imOut, imOut, i, se=se)
            m3D.closing3D(imOut, imOut, i, se=se)
        else:
            m3D.closing3D(imOut, imOut, i, se=se)
            m3D.opening3D(imOut, imOut, i, se=se)

def linearAlternateFilter3D(imIn, imOut, n, openFirst, grid=m3D.DEFAULT_GRID3D):
    """
    Performs an alternate filter operation on 3D image 'imIn' with openings and
    closings by segments of size 'n' (supremeum of openings and infimum of
    closings) and puts the result in 'imOut'. If 'openFirst' is True, the filter
    begins with an opening, a closing otherwise.
    """
    
    if openFirst:
        m3D.supOpen3D(imIn, imOut, n, grid=grid)
        m3D.infClose3D(imOut, imOut, n, grid=grid)
    else:
        m3D.infClose3D(imIn, imOut, n, grid=grid)
        m3D.supOpen3D(imOut, imOut, n, grid=grid)

def autoMedian3D(imIn, imOut, n, se=m3D.CUBOCTAHEDRON1):
    """
    Morphological automedian filter performed with alternate sequential filters.
    """
    
    oc_im = m3D.image3DMb(imIn)
    co_im = m3D.image3DMb(imIn)
    imWrk = m3D.image3DMb(imIn)
    alternateFilter3D(imIn, oc_im, n, True, se=se)
    alternateFilter3D(imIn, co_im, n, False, se=se)
    m3D.copy3D(imIn, imOut)
    m3D.copy3D(oc_im, imWrk)
    m3D.logic3D(co_im, imWrk, imWrk, "sup")
    m3D.logic3D(imWrk, imOut, imOut, "inf")
    m3D.copy3D(oc_im, imWrk)
    m3D.logic3D(co_im, imWrk, imWrk, "inf")
    m3D.logic3D(imWrk, imOut, imOut, "sup")

def simpleLevelling3D(imIn, imMask, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Performs a simple levelling of 3D image 'imIn' controlled by image 'imMask'
    and puts the result in 'imOut'. This operation is composed of two
    geodesic reconstructions. This filter tends to level regions in the 
    image of homogeneous grey values.
    """
    
    imWrk1 = m3D.image3DMb(imIn)
    imWrk2 = m3D.image3DMb(imIn)
    mask_im = m3D.image3DMb(imIn, 1)
    m3D.logic3D(imIn, imMask, imWrk1, "inf")
    m3D.build3D(imIn, imWrk1, grid=grid)
    m3D.logic3D(imIn, imMask, imWrk2, "sup")
    m3D.dualBuild3D(imIn, imWrk2, grid=grid)
    m3D.generateSupMask3D(imIn, imMask, mask_im, False)
    m3D.convertByMask3D(mask_im, imOut, 0, m3D.computeMaxRange3D(imIn)[1])
    m3D.logic3D(imOut, imWrk1, imWrk1, "inf")
    m3D.negate3D(imOut, imOut)
    m3D.logic3D(imOut, imWrk2, imOut, "inf")
    m3D.logic3D(imWrk1, imOut, imOut, "sup")

def strongLevelling3D(imIn, imOut, n, eroFirst, grid=m3D.DEFAULT_GRID3D):
    """
    Strong levelling of 'imIn', result in 'imOut'. 'n' defines the size of the
    erosion and dilation of 'imIn' in the operation. If 'eroFirst' is true, the
    operation starts with an erosion, it starts with a dilation otherwise.
    
    This filter is stronger (more efficient) that simpleLevelling3D. However, the
    order of the initial operations (erosion and dilation) matters.
    """
    
    imWrk = m3D.image3DMb(imIn)
    se = m3D.structuringElement3D(m3D.getDirections3D(grid), grid)
    if eroFirst:
        m3D.erode3D(imIn, imWrk, n, se=se)
        m3D.build3D(imIn, imWrk, grid=grid)
        m3D.dilate3D(imIn, imOut, n, se=se)
        m3D.dualBuild3D(imWrk, imOut, grid=grid)
    else:
        m3D.dilate3D(imIn, imWrk, n, se=se)
        m3D.dualBuild3D(imIn, imWrk, grid=grid)
        m3D.erode3D(imIn, imOut, n, se=se)
        m3D.build3D(imWrk, imOut, grid=grid)


