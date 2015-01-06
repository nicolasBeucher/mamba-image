"""
Erosion and dilation 3D operators for large structuring elements.

This module provides a set of functions and class to perform erosions and
dilations with large structuring elements.
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
    
def fastShift3D_old(imIn, imOut, d, amp, fill, grid=m3D.DEFAULT_GRID3D):
    """
    Shifts 3D image 'imIn' in direction 'd' of the 'grid' over an amplitude of
    'amp'. The emptied space is filled with 'fill' value.
    This implementation is faster than the previous one.
    The result is put in 'imOut'.
    """
    
    (width,height,length) = imIn.getSize()
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    # Cubic grid case (the simplest one).
    if grid.getCValue() == m3D.CUBIC.getCValue():
        # The above statement is an (ugly) way to get the grid in use.
        if d < 9:
            # Horizontal shift.
            for i in range(length):
                mamba.shift( imIn[i], imOut[i], d, amp, fill, grid=mamba.SQUARE)
            start = 0
            end = 0
        elif d < 18:
            # Downwards shift.
            hd = d - 9
            for i in range(amp, length):
                j = i - amp
                mamba.shift( imIn[i], imOut[j], hd, amp, fill, grid=mamba.SQUARE)
            start = max(length - amp, 0)
            end = length
        elif d < 27:
            # Upwards shift.
            hd = d - 18
            for i in range(length - amp - 1, -1, -1):
                j = i + amp
                mamba.shift( imIn[i], imOut[j], hd, amp, fill, grid=mamba.SQUARE)
            start = 0
            end = min(amp, length)
        else:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
    # Centered cubic grid.
    elif grid.getCValue() == m3D.CENTER_CUBIC.getCValue():
        if d < 9:
            # Horizontal shift.
            for i in range(length):
                mamba.shift( imIn[i], imOut[i], d, amp, fill, grid=mamba.SQUARE)
            start = 0
            end = 0
        elif d < 13:
            # Downwards shift.
            hd1 = m3D.CENTER_CUBIC.convertFromDir(d, 0)[1]
            hd2 = m3D.CENTER_CUBIC.convertFromDir(d, 1)[1]
            for i in range(amp, length):
                j = i - amp
                amp1 = amp//2
                amp2 = amp//2
                if amp%2 == 1:
                    if i%2 == 0:
                        amp1 = amp1 + 1
                    else:
                        amp2 = amp2 + 1
                mamba.shift( imIn[i], imOut[j], hd1, amp1, fill, grid=mamba.SQUARE)
                mamba.shift(imOut[j], imOut[j], hd2, amp2, fill, grid=mamba.SQUARE) 
            start = max(length - amp, 0)
            end = length
        elif d < 17:
            # Upwards shift.
            hd1 = m3D.CENTER_CUBIC.convertFromDir(d, 0)[1]
            hd2 = m3D.CENTER_CUBIC.convertFromDir(d, 1)[1]
            for i in range(length - amp - 1, -1, -1):
                j = i + amp
                amp1 = amp//2
                amp2 = amp//2
                if amp%2 == 1:
                    if i%2 == 0:
                        amp1 = amp1 + 1
                    else:
                        amp2 = amp2 + 1
                mamba.shift( imIn[i], imOut[j], hd1, amp1, fill, grid=mamba.SQUARE)
                mamba.shift(imOut[j], imOut[j], hd2, amp2, fill, grid=mamba.SQUARE)                 
            start = 0
            end = min(amp, length)
        else:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
    # Face centered cubic grid.
    else:
        if d < 7:
            # Horizontal shift.
            for i in range(length):
                mamba.shift(imIn[i], imOut[i], d, amp, fill, grid=mamba.HEXAGONAL)
            start = 0
            end = 0
        elif d < 9:
            # Downwards shift.
            extraS = (((0,0,0),(1,0,0),(1,0,1)),((0,0,0),(0,1,0),(1,1,0)),((0,0,0),(0,0,1),(0,1,1)))
            hdList = [m3D.FACE_CENTER_CUBIC.convertFromDir(d, i)[1] for i in range(3)]
            dirUse = [0, 1, 2]
            v = hdList.index(0)
            del dirUse[v]
            for i in range(amp, length):
                j = i - amp
                amp1 = amp//3 + extraS[i%3][amp%3][dirUse[0]]
                mamba.shift( imIn[i], imOut[j], hdList[dirUse[0]], amp1, fill, grid=mamba.HEXAGONAL)
                amp1 = amp//3 + extraS[i%3][amp%3][dirUse[1]]
                mamba.shift(imOut[j], imOut[j], hdList[dirUse[1]], amp1, fill, grid=mamba.HEXAGONAL) 
            start = max(length - amp, 0)
            end = length
        elif d == 9:
            # Specific algorithm is setup for direction 9 to avoid edge effects.
            extraS = (((0,0),(0,1),(1,0)),((0,0),(0,0),(0,1)),((0,0),(0,1),(0,1)))
            for i in range(amp, length):
                j = i - amp
                (sc, sh) = extraS[i%3][amp%3]
                nc = (amp//3 +sc) * 2
                mamba.shift( imIn[i], imOut[j], 1, nc, fill, grid=mamba.SQUARE)
                if sh <> 0:
                    if (i%3) == 2:
                        hd = 1
                    else:
                        hd = 6
                    mamba.shift(imOut[j], imOut[j], hd, 1, fill, grid=mamba.HEXAGONAL) 
            start = length - amp
            end = length            
        elif d < 12:
            # Upwards shift.
            extraS = (((0,0,0),(1,0,0),(1,1,0)),((0,0,0),(0,1,0),(0,1,1)),((0,0,0),(0,0,1),(1,0,1)))
            hdList = [m3D.FACE_CENTER_CUBIC.convertFromDir(d, i)[1] for i in range(3)]
            dirUse = [0, 1, 2]
            v = hdList.index(0)
            del dirUse[v]
            for i in range(length - amp - 1, -1, -1):
                j = i + amp
                amp1 = amp//3 + extraS[i%3][amp%3][dirUse[0]]
                mamba.shift( imIn[i], imOut[j], hdList[dirUse[0]], amp1, fill, grid=mamba.HEXAGONAL)
                amp1 = amp//3 + extraS[i%3][amp%3][dirUse[1]]
                mamba.shift(imOut[j], imOut[j], hdList[dirUse[1]], amp1, fill, grid=mamba.HEXAGONAL) 
            start = 0
            end = min(amp, length)
        elif d == 12:
            # Specific algorithm for direction 12.
            extraS = (((0,0),(0,0),(0,1)),((0,0),(0,1),(1,0)),((0,0),(0,1),(0,1)))
            for i in range(length - amp - 1, -1, -1):
                j = i + amp
                (sc, sh) = extraS[i%3][amp%3]
                nc = (amp//3 +sc) * 2
                mamba.shift( imIn[i], imOut[j], 1, nc, fill, grid=mamba.SQUARE)
                if sh <> 0:
                    if (i%3) == 2:
                        hd = 3
                    else:
                        hd = 4
                    mamba.shift(imOut[j], imOut[j], hd, 1, fill, grid=mamba.HEXAGONAL) 
            start = 0
            end = min(amp, length)
        else:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
    for i in range(start, end):
        imOut[i].fill(fill)
 
def fastShift3D(imIn, imOut, d, amp, fill, grid=m3D.DEFAULT_GRID3D):
    """
    Shifts 3D image 'imIn' in direction 'd' of the 'grid' over an amplitude of
    'amp'. The emptied space is filled with 'fill' value.
    This implementation is fast as a minimal number of shifts is used.
    The result is put in 'imOut'.
    """
    
    (width,height,length) = imIn.getSize()
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    # Computing limits according to the scanning direction.
    scan = grid.convertFromDir(d,0)[0]
    if scan == 0:
        startPlane, ehdPlane, scanDir = 0, length, 1
        startFill, endFill = 0, 0
    elif scan == -1:
        startPlane, endPlane, scanDir = amp, length, 1
        startFill, endFill = max(length - amp, 0), length
    else:
        startPlane, endPlane, scanDir = length - amp - 1, -1, -1
        startFill, endFill = 0, min(amp, length)    
    # Performing the shift operations given by the getShiftDirList method.
    for i in range(startPlane, endPlane, scanDir):
        j = i + amp * scan
        dirList = grid.getShiftDirsList(d, amp, i)
        mamba.shift(imIn[i], imOut[j], dirList[0][0] , dirList[0][1], fill, grid=dirList[0][2])
        if len(dirList) > 1:
            mamba.shift(imOut[j], imOut[j], dirList[1][0] , dirList[1][1], fill, grid=dirList[1][2])       
    # Filling the necessary planes.
    for i in range(startFill, endFill):
        imOut[i].fill(fill)
              
def supFarNeighbor3D(imIn, imInOut, nb, amp, grid=m3D.DEFAULT_GRID3D, edge=mamba.EMPTY):
    """
    Performs a supremum operation between the 'imInOut' 3D image pixels and their neighbor 'nb'
    at distance 'amp' according to 'grid' in 3D image 'imIn'. The result is put in 'imInOut'.
    "grid' value can be CUBIC, CENTER_CUBIC or FACE_CENTER_CUBIC. 'edge' value can be EMPTY
    or FILLED.
    """
    
    (width,height,length) = imIn.getSize()
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    imWrk = mamba.imageMb(imIn[0])
    # Computing limits according to the scanning direction.
    scan = grid.convertFromDir(nb,0)[0]
    if scan == 0:
        startPlane, ehdPlane, scanDir = 0, length, 1
        startFill, endFill = 0, 0
    elif scan == 1:
        startPlane, endPlane, scanDir = 0, length - amp, 1
        startFill, endFill = max(length - amp, 0), length
    else:
        startPlane, endPlane, scanDir = length - 1, amp, -1
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
            mamba.farSupNeighbor(imIn[j], imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)
        else:
            d = dirList[1][2].getTranDir(dirList[1][0])
            mamba.shift(imIn[j], imWrk, d, dirList[1][1], fillValue, grid=dirList[1][2])
            mamba.farSupNeighbor(imWrk, imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)            
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
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    imWrk = mamba.imageMb(imIn[0])
    # Computing limits according to the scanning direction.
    scan = grid.convertFromDir(nb,0)[0]
    if scan == 0:
        startPlane, ehdPlane, scanDir = 0, length, 1
        startFill, endFill = 0, 0
    elif scan == 1:
        startPlane, endPlane, scanDir = 0, length - amp, 1
        startFill, endFill = max(length - amp, 0), length
    else:
        startPlane, endPlane, scanDir = length - 1, amp, -1
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
            mamba.farInfNeighbor(imIn[j], imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)
        else:
            d = dirList[1][2].getTranDir(dirList[1][0])
            mamba.shift(imIn[j], imWrk, d, dirList[1][1], fillValue, grid=dirList[1][2])
            mamba.farInfNeighbor(imWrk, imInOut[i], dirList[0][0] , dirList[0][1], grid=dirList[0][2], edge=edge)            
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
 
 
 
