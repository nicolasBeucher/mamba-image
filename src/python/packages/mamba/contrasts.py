"""
Contrast operators.

This module provides a set of functions to perform morphological contrast
operators such as gradient, top-hat transform, ....
"""

import mamba

# Contributors: Serge BEUCHER, Nicolas BEUCHER

def gradient(imIn, imOut, n=1, se=mamba.DEFAULT_SE):
    """
    Computes the morphological gradient of image 'imIn' and puts the result in 
    'imOut'. The thickness can be controlled using parameter 'n' (1 by default).
    The structuring element used by the erosion and dilation is defined by 'se'
    (DEFAULT_SE by default).
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.erode(imIn, imWrk, n, se=se)
    mamba.dilate(imIn, imOut, n, se=se)
    mamba.sub(imOut, imWrk, imOut)

def halfGradient(imIn, imOut, type="intern", n=1, se=mamba.DEFAULT_SE):
    """
    Computes the half morphological gradient of image 'imIn' ond puts the result
    in 'imOut'.
    
    'type' indicates if the half gradient should be internal or external. 
    Possible values are :
        "extern" : dilation(imIn) - imIn
        "intern" : imIn - erosion(imIn)
    
    The thickness can be controlled using parameter 'n' (1 by default). The 
    structuring element used by the erosion or the dilation is defined by 'se'.
    """
    
    imWrk = mamba.imageMb(imIn)
    if type=="extern":
        mamba.dilate(imIn, imWrk, n, se=se)
        mamba.sub(imWrk, imIn, imOut)
    else:
        mamba.erode(imIn, imWrk, n, se=se)
        mamba.sub(imIn, imWrk, imOut)
    
def whiteTopHat(imIn, imOut, n, se=mamba.DEFAULT_SE):
    """
    Performs a white Top Hat operation on 'imIn' and puts the result in 'imOut'.
    This operator extracts from 'imIn' the bright objects thinner than 2*'n'+1.

    The structuring element used is defined by 'se' ('DEFAULT_SE' by default).
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.opening(imIn, imWrk, n, se=se)
    mamba.sub(imIn, imWrk, imOut)

def blackTopHat(imIn, imOut, n, se=mamba.DEFAULT_SE):
    """
    Performs a black Top Hat operation on 'imIn' and puts the result in 'imOut'.
    This operator extracts from 'imIn' the dark objects thinner than 2*'n'+1. 
    
    The structuring element used is defined by 'se' ('DEFAULT_SE' by default).
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.closing(imIn, imWrk, n, se=se)
    mamba.sub(imWrk, imIn, imOut)

def supWhiteTopHat(imIn, imOut, n, grid=mamba.DEFAULT_GRID):
    """
    Performs a white Top Hat operation with the supremum of directional openings
    on 'imIn' and puts the result in 'imOut'.
    This operator partly extracts from 'imIn' the bright objects whose extension
    in at least one direction of 'grid' is smaller than 'n'.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.supOpen(imIn, imWrk, n, grid=grid)
    mamba.sub(imIn, imWrk, imOut)

def supBlackTopHat(imIn, imOut, n, grid=mamba.DEFAULT_GRID):
    """
    Performs a black Top Hat operation with the infimum of directional openings
    on 'imIn' and puts the result in 'imOut'.
    This operator partly extracts from 'imIn' the dark objects whose extension
    in at least one direction of 'grid' is smaller than 'n'.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.infClose(imIn, imWrk, n, grid=grid)
    mamba.sub(imWrk, imIn, imOut)
        
def regularisedGradient(imIn, imOut, n, grid=mamba.DEFAULT_GRID):
    """
    Computes the regularized gradient of image 'imIn' of size 'n'.
    The result is put in 'imOut'. A regularized gradient of size 'n' extracts
    in the image contours thinner than 'n' while avoiding false detections.
    
    This operation is only valid for omnidirectional structuring elements.
    """
    
    imWrk = mamba.imageMb(imIn)
    se = mamba.structuringElement(mamba.getDirections(grid), grid)
    gradient(imIn, imWrk, n, se=se)
    whiteTopHat(imWrk, imWrk, n, se=se)
    mamba.erode(imWrk, imOut, n-1, se=se)
    
