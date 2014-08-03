"""
Statistical operators.

This module provides a set of functions to compute statistical values such
as mean and median inside an image.
"""

# contributor: Nicolas BEUCHER

import mamba
import mamba.core as core

def getHistogram(imIn):
    """
    Returns a list holding the histogram of the greyscale image 'imIn' (0 to 255).
    """
    histo = 256*[0]
    err, histo = core.MB_Histo(imIn.mbIm,histo)
    mamba.raiseExceptionOnError(err)
    return histo

def getMean(imIn):
    """
    Returns the average value (float) of the pixels of 'imIn' (which must be a
    greyscale image).
    """
    
    histo = mamba.getHistogram(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t + i*v
    return float(t)/float(s)

def getMedian(imIn):
    """
    Returns the median value of the pixels of 'imIn'.

    The median value is defined as the first pixel value for which at least
    half of the pixels are below it. 
    
    'imIn' must be a greyscale image.
    """
    
    histo = mamba.getHistogram(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t+v
        if t>s//2:
            break
    return i

def getVariance(imIn):
    """
    Returns the pixels variance (estimator without bias) of image 'imIn' (which 
    must be a greyscale image)..
    """
    
    mean = getMean(imIn)
    histo = mamba.getHistogram(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t+v*(i-mean)*(i-mean)
    return t/(s-1)
