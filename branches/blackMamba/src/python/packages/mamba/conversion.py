"""
Depth conversion operators.

This module regroups various functions/operators to perform conversions
based on image depth. It allows to transfer data from an image depth to another.
"""

import mamba
import mamba.core as core

# Conversion and similar operators #############################################

def convert(imIn, imOut):
    """
    Converts the contents of 'imIn' to the depth of 'imOut' and puts the result
    in 'imOut'.

    For greyscale/32-bit to binary conversion, value 255/0xffffffff in 'imIn'
    is converted to 1 in 'imOut'. All other values are transformed to 0.
    The reverse convention applies to binary to greyscale/32-bit conversion.

    32-bit images are downscaled into greyscale images. Conversion from 8-bit
    to 32-bit is equivalent to copyBytePlane for plane 0.

    When both images have the same depth this function is a simple copy.
    """
    err = core.MB_Convert(imIn.mbIm, imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def convertByMask(imIn, imOut, mFalse, mTrue):
    """
    Converts a binary image 'imIn' into a greyscale image (8-bit) or a 32-bit 
    image and puts the result in 'imOut'.
    
    white pixels of 'imIn' are set to value 'mTrue' in the output image and the 
    black pixels set to value 'mFalse'.
    """
    err = core.MB_Mask(imIn.mbIm, imOut.mbIm, mFalse, mTrue)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def threshold(imIn, imOut, low, high):
    """
    Performs a threshold operation over image 'imIn'.
    The result is put in binary image 'imOut'.
    
    All the pixels that have a strictly lower value than 'low' or 
    strictly higher than 'high' are set to false.
    Otherwise they are set to true.
    
    'imIn' can be a 8-bit or 32-bit image.
    """
    err = core.MB_Thresh(imIn.mbIm, imOut.mbIm, low, high)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def generateSupMask(imIn1, imIn2, imOut, strict):
    """
    Generates a binary mask image in 'imOut' where pixels are set to 1 when they
    are greater (strictly if 'strict' is set to True, greater or equal otherwise)
    in image 'imIn1' than in image 'imIn2'.
    
    'imIn1' and imIn2' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    err = core.MB_SupMask(imIn1.mbIm, imIn2.mbIm,imOut.mbIm, int(strict))
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def lookup(imIn, imOut, lutable):
    """
    Converts the greyscale image 'imIn' using the look-up table 'lutable'
    and puts the result in greyscale image 'imOut'.
    
    'lutable' is a list containing 256 values with the first one corresponding 
    to 0 and the last one to 255.
    """
    err = core.MB_Lookup(imIn.mbIm,imOut.mbIm,lutable)
    mamba.raiseExceptionOnError(err)
    imOut.update()

