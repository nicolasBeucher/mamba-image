"""
Segmentation operators.

This module provides a set of functions to perform segmentation
operations (such as watershed and basin). The module also contains the
labelling operator.
"""

# Contributors: Nicolas BEUCHER, Serge BEUCHER

import mamba
import mamba.core as core

def label(imIn, imOut, lblow=0, lbhigh=256, grid=mamba.DEFAULT_GRID):
    """
    Labels the image 'imIn' and puts the result in 32-bit image 'imOut'.
    Returns the number of connected components found by the labelling algorithm.
    The labelling will be performed according to the 'grid' (HEXAGONAL is 
    6-Neighbors and SQUARE is 8-Neighbors).
    
    'lblow' and 'lbhigh' are used to restrain the possible values in the
    lower byte of 'imOut' pixel values. these values (and all their multiples of 
    256) are then reserved for another use (see Mamba User Manual for further details).
    """

    err, nbobj = core.MB_Label(imIn.mbIm,imOut.mbIm, lblow, lbhigh, grid.id)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    return nbobj
    
def watershedSegment(imIn, imMarker, grid=mamba.DEFAULT_GRID, max_level=0):
    """
    Segments image 'imIn' (greyscale or 32-bit) using the watershed algorithm.
    'imMarker' is used both as the marker image (the wells from which the
    flooding proceeds) and as the output image. It is a 32-bit image.
    'max_level' can be used to limit the flooding process to a specific level
    (useful if you want to survey the flooding level by level). A zero value
    will make the flooding run to its completion.
    
    'grid' will change the number of neighbors considered by the algorithm 
    (HEXAGONAL is 6-Neighbors and SQUARE is 8-Neighbors).
    
    The result is put inside 'imMarker'. The three first byte planes contain
    the actual segmentation (each region has a specific label according to the
    original marker). The last plane represents the actual watershed line
    (pixels set to 255).
    """
    
    err = core.MB_Watershed(imIn.mbIm, imMarker.mbIm, max_level, grid.id)
    mamba.raiseExceptionOnError(err)
    imMarker.update()
    
def basinSegment(imIn, imMarker, grid=mamba.DEFAULT_GRID, max_level=0):
    """
    Segments image 'imIn' (greyscale or 32-bit) using the watershed algorithm.
    'imMarker' is used both as the marker image (the wells from which the
    flooding proceeds) and as the output image. It is a 32-bit image. 
    'max_level' can be used to  limit the flooding process to a specific level
    (useful if you want to survey the flooding level by level). A zero value
    will make the flooding run to its completion.
    
    'grid' will change the number of neighbors considered by the algorithm 
    (HEXAGONAL is 6-Neighbors and SQUARE is 8-Neighbors).
    
    The result is put inside 'imMarker'. The three first byte planes contain
    the actual segmentation (each segment has a specific label according to the
    original marker). This function only returns catchment basins (no watershed 
    line) and is faster than watershedSegment if you are not interested in the 
    watershed line.
    """
    
    err = core.MB_Basins(imIn.mbIm, imMarker.mbIm, max_level, grid.id)
    mamba.raiseExceptionOnError(err)
    imMarker.update()

def markerControlledWatershed(imIn, imMarkers, imOut, grid=mamba.DEFAULT_GRID):
    """
    Marker-controlled watershed transform of greytone image 'imIn'. The binary
    image 'imMarkers' contains the markers which control the flooding process.
    'imOut' contains the valued watershed.
    """
    
    im_mark = mamba.imageMb(imIn, 32)
    imWrk = mamba.imageMb(imIn)
    label(imMarkers, im_mark, grid=grid)
    watershedSegment(imIn, im_mark, grid=grid)
    mamba.copyBytePlane(im_mark, 3, imWrk)
    mamba.logic(imWrk, imIn, imOut, 'inf')

