"""
Erosion and dilation 3D operators for large structuring elements.

This module provides a set of functions and class to perform erosions and
dilations with large structuring elements on 3D images.
"""

# Contributors : Serge BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

def _sizeSplit(size):
    # This internal function splits the size of the structuring element into a list of
    # successive and decreasing sizes (except the first one). Successive erosions
    # or dilations by double points produce an erosion or dilation by a segment
    # of length 'size'.
   
    sizeList=[]
    incr=1
    while size>incr:
        sizeList.append(incr)
        size=size-incr
        incr=2*incr
    sizeList.append(size)
    sizeList.reverse()
    return sizeList
               
def supFarNeighbor3D(imIn, imInOut, nb, amp, grid=m3D.DEFAULT_GRID3D, edge=mamba.EMPTY):
    """
    Performs a supremum operation between the 'imInOut' 3D image pixels and their neighbor 'nb'
    at distance 'amp' according to 'grid' in 3D image 'imIn'. The result is put in 'imInOut'.
    "grid' value can be CUBIC, CENTER_CUBIC or FACE_CENTER_CUBIC. 'edge' value can be EMPTY
    or FILLED.
    """
    
    (width,height,length) = imIn.getSize()
    if length!=len(imInOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    imWrk = mamba.imageMb(imIn[0])
    # Computing limits according to the scanning direction.
    scan = grid.convertFromDir(nb,0)[0]
    if scan == 0:
        startPlane, endPlane, scanDir = 0, length, 1
        startFill, endFill = 0, 0
    elif scan == 1:
        startPlane, endPlane, scanDir = 0, length - amp, 1
        startFill, endFill = max(length - amp, 0), length
    else:
        startPlane, endPlane, scanDir = length - 1, amp - 1, -1
        startFill, endFill = 0, min(amp, length)    
    # Performing the shift operations given by the getShiftDirList method.
    if edge == mamba.EMPTY:
        fillValue = 0
    else:
        fillValue = mamba.computeMaxRange(imIn[0])[1]
    for i in range(startPlane, endPlane, scanDir):
        j = i + amp * scan
        dirList = grid.getShiftDirsList(nb, amp, i)
        if len(dirList) == 1:
            mamba.supFarNeighbor(imIn[j], imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)
        else:
            d = mamba.transposeDirection(dirList[1][0], dirList[1][2])
            mamba.shift(imIn[j], imWrk, d, dirList[1][1], fillValue, grid=dirList[1][2])
            mamba.supFarNeighbor(imWrk, imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)            
    # Filling the necessary planes.
    if edge == mamba.FILLED:
        for i in range(startFill, endFill):
            imInOut[i].fill(fillValue)
        
def infFarNeighbor3D(imIn, imInOut, nb, amp, grid=m3D.DEFAULT_GRID3D, edge=mamba.FILLED):
    """
    Performs an infimum operation between the 'imInOut' 3D image pixels and their neighbor 'nb'
    at distance 'amp' according to 'grid' in 3D image 'imIn'. The result is put in 'imInOut'.
    "grid' value can be CUBIC, CENTER_CUBIC or FACE_CENTER_CUBIC. 'edge' value can be EMPTY
    or FILLED.
    """
    
    (width,height,length) = imIn.getSize()
    if length!=len(imInOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    imWrk = mamba.imageMb(imIn[0])
    # Computing limits according to the scanning direction.
    scan = grid.convertFromDir(nb,0)[0]
    if scan == 0:
        startPlane, endPlane, scanDir = 0, length, 1
        startFill, endFill = 0, 0
    elif scan == 1:
        startPlane, endPlane, scanDir = 0, length - amp, 1
        startFill, endFill = max(length - amp, 0), length
    else:
        startPlane, endPlane, scanDir = length - 1, amp - 1, -1
        startFill, endFill = 0, min(amp, length)    
    # Performing the shift operations given by the getShiftDirList method.
    if edge == mamba.EMPTY:
        fillValue = 0
    else:
        fillValue = mamba.computeMaxRange(imIn[0])[1]
    for i in range(startPlane, endPlane, scanDir):
        j = i + amp * scan
        dirList = grid.getShiftDirsList(nb, amp, i)
        if len(dirList) == 1:
            mamba.infFarNeighbor(imIn[j], imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)
        else:
            d = mamba.transposeDirection(dirList[1][0], dirList[1][2])
            mamba.shift(imIn[j], imWrk, d, dirList[1][1], fillValue, grid=dirList[1][2])
            mamba.infFarNeighbor(imWrk, imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)            
    # Filling the necessary planes.
    if edge == mamba.EMPTY:
        for i in range(startFill, endFill):
            imInOut[i].fill(fillValue)
          
def largeLinearErode3D(imIn, imOut, dir, size, grid=m3D.DEFAULT_GRID3D, edge=mamba.FILLED):
    """
    Erosion of a 3D image 'imIn' by a large segment in direction 'dir' in a reduced
    number of iterations.
    Uses the erosions by doublets of points (supposed to be faster, thanks to
    an enhanced shift operator).
    """
    
    m3D.copy3D(imIn, imOut)
    for i in _sizeSplit(size):
        infFarNeighbor3D(imOut, imOut, dir, i, grid=grid, edge=edge)

def largeLinearDilate3D(imIn, imOut, dir, size, grid=m3D.DEFAULT_GRID3D, edge=mamba.EMPTY):
    """
    Dilation of the 3D image 'imIn' by a large segment in direction 'dir' in a reduced
    number of iterations.
    Uses the dilations by doublets of points (supposed to be faster, thanks to
    an enhanced shift operator).
    """
    
    m3D.copy3D(imIn, imOut)
    for i in _sizeSplit(size):
        supFarNeighbor3D(imOut, imOut, dir, i, grid=grid, edge=edge)

def largeCubeErode(imIn, imOut, size, edge=mamba.FILLED):
    """
    Erosion by a large cube using erosions by large segments and the Steiner
    decomposition property of the cube.
    No edge effects are likely to happen with a cubic structuring element.
    """
    
    largeLinearErode3D(imIn, imOut, 1, size, grid=m3D.CUBIC, edge=edge)
    largeLinearErode3D(imOut, imOut, 3, size, grid=m3D.CUBIC, edge=edge)
    largeLinearErode3D(imOut, imOut, 5, size, grid=m3D.CUBIC, edge=edge)
    largeLinearErode3D(imOut, imOut, 7, size, grid=m3D.CUBIC, edge=edge)
    largeLinearErode3D(imOut, imOut, 9, size, grid=m3D.CUBIC, edge=edge)
    largeLinearErode3D(imOut, imOut, 18, size, grid=m3D.CUBIC, edge=edge)
    
def largeCubeDilate(imIn, imOut, size, edge=mamba.EMPTY):
    """
    Dilation by a large cube using dilations by large segments and the Steiner
    decomposition property of the cube.
    No edge effects are likely to happen with a cubic structuring element.
    """
    
    largeLinearDilate3D(imIn, imOut, 1, size, grid=m3D.CUBIC, edge=edge)
    largeLinearDilate3D(imOut, imOut, 3, size, grid=m3D.CUBIC, edge=edge)
    largeLinearDilate3D(imOut, imOut, 5, size, grid=m3D.CUBIC, edge=edge)
    largeLinearDilate3D(imOut, imOut, 7, size, grid=m3D.CUBIC, edge=edge)
    largeLinearDilate3D(imOut, imOut, 9, size, grid=m3D.CUBIC, edge=edge)
    largeLinearDilate3D(imOut, imOut, 18, size, grid=m3D.CUBIC, edge=edge)
 
 
 
