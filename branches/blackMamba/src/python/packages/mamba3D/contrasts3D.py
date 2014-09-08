"""
Contrast 3D operators.

This module provides a set of functions to perform morphological contrast
operators such as gradient, top-hat transform, ....
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba

def gradient3D(imIn, imOut, n=1, se=m3D.CUBOCTAHEDRON1):
    """
    Computes the morphological gradient of 3D image 'imIn' and puts the
    result in 'imOut'. The thickness can be controlled using parameter 'n'
    (1 by default). The structuring element used by the erosion and dilation
    is defined by 'se' (CUBOCTAHEDRON1 by default).
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.erode3D(imIn, imWrk, n, se=se)
    m3D.dilate3D(imIn, imOut, n, se=se)
    m3D.sub3D(imOut, imWrk, imOut)

def halfGradient3D(imIn, imOut, type="intern", n=1, se=m3D.CUBOCTAHEDRON1):
    """
    Computes the half morphological gradient of 3D image 'imIn' ond puts
    the result in 'imOut'.
    
    'type' indicates if the half gradient should be internal or external. 
    Possible values are :
        "extern" : dilation(imIn) - imIn
        "intern" : imIn - erosion(imIn)
    
    The thickness can be controlled using parameter 'n' (1 by default). The 
    structuring element used by the erosion or the dilation is defined by 'se'.
    """
    
    imWrk = m3D.image3DMb(imIn)
    if type=="extern":
        m3D.dilate3D(imIn, imWrk, n, se=se)
        m3D.sub3D(imWrk, imIn, imOut)
    else:
        m3D.erode3D(imIn, imWrk, n, se=se)
        m3D.sub3D(imIn, imWrk, imOut)
    
def whiteTopHat3D(imIn, imOut, n, se=m3D.CUBOCTAHEDRON1):
    """
    Performs a white Top Hat operation on 'imIn' and puts the result in 'imOut'.
    This operator extracts from 'imIn' the bright objects thinner than 2*'n'+1.

    The structuring element used is defined by 'se' ('CUBOCTAHEDRON1' by default).
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.opening3D(imIn, imWrk, n, se=se)
    m3D.sub3D(imIn, imWrk, imOut)

def blackTopHat3D(imIn, imOut, n, se=m3D.CUBOCTAHEDRON1):
    """
    Performs a black Top Hat operation on 'imIn' and puts the result in 'imOut'.
    This operator extracts from 'imIn' the dark objects thinner than 2*'n'+1. 
    
    The structuring element used is defined by 'se' ('CUBOCTAHEDRON1' by default).
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.closing3D(imIn, imWrk, n, se=se)
    m3D.sub3D(imWrk, imIn, imOut)

def supWhiteTopHat3D(imIn, imOut, n, grid=m3D.DEFAULT_GRID3D):
    """
    Performs a white Top Hat operation with the supremum of directional openings
    on 'imIn' and puts the result in 'imOut'.
    This operator partly extracts from 'imIn' the bright objects whose extension
    in at least one direction of 'grid' is smaller than 'n'.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.supOpen3D(imIn, imWrk, n, grid=grid)
    m3D.sub3D(imIn, imWrk, imOut)

def supBlackTopHat3D(imIn, imOut, n, grid=m3D.DEFAULT_GRID3D):
    """
    Performs a black Top Hat operation with the infimum of directional openings
    on 'imIn' and puts the result in 'imOut'.
    This operator partly extracts from 'imIn' the dark objects whose extension
    in at least one direction of 'grid' is smaller than 'n'.
    """
    
    imWrk = m3D.image3DMb(imIn)
    m3D.infClose3D(imIn, imWrk, n, grid=grid)
    m3D.sub3D(imWrk, imIn, imOut)
        
def regularisedGradient3D(imIn, imOut, n, grid=m3D.DEFAULT_GRID3D):
    """
    Computes the regularized gradient of 3D image 'imIn' of size 'n'.
    The result is put in 'imOut'. A regularized gradient of size 'n' extracts
    in the 3D image contours thinner than 'n' while avoiding false detections.
    
    This operation is only valid for omnidirectional structuring elements.
    """
    
    imWrk = m3D.image3DMb(imIn)
    se = m3D.structuringElement3D(m3D.getDirections3D(grid), grid)
    gradient3D(imIn, imWrk, n, se=se)
    whiteTopHat3D(imWrk, imWrk, n, se=se)
    m3D.erode3D(imWrk, imOut, n-1, se=se)
    
    
