"""
Arithmetic and logical 3D operators.

This module provides arithmetic operators such as addition, subtraction,
multiplication, division and logical operators between 3D images.
(and, or, not, xor ...).
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

# Arithmetic operators #########################################################

def add3D(imIn1, imIn2, imOut):
    """
    Adds 'imIn2' pixel values to 'imIn1' pixel values and puts the result in
    'imOut'. The operation can be sum up in the following formula: 
    
    imOut = imIn1 + imIn2.

    You can mix formats in the addition operation (a binary image can be added
    to a greyscale image, etc...).
    However you must ensure that the output image is as deep as the deepest of 
    the two added images.
    
    The operation is also saturated for greyscale images (e.g. on a 8-bit
    greyscale image, 255+1=255). With 32-bit images, the addition is not saturated.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)

    for i in range(outl):
        mamba.add(imIn1[i], imIn2[i], imOut[i])

def sub3D(imIn1, imIn2, imOut):
    """
    Subtracts 'imIn2' pixel values to 'imIn1' pixel values and put the result 
    in 'imOut'. The operation can be sum up in the following formula:
    
    imOut = imIn1 - imIn2

    You can mix formats in the subtraction operation (a binary image can be
    subtracted to a greyscale image, etc...). 
    However you must ensure that the output image is as deep as the deepest of 
    the two subtracted images.
    
    The operation is also saturated for grey-scale images (e.g. on a grey scale 
    image 0-1=0) but not for 32-bit images.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)

    for i in range(outl):
        mamba.sub(imIn1[i], imIn2[i], imOut[i])
    
def mul3D(imIn1, imIn2, imOut):
    """
    Multiplies 'imIn2' pixel values with 'imIn1' pixel values and put the result
    in 'imOut'. The operation can be sum up in the following formula :
    
    imOut = imIn1 * imIn2

    You can mix formats in the multiply operation (a binary image can be
    multiplied with a greyscale image, etc...). 
    However you must ensure that the output image is as deep as the deepest of 
    the two input images.
    
    The operation is also saturated for greyscale images (e.g. on a greyscale 
    image 255*255=255).
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)

    for i in range(outl):
        mamba.mul(imIn1[i], imIn2[i], imOut[i])
    
def div3D(imIn1, imIn2, imOut):
    """
    Divides 'imIn1' pixel values with 'imIn2' pixel values and put the result
    in 'imOut'. The operation can be sum up in the following formula :
    
    imOut = imIn1 / imIn2

    You can mix formats in the divide operation.
    However you must ensure that the output image is as deep as 'imIn1'.
    
	In order to avoid divisions by zero, the result of the operation is set to
	the maximal pixel value whenever the corresponding pixel in 'imIn2' is
	equal to zero.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.div(imIn1[i], imIn2[i], imOut[i])

def addConst3D(imIn, v, imOut):
    """
    Adds 'imIn' pixel values to value 'v' and puts the result in 'imOut'. 
    The operation can be sum up in the following formula:
    
    imOut = imIn + v

    'imIn' and imOut' can be 8-bit or 32-bit images of same
    size and depth.
    
    The operation is saturated (limited to 255) for greyscale images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.addConst(imIn[i], v, imOut[i])
    
def subConst3D(imIn, v, imOut):
    """
    Subtracts 'v' value to 'imIn' pixel values and puts the result in 'imOut'. 
    The operation can be sum up in the following formula: 
    
    imOut = imIn - v

    'imIn' and imOut' can be 8-bit or 32-bit images of same
    size and depth.
    
    The operation is saturated (lower limit is 0) for greyscale images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.subConst(imIn[i], v, imOut[i])
    
def divConst3D(imIn, v, imOut):
    """
    Divides 'imIn' pixel values by value 'v' and puts the result in 'imOut'. 
    The operation can be sum up in the following formula: 
    
    imOut = imIn / v
    (or more acurately : imIn = imOut * v + r, r being the ignored reminder)

    A zero value in 'v' will return an error.
    For a 8-bit image, v will be restricted between 1 and 255.
    You cannot use it with binary images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.divConst(imIn[i], v, imOut[i])
    
