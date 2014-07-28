"""
This module provides a set of functions to perform geodesic computations on
3D images using Mamba based functions.

It includes build and dualbuild operations, computation of maxima and minima...
"""

# Contributors: Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

################################################################################
# Private functions to cover all the depth case for build and dualbuild 
# functions

def _build3D_1(imMask, imInout, grid):
    # build function for binary 3D images
    if imMask.getDepth()!=1:
        mamba.raiseExceptionOnError(core.ERR_BAD_DEPTH)
    imMask_8 = m3D.image3DMb(imMask, 8)
    imInout_8= m3D.image3DMb(imInout, 8)
    m3D.convert3D(imMask, imMask_8)
    m3D.convert3D(imInout, imInout_8)
    err = core.MB3D_HierarBld(imMask_8.mb3DIm, imInout_8.mb3DIm, grid.getCValue())
    mamba.raiseExceptionOnError(err)
    m3D.convert3D(imMask_8, imMask)
    m3D.convert3D(imInout_8, imInout)

def _dualBuild3D_1(imMask, imInout, grid):
    # build function for binary 3D images
    if imMask.getDepth()!=1:
        mamba.raiseExceptionOnError(core.ERR_BAD_DEPTH)
    imMask_8 = m3D.image3DMb(imMask, 8)
    imInout_8= m3D.image3DMb(imInout, 8)
    m3D.convert3D(imMask, imMask_8)
    m3D.convert3D(imInout, imInout_8)
    err = core.MB3D_HierarDualBld(imMask_8.mb3DIm, imInout_8.mb3DIm, grid.getCValue())
    mamba.raiseExceptionOnError(err)
    m3D.convert3D(imMask_8, imMask)
    m3D.convert3D(imInout_8, imInout)

################################################################################

def upperGeodesicDilate3D(imIn, imMask, imOut, n=1, se=m3D.CUBOCTAHEDRON):
    """
    Performs a upper geodesic dilation of 3D image 'imIn' above 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the dilation.
    'se' specifies the type of structuring element used to perform the 
    computation (CUBOCTAHEDRON by default). 
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    m3D.logic3D(imIn, imMask, imOut, "sup")
    if imIn.getDepth() == 1:
        for i in range(n):
            m3D.diff3D(imOut, imMask, imOut)
            m3D.dilate3D(imOut, imOut, se=se)
            m3D.logic3D(imMask, imOut, imOut, "sup")
    else:
        imWrk1 = m3D.image3DMb(imIn)
        imWrk2 = m3D.image3DMb(imIn, 1)
        for i in range(n):
            m3D.generateSupMask3D(imOut, imMask, imWrk2, True)
            m3D.convertByMask3D(imWrk2, imWrk1, 0, m3D.computeMaxRange3D(imWrk1)[1])
            m3D.logic3D(imOut, imWrk1, imOut, "inf")
            m3D.dilate3D(imOut, imOut, se=se)
            m3D.logic3D(imOut, imMask, imOut, "sup")

def lowerGeodesicDilate3D(imIn, imMask, imOut, n=1, se=m3D.CUBOCTAHEDRON):
    """
    Performs a lower geodesic dilation of 3D image 'imIn' below 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the dilation.
    'se' specifies the type of structuring element used to perform the 
    computation (CUBOCTAHEDRON by default). 
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    m3D.logic3D(imIn, imMask, imOut, "inf")
    for i in range(n):
        m3D.dilate3D(imOut, imOut, se=se)
        m3D.logic3D(imMask, imOut, imOut, "inf")

def geodesicDilate3D(imIn, imMask, imOut, n=1, se=m3D.CUBOCTAHEDRON):
    """
    This operator is simply an alias of lowerGeodesicDilate3D. It is kept for
    compatibility reasons.
    """
    
    lowerGeodesicDilate3D(imIn, imMask, imOut, n, se=se)
    
        
