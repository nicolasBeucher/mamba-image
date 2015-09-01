"""
Measure 3D operators.

This module provides a set of functions which perform measure
operations on a 3D image. Measures include volume, range ...
"""

# Contributors : Nicolas BEUCHER

import mamba

def computeVolume3D(imIn):
    """
    Computes the volume of the 3D image 'imIn', i.e. the sum of its pixel
    values. The computed integer value is returned by the function.
    
    'imIn' can be a 1-bit, 8-bit or 32-bit image.
    
    Be aware that because this operator runs on 3D image, the returned value
    can be very high.
    """
    vol = 0
    for im2D in imIn:
        vol += mamba.computeVolume(im2D)
    return vol
    
def computeRange3D(imIn):
    """
    Computes the range, i.e. the minimum and maximum values, of 3D image 'imIn'.
    The values are returned in a tuple holding the minimum and the maximum.
    """
    mav,miv = mamba.computeMaxRange(imIn[0])
    
    for im2D in imIn:
        mi,ma = mamba.computeRange(im2D)
        miv = min(mi,miv)
        mav = max(ma,mav)
    return (miv,mav)
    
def computeMaxRange3D(imIn):
    """
    Returns a tuple with the minimum and maximum possible pixel values given the
    depth of 3D image 'imIn'. The values are returned in a tuple holding the 
    minimum and the maximum.
    """
    return mamba.computeMaxRange(imIn[0])