def mulConst3D(imIn, v, imOut):
    """
    Multiplies 'imIn' pixel values with value 'v' and puts the result in 'imOut'.
    The operation can be sum up in the following formula:
    
    imOut = imIn * v 

    The operation is saturated for greyscale images. You cannot use it with 
    binary images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.mulConst(imIn[i], v, imOut[i])
        
def mulRealConst3D(imIn, v, imOut, nearest=False, precision=2):
    """
    Multiplies image 'imIn' by a real positive constant value 'v' and puts the 
    result in image 'imOut'. 'imIn' and 'imOut' can be 8-bit or 32-bit images.
    If 'imOut' is greyscale (8-bit), the result is saturated (results
    of the multiplication greater than 255 are limited to this value).
    'precision' indicates the number of decimal digits taken into account for
    the constant 'v' (default is 2).
    If 'nearest' is true, the result is rounded to the nearest integer value.
    If not (default), the result is simply truncated.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.mulRealConst(imIn[i], v, imOut[i], nearest, precision)

def negate3D(imIn, imOut):
    """
    Negates the 3D image 'imIn' and puts the result in 'imOut'.
    
    The operation is a binary complement for binary images and a negation for
    greyscale and 32-bit images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.negate(imIn[i], imOut[i])
        
def logic3D(imIn1, imIn2 , imOut, log):
    """
    Performs a logic operation between the pixels of images 'imIn1' and 'imIn2'
    and put the result in 'imOut'.
    The logic operation to be performed is indicated through argument 'log'.
    The allowed logical operations in 'log' are : 
    
    "and", "or", "xor", ""inf" or "sup". 
    
    "and" performs a bitwise AND operation, "or" a bitwise OR and "xor" a bitwise XOR.
    "inf" calculates the minimum and "sup" the maximum between corresponding pixel values.

    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.logic(imIn1[i], imIn2[i], imOut[i], log)
        
def diff3D(imIn1, imIn2, imOut):
    """
    Performs a set difference between 'imIn1' and 'imIn2' and puts the result in
    'imOut'. The set difference will copy 'imIn1' pixels in 'imOut' if the 
    corresponding pixel in 'imIn2' is lower and will write 0 otherwise:
    
    imOut = imIn1 if imIn1 > imin2
    imOut = 0 otherwise.
    
    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.diff(imIn1[i], imIn2[i], imOut[i])

# Saturated arithmetic operators (for 32-bit images)

def ceilingAddConst3D(imIn, v, imOut):
    """
    Adds a constant value 'v' to image 'imIn' and puts the result in 'imOut'. If
    imIn + v is larger than the maximal possible value in imOut, the result is
    truncated and limited to this maximal value.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the addition is always truncated for 8-bit images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.ceilingAddConst(imIn[i], v, imOut[i])
    
def ceilingAdd3D(imIn1, imIn2, imOut):
    """
    Adds image 'imIn2' to image 'imIn1' and puts the result in 'imOut'. If
    imIn1 + imIn2 is larger than the maximal possible value in imOut, the result
    is truncated and limited to this maximal value.
    
    Although it is possible to use a 8-bit image for imIn2, it is recommended to
    use the same depth for all the images.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the addition is always truncated for 8-bit images.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.ceilingAdd(imIn1[i], imIn2[i], imOut[i])

def floorSubConst3D(imIn, v, imOut):
    """
    Subtracts a constant value 'v' to image 'imIn' and puts the result in 'imOut'.
    If imIn - v is negative, the result is truncated and limited to 0.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the subtraction is always truncated for 8-bit images.
    """
    outl = len(imOut)
    inl = len(imIn)
    if inl!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.floorSubConst(imIn[i], v, imOut[i])
   
def floorSub3D(imIn1, imIn2, imOut):
    """
    subtracts image 'imIn2' from image 'imIn1' and puts the result in 'imOut'.
    If imIn1 - imIn2 is negative, the result is truncated and limited to 0.
    
    Although it is possible to use a 8-bit image for imIn2, it is recommended to
    use the same depth for all the images.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the subtractiontion is always truncated for 8-bit images.
    """
    outl = len(imOut)
    in1l = len(imIn1)
    in2l = len(imIn2)
    if in1l!=outl or in2l!=outl:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    
    for i in range(outl):
        mamba.floorSub(imIn1[i], imIn2[i], imOut[i])
    
