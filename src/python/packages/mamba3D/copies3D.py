"""
Copy 3D operators.

This module regroups various complete or partial copy operators for 3D images.
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
    nbPlanes = min(len(imOut)-firstPlaneOut, len(imIn)-firstPlaneIn)
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
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
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
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.copyBytePlane(imIn[i], plane, imOut[i])

def cropCopy3D(imIn, posin, imOut, posout, size):
    """
    Crops a cube of size 'size' at position 'posin' in image 'imIn' and
    inserts it in image 'imOut' at position 'posout'.
    'posin', 'posout' and 'size' are tuples containing width, height and length
    values.
    This operator is similar to the 2D cropCopy operator. It shares the
    same restrictions.
    """
	
    if (len(imIn) <= posin[2]) or (len(imOut) <= posout[2]):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_VALUE)
	
    nbPlanes = min(size[2], len(imIn) - posin[2], len(imOut) - posout[2])
    for i in range(nbPlanes):
        mamba.cropCopy(imIn[posin[2] + i], posin[0:2], imOut[posout[2] + i], posout[0:2], size[0:2])
	
	
	
	
