"""
Various unclassed 3D operators.

This module regroups functions/operators that could not be regrouped with other
operators because of their unique nature or other peculiarity. As such, it
regroups some utility functions.
"""

# Contributors : Nicolas BEUCHER, Serge BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

# Properties operators #########################################################
    
def checkEmptiness3D(imIn):
    """
    Checks if 3D image 'imIn' is empty (i.e. completely black).
    Returns True if so, False otherwise.
    
    'imIn' can be a 1-bit, 8-bit or 32-bit image.
    """
    inl = len(imIn)
    i = 0
    isEmpty = True
    while isEmpty and i<inl:
        isEmpty = mamba.checkEmptiness(imIn[i])
        i += 1
    return isEmpty
    
def compare3D(imIn1, imIn2, imOut):
    """
    Compares the two 3D images 'imIn1' and 'imIn2'.
    The comparison is performed pixelwise by scanning the two images from top left
    to bottom right starting with plane 0 and it stops as soon as a pixel is
    different in the two images.
    The corresponding pixel in 'imOut' is set to the value of the pixel of 
    'imIn1'.
    
    The function returns a tuple holding the position of the first mismatching 
    pixel. The tuple value is (-1,-1,-1) if the two images are identical.
    
    'imOut' is not reset at the beginning of the comparison.
    
    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
        
    z = 0
    x = -1
    y = -1
    while x<0 and z<outl:
        x,y = mamba.compare(imIn1[z], imIn2[z], imOut[z])
        z += 1
    if x<0:
        z = -1
    else:
        z -= 1
    return (x,y,z)

def shift3D(imIn, imOut, d, amp, fill, grid=m3D.DEFAULT_GRID3D):
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
        startPlane, endPlane, scanDir = 0, length, 1
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
 
# Other operators ##############################################################

def drawEdge3D(imOut, thick=1):
    """
    Draws a frame around the edge of 'imOut' whose value equals the maximum
    range value and whose thickness is given by 'thick' (default 1).
    """
    
    imOut.reset()
    se=m3D.structuringElement3D(list(m3D.getDirections3D(m3D.CUBIC)), m3D.CUBIC)
    m3D.dilate3D(imOut, imOut, thick, se=se, edge=mamba.FILLED)