def valuedWatershed(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Returns the valued watershed of greyscale image 'imIn' into greyscale image
    'imOut'. Each pixel of the watershed lines is given its corresponding value
    in initial image 'imIn'.
    """
    
    im_min = mamba.imageMb(imIn, 1)
    mamba.minima(imIn, im_min, grid=grid)
    markerControlledWatershed(imIn, im_min, imOut, grid=grid)

def fastSKIZ(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Fast skeleton by zones of influence of binary image 'imIn'. Result is put in
    binary image 'imOut'. The transformation is faster as it uses the watershed
    transform by hierarchical queues.
    """
    
    imWrk = mamba.imageMb(imIn, 8)
    mamba.convertByMask(imIn, imWrk, 1, 0)
    markerControlledWatershed(imWrk, imIn, imWrk, grid=grid)
    mamba.threshold(imWrk, imOut, 0, 0)

def geodesicSKIZ(imIn, imMask, imOut, grid=mamba.DEFAULT_GRID):
    """
    Geodesic skeleton by zones of influence of binary image 'imIn' inside the
    geodesic mask 'imMask'. The result is in binary image 'imOut'.
    """
    
    imWrk1 = mamba.imageMb(imIn, 8)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk2)
    mamba.build(imMask, imWrk2, grid=grid)
    mamba.convertByMask(imWrk2, imWrk1, 2, 1)
    mamba.sub(imWrk1, imIn, imWrk1)
    markerControlledWatershed(imWrk1, imIn, imWrk1, grid=grid)
    mamba.threshold(imWrk1, imOut, 0, 0)
    mamba.logic(imOut, imWrk2, imOut, "inf")
    
def mosaic(imIn, imOut, imWts, grid=mamba.DEFAULT_GRID):
    """
    Builds the mosaic image of 'imIn' and puts the results into 'imOut'.
    The watershed line (pixel values set to 255) is stored in the 
    greytone image 'imWts'. A mosaic image is a simple image made of various 
    tiles of uniform grey values. It is built using the watershed of 'imIn' 
    gradient and original markers made of gradient minima which are labelled by
    the maximum value of 'imIn' pixels inside them.
    """
   
    imWrk1 = mamba.imageMb(imIn, 1)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk2)
    im_mark = mamba.imageMb(imIn, 32)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    mamba.gradient(imIn, imOut, se=se)
    mamba.minima(imOut, imWrk1, grid=grid) 
    mamba.add(im_mark, imWrk1, im_mark) 
    imWrk1.convert(8)
    mamba.build(imWrk1, imWrk2, grid=grid)
    mamba.add(im_mark, imWrk2, im_mark)   
    watershedSegment(imOut, im_mark, grid=grid)
    mamba.copyBytePlane(im_mark, 3, imWts)
    mamba.subConst(im_mark, 1, im_mark)
    mamba.copyBytePlane(im_mark, 0, imOut)
    
def mosaicGradient(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Builds the mosaic-gradient image of 'imIn' and puts the result in 'imOut'.
    The mosaic-gradient image is built by computing the differences of two
    mosaic images generated from 'imIn', the first one having its watershed
    lines valued by the suprema of the adjacent catchment basins values, the
    second one been valued by the infima.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn)
    imWrk5 = mamba.imageMb(imIn)
    imWrk6 = mamba.imageMb(imIn, 1)
    mosaic(imIn, imWrk2, imWrk3, grid=grid)
    mamba.sub(imWrk2, imWrk3, imWrk1)
    mamba.logic(imWrk2, imWrk3, imWrk2, "sup")
    mamba.negate(imWrk2, imWrk2)
    mamba.threshold(imWrk3, imWrk6, 1, 255)
    mamba.multiplePoints(imWrk6, imWrk6, grid=grid)
    mamba.convertByMask(imWrk6, imWrk3, 0, 255)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    mamba.dilate(imWrk1, imWrk4, se=se)
    mamba.dilate(imWrk2, imWrk5, se=se)
    while mamba.computeVolume(imWrk3) != 0:
        mamba.dilate(imWrk1, imWrk1, 2, se=se)
        mamba.dilate(imWrk2, imWrk2, 2, se=se)
        mamba.logic(imWrk1, imWrk3, imWrk1, "inf")
        mamba.logic(imWrk2, imWrk3, imWrk2, "inf")
        mamba.logic(imWrk1, imWrk4, imWrk4, "sup")
        mamba.logic(imWrk2, imWrk5, imWrk5, "sup")
        mamba.erode(imWrk3, imWrk3, 2, se=se)
    mamba.negate(imWrk5, imWrk5)
    mamba.sub(imWrk4, imWrk5, imOut)

