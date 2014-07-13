"""
This module regroups copy functions/operators on 3D images.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

# Copy operators ###############################################################

def copy3D(imIn, imOut, firstPlaneIn=0, firstPlaneOut=0):
    """
    Copies 3D image 'imIn' into 'imOut'. 'firstPlaneIn' indicates the starting
    plane inside 'imIn' and 'firstPlaneOut' the starting plane inside 'imOut'.
    """
    nbPlanes = min(imOut.getLength()-firstPlaneOut, imIn.getLength()-firstPlaneIn)
    for i in range(nbPlanes):
        mamba.copy(imIn[i+firstPlaneIn], imOut[i+firstPlaneOut])

def copyBitPlane3D(imIn, plane, imOut):
    """
    Inserts or extracts a bit plane in a 3D image.
    If 'imIn' is a binary image, it is inserted at 'plane' position in 
    greyscale 'imOut'.
    If 'imIn' is a greyscale image, its bit plane at 'plane' position is 
    extracted and put into binary image 'imOut'.
    
    Plane values are 0 (LSB) to 7 (MSB).
    """
    outl = imOut.getLength()
    inl = imIn.getLength()
    if inl!=outl:
        mamba.raiseExceptionOnError(core.ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.copyBitPlane(imIn[i], plane, imOut[i])

def copyBytePlane3D(imIn, plane, imOut):
    """
    Inserts or extracts a byte plane in a 3D image.
    If 'imIn' is a greyscale image, it is inserted at 'plane' position in 
    32-bit 'imOut'.
    If 'imIn' is a 32-bit image, its byte plane at 'plane' position is 
    extracted and put into 'imOut'.
    
    Plane values are 0 (LSByte) to 3 (MSByte).
    """
    outl = imOut.getLength()
    inl = imIn.getLength()
    if inl!=outl:
        mamba.raiseExceptionOnError(core.ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.copyBytePlane(imIn[i], plane, imOut[i])