def upperGeodesicErode3D(imIn, imMask, imOut, n=1, se=m3D.CUBOCTAHEDRON):
    """
    Performs a upper geodesic erosion of 3D image 'imIn' above 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the erosion.
    'se' specifies the type of structuring element used to perform the 
    computation (CUBOCTAHEDRON by default).
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    m3D.logic3D(imIn, imMask, imOut, "sup")
    for i in range(n):
        m3D.erode3D(imOut, imOut, se=se)
        m3D.logic3D(imOut, imMask, imOut, "sup")

def lowerGeodesicErode3D(imIn, imMask, imOut, n=1, se=m3D.CUBOCTAHEDRON):
    """
    Performs a lower geodesic erosion of 3D image 'imIn' under 'imMask'.
    The result is put inside 'imOut', 'n' controls the size of the erosion.
    'se' specifies the type of structuring element used to perform the 
    computation (CUBOCTAHEDRON by default).

    The binary lower geodesic erosion is realised using the fact that the
    dilation is the dual operation of the erosion.
    
    Warning! 'imMask' and 'imOut' must be different.
    """
    
    if imIn.getDepth() == 1:
        m3D.diff3D(imMask, imIn, imOut)
        lowerGeodesicDilate3D(imOut, imMask, imOut, n, se=se)
        m3D.diff3D(imMask, imOut, imOut)
    else:
        imWrk1 = m3D.image3DMb(imIn)
        imWrk2 = m3D.image3DMb(imIn, 1)
        m3D.logic3D(imIn, imMask, imOut, "inf")
        for i in range(n):
            m3D.generateSupMask3D(imOut, imMask, imWrk2, False)
            m3D.convertByMask3D(imWrk2, imWrk1, 0, m3D.computeMaxRange3D(imWrk1)[1])
            m3D.logic3D(imOut, imWrk1, imOut, "sup")
            m3D.erode3D(imOut, imOut, se=se)
            m3D.logic3D(imOut, imMask, imOut, "inf")
 
def geodesicErode3D(imIn, imMask, imOut, n=1, se=m3D.CUBOCTAHEDRON):
    """
    This transformation is identical to the previous version and it has been
    kept for compatibilty purposes.
    
    Note that the binary and the greytone operators are different.
    """
    
    if imIn.getDepth() == 1:
        lowerGeodesicErode3D(imIn, imMask, imOut, n, se=se)
    else:
        upperGeodesicErode3D(imIn, imMask, imOut, n, se=se)

def build3D(imMask, imInout, grid=m3D.DEFAULT_GRID3D):
    """
    Builds 3D image 'imInout' using 'imMask' as a mask. This operator performs
    the geodesic reconstruction of 'imInout' inside the mask image and puts the
    result in the same image.
    
    This operator uses a hierarchical implementation of the reconstruction.
    
    This function will use the mamba3D default grid unless specified otherwise
    in 'grid'. It works only with grids FACE_CENTER_CUBIC and CUBIC.
    """
    
    if imInout.getDepth()==1:
        _build3D_1(imMask, imInout, grid)
    else:
        err = core.MB3D_HierarBld(imMask.mb3DIm, imInout.mb3DIm, grid.getCValue())
        mamba.raiseExceptionOnError(err)

def dualBuild3D(imMask, imInout, grid=m3D.DEFAULT_GRID3D):
    """
    Builds (dual build) 3D image 'imInout' using 'imMask' as a mask.
    This operator performs the geodesic dual reconstruction (by erosions)
    of 'imInout' inside the mask image and puts the result in the same image.
    
    This operator uses a hierarchical implementation of the reconstruction.
    
    This function will use the mamba3D default grid unless specified otherwise
    in 'grid'. It works only with grids FACE_CENTER_CUBIC and CUBIC.
    """
    
    if imInout.getDepth()==1:
        _dualBuild3D_1(imMask, imInout, grid)
    else:
        err = core.MB3D_HierarDualBld(imMask.mb3DIm, imInout.mb3DIm, grid.getCValue())
        mamba.raiseExceptionOnError(err)

def minima3D(imIn, imOut, h=1, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the minima of 'imIn' using a dual build operation and puts the 
    result in 'imOut'.
    
    'h' can be used to define the minima depth. Grid used by the dual build 
    operation can be specified by 'grid'.
    
    Only works with greyscale images as input. 'imOut' must be binary.
    """
    if imIn.getDepth()!=8:
        mamba.raiseExceptionOnError(core.ERR_BAD_DEPTH)
    
    imWrk = m3D.image3DMb(imIn)
    m3D.addConst3D(imIn, h, imWrk)
    dualBuild3D(imIn, imWrk, grid=grid)
    m3D.sub3D(imWrk, imIn, imWrk)
    m3D.threshold3D(imWrk, imOut, 1, mamba.computeMaxRange(imIn[0])[1])

def maxima3D(imIn, imOut, h=1, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the maxima of 'imIn' using a build operation and puts the result in
    'imOut'.
    
    'h' can be used to define the maxima height. Grid used by the build operation 
    can be specified by 'grid'.
    
    Only works with greyscale images as input. 'imOut' must be binary.
    """
    if imIn.getDepth()!=8:
        mamba.raiseExceptionOnError(core.ERR_BAD_DEPTH)
    
    imWrk = m3D.image3DMb(imIn)
    m3D.subConst3D(imIn, h, imWrk)
    build3D(imIn, imWrk, grid=grid)
    m3D.sub3D(imIn, imWrk, imWrk)
    m3D.threshold3D(imWrk, imOut, 1, mamba.computeMaxRange(imIn[0])[1])

def closeHoles3D(imIn, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Close holes in 3D image 'imIn' and puts the result in 'imOut'. This
    operator works on binary and greytone images. In this case, however,
    it should be used cautiously.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.negate3D(imIn, imIn)
    m3D.drawEdge3D(imWrk)
    m3D.logic3D(imIn, imWrk, imWrk, "inf")
    build3D(imIn, imWrk, grid=grid)
    m3D.negate3D(imIn, imIn)
    m3D.negate3D(imWrk, imOut)

def removeEdgeParticles3D(imIn, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Removes particles (connected components) touching the edge in 3D image
    'imIn'. The resulting image is put in image 'imOut'.
    Although this operator may be used with greytone images, it should be
    considered with caution.
    """
    
    imWrk = m3D.image3DMb(imIn)
    se = m3D.structuringElement3D(m3D.getDirections3D(grid), grid)
    m3D.dilate3D(imWrk, imWrk, se=se, edge=mamba.FILLED)
    m3D.logic3D(imIn, imWrk, imWrk, "inf")
    build3D(imIn, imWrk, grid=grid)
    m3D.diff3D(imIn, imWrk, imOut)
