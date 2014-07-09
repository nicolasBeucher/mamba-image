"""
This module provides a set of functions to compute statistical values inside
a 3D image.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
    
def getMean3D(imIn):
    """
    Returns the average value (float) of the pixels of 'imIn' (which must be a
    greyscale 3D image).
    """
    
    histo = m3D.getHistogram3D(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t + i*v
    return float(t)/float(s)

def getMedian3D(imIn):
    """
    Returns the median value of the pixels of 'imIn'.

    The median value is defined as the first pixel value for which at least
    half of the pixels are below it. 
    
    'imIn' must be a greyscale 3D image.
    """
    
    histo = m3D.getHistogram3D(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t+v
        if t>s//2:
            break
    return i

def getVariance3D(imIn):
    """
    Returns the pixels variance (estimator without bias) of 3D image 'imIn'
    (which must be a greyscale image).
    """
    
    mean = getMean3D(imIn)
    histo = m3D.getHistogram3D(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t+v*(i-mean)*(i-mean)
    return t/(s-1)
