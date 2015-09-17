"""
Segmentation 3D operators.

This module provides a set of functions to perform 3D segmentation
operations (such as watershed and basin). The module also contains the
labelling operator.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

def label3D(imIn, imOut, lblow=0, lbhigh=256, grid=m3D.DEFAULT_GRID3D):
    """
    Labels the 3D image 'imIn' and puts the result in 32-bit 3D image
    'imOut'. Returns the number of connected components found by the
    labeling algorithm. The labelling will be performed according to the
    'grid'.
    
    'lblow' and 'lbhigh' are used to restrain the possible values in the
    lower byte of 'imOut' pixel values. these values (and all their multiples of 
    256) are then reserved for another use (see Mamba User Manual for further
    details).
    
    This operator works only with grids FACE_CENTER_CUBIC and CUBIC.
    """

    err, nbobj = core.MB3D_Label(imIn.mb3DIm, imOut.mb3DIm, lblow, lbhigh, grid.getCValue())
    mamba.raiseExceptionOnError(err)
    return nbobj

def watershedSegment3D(imIn, imMarker, grid=m3D.DEFAULT_GRID3D, max_level=0):
    """
    Segments greyscale or 32-bit 3D image 'imIn' using the watershed algorithm.
    'imMarker' is used both as the marker image (the wells from which the
    flooding proceeds) and as the output image. It is a 32-bit 3D image.
    'max_level' can be used to limit the flooding process to a specific
    level (useful if you want to survey the flooding level by level).
    
    'grid' will change the number and position of neighbors considered by
    the algorithm.
    
    The result is put inside 'imMarker'. The three first byte planes contain
    the actual segmentation (each region has a specific label according to the
    original marker). The last plane represents the actual watershed line
    (pixels set to 255).
    
    This operator works only with grids FACE_CENTER_CUBIC and CUBIC.
    """
    
    err = core.MB3D_Watershed(imIn.mb3DIm, imMarker.mb3DIm, max_level, grid.getCValue())
    mamba.raiseExceptionOnError(err)

def basinSegment3D(imIn, imMarker, grid=m3D.DEFAULT_GRID3D, max_level=0):
    """
    Segments 3D image 'imIn' (greyscale or 32-bit) using the watershed algorithm.
    'imMarker' is used both as the marker image (the wells from which the
    flooding proceeds) and as the output image. It is a 32-bit 3D image.
    'max_level' can be used to limit the flooding process to a specific
    level (useful if you want to survey the flooding level by level).
    
    'grid' will change the number and position of neighbors considered by
    the algorithm.
    
    The result is put inside 'imMarker'. The three first byte planes contain
    the actual segmentation (each segment has a specific label according to the
    original marker). This function only return catchment basins (no watershed 
    line) and is faster than watershedSegment3D if you are not interested in the 
    watershed line.
    
    This operator works only with grids FACE_CENTER_CUBIC and CUBIC.
    """
    
    err = core.MB3D_Basins(imIn.mb3DIm, imMarker.mb3DIm, max_level, grid.getCValue())
    mamba.raiseExceptionOnError(err)

def markerControlledWatershed3D(imIn, imMarkers, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Marker-controlled watershed transform of greyscale or 32-bit 3D image 'imIn'.
    The binary 3D image 'imMarkers' contains the markers which control the
    flooding process. 'imOut' contains the valued watershed.
    """
    
    im_mark = m3D.image3DMb(imIn, 32)
    imWrk = m3D.image3DMb(imIn)
    label3D(imMarkers, im_mark, grid=grid)
    watershedSegment3D(imIn, im_mark, grid=grid)
    m3D.copyBytePlane3D(im_mark, 3, imWrk)
    m3D.logic3D(imWrk, imIn, imOut, 'inf')

