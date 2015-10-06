"""
Arithmetic and logical operators.

This module provides arithmetic operators such as addition, subtraction,
multiplication and division between images together with logical operators
(and, or, not, xor ...) between these images.
"""

import mamba
import mamba.core as core

def negate(imIn, imOut):
    """
    Negates the image 'imIn' and puts the result in 'imOut'.
    
    The operation is a binary complement for binary images and a negation for
    greyscale and 32-bit images.
    """
    err = core.MB_Inv(imIn.mbIm, imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def add(imIn1, imIn2, imOut):
    """
    Adds 'imIn2' pixel values to 'imIn1' pixel values and puts the result in
    'imOut'. The operation can be sum up in the following formula : 
    
    imOut = imIn1 + imIn2.

    You can mix formats in the addition operation (a binary image can be added
    to a greyscale image, etc...).
    However you must ensure that the output image is as deep as the deepest of 
    the two added images.
    
    The operation is also saturated for greyscale images (e.g. on a 8-bit
    greyscale image, 255+1=255). With 32-bit images, the addition is not saturated.
    """
    err = core.MB_Add(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()

def sub(imIn1, imIn2, imOut):
    """
    Subtracts 'imIn2' pixel values to 'imIn1' pixel values and puts the result 
    in 'imOut'. The operation can be sum up in the following formula :
    
    imOut = imIn1 - imIn2

    You can mix formats in the subtraction operation (a binary image can be
    subtracted to a greyscale image, etc...). 
    However you must ensure that the output image is as deep as the deepest of 
    the two subtracted images.
    
    The operation is also saturated for grey-scale images (e.g. on a grey scale 
    image 0-1=0) but not for 32-bit images.
    """
    err = core.MB_Sub(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def mul(imIn1, imIn2, imOut):
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
    err = core.MB_Mul(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def div(imIn1, imIn2, imOut):
    """
    Divides 'imIn1' pixel values with 'imIn2' pixel values and put the result
    in 'imOut'. The operation can be sum up in the following formula :
    
    imOut = imIn1 / imIn2

    Greyscale or 32-bit images can be used. You can mix formats in the divide operation.
    However you must ensure that the output image is as deep as 'imIn1'.
    
    In order to avoid errors due to divisions by zero, each time a pixel in 'imIn2' is equal
    to zero, the result is set to the maximum value corresponding to the depth of the image. 
    """
    err = core.MB_Div(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()

def diff(imIn1, imIn2, imOut):
    """
    Performs a set difference between 'imIn1' and 'imIn2' and puts the result in
    'imOut'. The set difference will copy 'imIn1' pixels in 'imOut' if the 
    corresponding pixel in 'imIn2' is lower and will write 0 otherwise:
    
    imOut = imIn1 if imIn1 > imin2
    imOut = 0 otherwise.
    
    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    err = core.MB_Diff(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()

def logic(imIn1, imIn2 , imOut, log):
    """
    Performs a logic operation between the pixels of images 'imIn1' and 'imIn2'
    and put the result in 'imOut'.
    The logic operation to be performed is indicated through argument 'log'.
    The allowed logical operations in 'log' are: 
    
    "and", "or", "xor", ""inf" or "sup". 
    
    "and" performs a bitwise AND operation, "or" a bitwise OR and "xor" a bitwise XOR.
    "inf" calculates the minimum and "sup" the maximum between corresponding pixel values.

    'imIn1', imIn2' and 'imOut' can be 1-bit, 8-bit or 32-bit images of same
    size and depth.
    """
    if log=="and":
        err = core.MB_And(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    elif log=="or":
        err = core.MB_Or(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    elif log=="xor":
        err = core.MB_Xor(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    elif log=="inf":
        err = core.MB_Inf(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    elif log=="sup":
        err = core.MB_Sup(imIn1.mbIm, imIn2.mbIm,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def addConst(imIn, v, imOut):
    """
    Adds 'imIn' pixel values to value 'v' and puts the result in 'imOut'. 
    The operation can be sum up in the following formula:
    
    imOut = imIn + v

    'imIn' and imOut' can be 8-bit or 32-bit images of same
    size and depth.
    
    The operation is saturated (limited to 255) for greyscale images.
    """
    err = core.MB_ConAdd(imIn.mbIm,v,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def subConst(imIn, v, imOut):
    """
    Subtracts 'v' value to 'imIn' pixel values and puts the result in 'imOut'. 
    The operation can be sum up in the following formula: 
    
    imOut = imIn - v

    'imIn' and imOut' can be 8-bit or 32-bit images of same
    size and depth.
    
    The operation is saturated (lower limit is 0) for greyscale images.
    """
    err = core.MB_ConSub(imIn.mbIm,v,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def mulConst(imIn, v, imOut):
    """
    Multiplies 'imIn' pixel values with value 'v' and puts the result in 'imOut'.
    The operation can be sum up in the following formula:
    
    imOut = imIn * v 

    The operation is saturated for greyscale images. You cannot use it with 
    binary images.
    """
    err = core.MB_ConMul(imIn.mbIm,v,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def divConst(imIn, v, imOut):
    """
    Divides 'imIn' pixel values by value 'v' and puts the result in 'imOut'. 
    The operation can be sum up in the following formula: 
    
    imOut = imIn / v
    (or more acurately : imIn = imOut * v + r, r being the ignored reminder)

    A zero value in 'v' will return an error.
    For a 8-bit image, v will be restricted between 1 and 255.
    You cannot use it with binary images.
    """
    err = core.MB_ConDiv(imIn.mbIm,v,imOut.mbIm)
    mamba.raiseExceptionOnError(err)
    imOut.update()

# Saturated arithmetic operators (for 32-bit images)

def ceilingAddConst(imIn, v, imOut):
    """
    Adds a constant value 'v' to image 'imIn' and puts the result in 'imOut'. If
    imIn + v is larger than the maximal possible value in imOut, the result is
    truncated and limited to this maximal value.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the addition is always truncated for 8-bit images.
    """
    
    imMask = mamba.imageMb(imIn, 1)
    imWrk = mamba.imageMb(imIn)
    mamba.addConst(imIn, v, imWrk)
    mamba.generateSupMask(imIn, imWrk, imMask, True)
    mamba.convertByMask(imMask, imOut, 0, mamba.computeMaxRange(imOut)[1])
    mamba.logic(imOut, imWrk, imOut, "sup")
    
def ceilingAdd(imIn1, imIn2, imOut):
    """
    Adds image 'imIn2' to image 'imIn1' and puts the result in 'imOut'. If
    imIn1 + imIn2 is larger than the maximal possible value in imOut, the result
    is truncated and limited to this maximal value.
    
    Although it is possible to use a 8-bit image for imIn2, it is recommended to
    use the same depth for all the images.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the addition is always truncated for 8-bit images.
    """
    
    imMask = mamba.imageMb(imIn1, 1)
    imWrk = mamba.imageMb(imIn1)
    mamba.add(imIn1, imIn2, imWrk)
    mamba.generateSupMask(imIn1, imWrk, imMask, True)
    mamba.convertByMask(imMask, imOut, 0, mamba.computeMaxRange(imOut)[1])
    mamba.logic(imOut, imWrk, imOut, "sup")

def floorSubConst(imIn, v, imOut):
    """
    Subtracts a constant value 'v' to image 'imIn' and puts the result in 'imOut'.
    If imIn - v is negative, the result is truncated and limited to 0.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the subtraction is always truncated for 8-bit images.
    """
    
    imMask = mamba.imageMb(imIn, 1)
    imWrk = mamba.imageMb(imIn)
    mamba.subConst(imIn, v, imWrk)
    mamba.generateSupMask(imIn, imWrk, imMask, False)
    mamba.convertByMask(imMask, imOut, 0, mamba.computeMaxRange(imOut)[1])
    mamba.logic(imOut, imWrk, imOut, "inf")
   
def floorSub(imIn1, imIn2, imOut):
    """
    Subtracts image 'imIn2' from image 'imIn1' and puts the result in 'imOut'.
    If imIn1 - imIn2 is negative, the result is truncated and limited to 0.
    
    Although it is possible to use a 8-bit image for imIn2, it is recommended to
    use the same depth for all the images.
    
    Note that this operator is mainly useful for 32-bit images, as the result
    of the subtraction is always truncated for 8-bit images.
    """
    
    imMask = mamba.imageMb(imIn1, 1)
    imWrk = mamba.imageMb(imIn1)
    mamba.sub(imIn1, imIn2, imWrk)
    mamba.generateSupMask(imIn1, imWrk, imMask, False)
    mamba.convertByMask(imMask, imOut, 0, mamba.computeMaxRange(imOut)[1])
    mamba.logic(imOut, imWrk, imOut, "inf")
    
def mulRealConst(imIn, v, imOut, nearest=False, precision=2):
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
    
    if imIn.getDepth()==1 or imOut.getDepth()==1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    imWrk1 = mamba.imageMb(imIn, 32)
    imWrk2 = mamba.imageMb(imIn, 1)
    precVal = (10 ** precision)
    v1 = int(v * precVal)
    if imIn.getDepth()==8:
        imWrk1.reset()
        mamba.copyBytePlane(imIn, 0, imWrk1)
    else:
        mamba.copy(imIn, imWrk1)
    mulConst(imWrk1, v1, imWrk1)
    if nearest:
        adjVal = int(5 * (10 ** (precision - 1)))
        addConst(imWrk1, adjVal , imWrk1)
    divConst(imWrk1, precVal, imWrk1)
    if imOut.getDepth()==8:
        mamba.threshold(imWrk1, imWrk2, 255, mamba.computeMaxRange(imWrk1)[1])
        mamba.copyBytePlane(imWrk1, 0, imOut)
        imWrk2.convert(8)
        mamba.logic(imOut, imWrk2, imOut, "sup")
    else:
        mamba.copy(imWrk1, imOut)

