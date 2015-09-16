"""
Copy operators.

This module regroups various complete or partial copy operators.
"""

# Contributors: Serge BEUCHER, Nicolas BEUCHER

import mamba
import mamba.core as core

# Copy operators ###############################################################

def copy(imIn, imOut):
    """
    Copies 'imIn' image into 'imOut' image. 
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images.
    The images must have the same depth and size.
    """
    err = core.MB_Copy(imIn.mbIm, imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()

def copyLine(imIn, nIn, imOut, nOut):
    """
    Copies the line numbered 'nIn' of image 'imIn' into 'imOut' at line 
    index 'nOut'.
    
    'imIn' and 'imOut' can be 1-bit, 8-bit or 32-bit images.
    The images must have the same depth and size.
    """
    err = core.MB_CopyLine(imIn.mbIm, imOut.mbIm, nIn, nOut)
    mamba.raiseExceptionOnError(err)
    imOut.update()

def cropCopy(imIn, posIn, imOut, posOut, size):
    """
    Copies the pixels of 'imIn' in 'imOut' starting from position 'posIn' (tuple 
    x,y) in 'imIn' to position 'posOut' in 'imOut'. The size of the copy in 
    controlled by 'size' (tuple w,h). The actual size will be computed
    so as not to exceed the images border.

    The images must be of the same depth but can have different sizes. Only non
    binary images are accepted (8-bit or 32-bit).
    """
    err = core.MB_CropCopy(imIn.mbIm, posIn[0], posIn[1],
                           imOut.mbIm, posOut[0], posOut[1],
                           size[0], size[1])
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def copyBitPlane(imIn, plane, imOut):
    """
    Inserts or extracts a bit plane.
    If 'imIn' is a binary image, it is inserted at 'plane' position in 
    greyscale or 32-bit image 'imOut'.
    If 'imIn' is a greyscale or 32-bit image, its bit plane at 'plane' position is 
    extracted and put into binary image 'imOut'.
    
    Plane values are from 0 (LSB) to 7 (MSB) for 8-bit images or from 0 (LSB) to
    31 (MSB) for 32-bit images.
    """ 
    err = core.MB_CopyBitPlane(imIn.mbIm,imOut.mbIm, plane)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def copyBytePlane(imIn, plane, imOut):
    """
    Inserts or extracts a byte plane.
    If 'imIn' is a greyscale image, it is inserted at 'plane' position in 
    32-bit 'imOut'.
    If 'imIn' is a 32-bit image, its byte plane at 'plane' position is 
    extracted and put into 'imOut'.
    
    Plane values are from 0 (LSByte) to 3 (MSByte).
    """
    err = core.MB_CopyBytePlane(imIn.mbIm,imOut.mbIm, plane)
    mamba.raiseExceptionOnError(err)
    imOut.update()

