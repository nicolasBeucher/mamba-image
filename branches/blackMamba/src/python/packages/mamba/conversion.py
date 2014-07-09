"""
This module regroups various functions/operators to perform conversion
based on image depth.
"""

import mamba
import mamba.core as core

# Conversion and similar operators #############################################

def convert(imIn, imOut):
    """
    Converts the contents of 'imIn' to the depth of 'imOut' and puts the result
    in 'imOut'.
    
    Only greyscale to binary and binary to greyscale conversion are supported.
    Value 255 is in a greyscale image is considered as 1 in a binary one. All other
    values are transformed to 0. The reverse convention applies.
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