def valuedWatershed3D(imIn, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Returns the valued watershed of greyscale or 32-bit 3D image 'imIn' into greyscale
    3D image 'imOut'. Each pixel of the watershed lines is given its
    corresponding value in initial image 'imIn'.
    """
    
    im_min = m3D.image3DMb(imIn, 1)
    m3D.minima3D(imIn, im_min, grid=grid)
    markerControlledWatershed3D(imIn, im_min, imOut, grid=grid)

def fastSKIZ3D(imIn, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Fast skeleton by zones of influence of binary 3D image 'imIn'. Result is
    put in binary 3D image 'imOut'. The transformation is faster as it uses
    the watershed transform by hierarchical queues.
    """
    
    imWrk = m3D.image3DMb(imIn, 8)
    m3D.convertByMask3D(imIn, imWrk, 1, 0)
    markerControlledWatershed3D(imWrk, imIn, imWrk, grid=grid)
    m3D.threshold3D(imWrk, imOut, 0, 0)
    
def mosaic3D(imIn, imOut, imWts, grid=m3D.DEFAULT_GRID3D):
    """
    Builds the mosaic 3D image of 'imIn' and puts the results into 'imOut'.
    The watershed line (pixel values set to 255) is stored in the 
    greytone 3D image 'imWts'. A mosaic image is a simple image made of various 
    tiles of uniform grey values. It is built using the watershed of 'imIn' 
    gradient and original markers made of gradient minima which are labelled by
    the maximum value of 'imIn' pixels inside them.
    """
   
    imWrk1 = m3D.image3DMb(imIn, 1)
    imWrk2 = m3D.image3DMb(imIn)
    m3D.copy3D(imIn, imWrk2)
    im_mark = m3D.image3DMb(imIn, 32)
    se = m3D.structuringElement3D(m3D.getDirections3D(grid), grid)
    m3D.gradient3D(imIn, imOut, se=se)
    m3D.minima3D(imOut, imWrk1, grid=grid) 
    m3D.add3D(im_mark, imWrk1, im_mark) 
    imWrk1.convert(8)
    m3D.build3D(imWrk1, imWrk2, grid=grid)
    m3D.add3D(im_mark, imWrk2, im_mark)   
    m3D.watershedSegment3D(imOut, im_mark, grid=grid)
    m3D.copyBytePlane3D(im_mark, 3, imWts)
    m3D.subConst3D(im_mark, 1, im_mark)
    m3D.copyBytePlane3D(im_mark, 0, imOut)
    
def mosaicGradient3D(imIn, imOut, grid=m3D.DEFAULT_GRID3D):
    """
    Builds the mosaic-gradient 3D image of 'imIn' and puts the result in 'imOut'.
    The mosaic-gradient image is built by computing the differences of two
    mosaic images generated from 'imIn', the first one having its watershed
    lines valued by the suprema of the adjacent catchment basins values, the
    second one been valued by the infima.
    """
    
    imWrk1 = m3D.image3DMb(imIn)
    imWrk2 = m3D.image3DMb(imIn)
    imWrk3 = m3D.image3DMb(imIn)
    imWrk4 = m3D.image3DMb(imIn)
    imWrk5 = m3D.image3DMb(imIn)
    mosaic3D(imIn, imWrk2, imWrk3, grid=grid)
    m3D.sub3D(imWrk2, imWrk3, imWrk1)
    m3D.logic3D(imWrk2, imWrk3, imWrk2, "sup")
    m3D.negate3D(imWrk2, imWrk2)
    se = m3D.structuringElement3D(m3D.getDirections3D(grid), grid)
    while m3D.computeVolume3D(imWrk3) != 0:
        m3D.dilate3D(imWrk1, imWrk4, 2, se=se)
        m3D.dilate3D(imWrk2, imWrk5, 2, se=se)
        m3D.logic3D(imWrk4, imWrk3, imWrk4, "inf")
        m3D.logic3D(imWrk5, imWrk3, imWrk5, "inf")
        m3D.logic3D(imWrk1, imWrk4, imWrk1, "sup")
        m3D.logic3D(imWrk2, imWrk5, imWrk2, "sup")
        m3D.erode3D(imWrk3, imWrk3, 2, se=se)
    m3D.negate3D(imWrk2, imWrk2)
    m3D.sub3D(imWrk1, imWrk2, imOut)
