"""
Statistical 3D operators.

This module provides a set of functions to compute statistical values such
as mean and median inside a 3D image.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba

def getHistogram3D(imIn):
    """
    Returns a list holding the histogram of the greyscale 3D image 'imIn'
    (0 to 255).
    """
    histo = 256*[0]
    for im2D in imIn:
        hist_im = mamba.getHistogram(im2D)
        for i in range(256):
            histo[i] += hist_im[i]
    return histo

def getMean3D(imIn):
    """
    Returns the average value (float) of the pixels of 'imIn' (which must be a
    greyscale 3D image).
    """
    
    histo = getHistogram3D(imIn)
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
    
    histo = getHistogram3D(imIn)
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
    histo = getHistogram3D(imIn)
    s = sum(histo)
    t = 0
    for i,v in enumerate(histo):
        t = t+v*(i-mean)*(i-mean)
    return t/(s-1)
