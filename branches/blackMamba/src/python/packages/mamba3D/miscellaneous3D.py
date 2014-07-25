"""
This module regroups various functions/operators that performs operations which
do not fall in the others categories (properties extraction ...).
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

# Properties operators #########################################################

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
    
def checkEmptiness3D(imIn):
    """
    Checks if 3D image 'imIn' is empty (i.e. completely black).
    Returns True if so, False otherwise.
    
    'imIn' can be a 1-bit, 8-bit or 32-bit image.
    """
    inl = len(imIn)
    i = 0
    isEmpty = True
    while isEmpty and i<inl:
        isEmpty = mamba.checkEmptiness(imIn[i])
        i += 1
    return isEmpty
    
def compare3D(imIn1, imIn2, imOut):
    """
    Compares the two 3D images 'imIn1' and 'imIn2'.
    The comparison is performed pixelwise by scanning the two images from top left
    to bottom right starting with plane 0 and it stops as soon as a pixel is
    different in the two images.
    The corresponding pixel in 'imOut' is set to the value of the pixel of 
    'imIn1'.
    
    The function returns a tuple holding the position of the first mismatching 
    pixel. The tuple value is (-1,-1,-1) if the two images are identical.
    
    'imOut' is not reset at the beginning of the comparison.
    
    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.ERR_BAD_SIZE)
        
    z = 0
    x = -1
    y = -1
    while x<0 and z<outl:
        x,y = mamba.compare(imIn1[z], imIn2[z], imOut[z])
        z += 1
    if x<0:
        z = -1
    else:
        z -= 1
    return (x,y,z)
        
def shift3D(imIn, imOut, d, amp, fill, grid=m3D.DEFAULT_GRID3D):
    """
    Shifts 3D image 'imIn' in direction 'd' of the 'grid' over an amplitude of
    'amp'. The emptied space is filled with 'fill' value.
    The result is put in 'imOut'.
    """
    (width,height,length) = imIn.getSize()
    depth = imIn.getDepth()
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.ERR_BAD_SIZE)
    zext = grid.getZExtension()
    imWrk = m3D.image3DMb(width, height, length+zext*2, depth)
    for i in range(zext):
        imWrk[i].fill(fill)
        imWrk[length+zext*2-1-i].fill(fill)
    
    m3D.copy3D(imIn, imOut)
    for n in range(amp):
        m3D.copy3D(imOut, imWrk, 0, 1)
        for i in range(length):
            (planeOffset, dc) = grid.convertFromDir(d,i)
            mamba.shift(imWrk[i+1-planeOffset], imOut[i], dc, 1, fill, grid=grid.get2DGrid())

# Other operators ##############################################################

def drawEdge3D(imOut, thick=1):
    """
    Draws a frame around the edge of 'imOut' whose value equals the maximum
    range value and whose thickness is given by 'thick' (default 1).
    
    This function works with 3D images.
    """
    
    imOut.reset()
    se=m3D.structuringElement3D(list(m3D.getDirections3D(m3D.CUBIC)), m3D.CUBIC)
    m3D.dilate3D(imOut, imOut, thick, se=se, edge=mamba.FILLED)

