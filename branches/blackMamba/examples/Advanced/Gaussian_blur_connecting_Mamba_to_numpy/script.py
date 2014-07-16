# exampleA6.py
# IN snake.png
# OUT blurred_snake.png

## TITLE #######################################################################
# Gaussian blur : connecting Mamba to numpy/scipy

## DESCRIPTION #################################################################
# Numpy and scipy are powerful Python API to perform scientific computations.
# Numpy provides a multidimensional array object and a very complete range
# of functions for fast operations on it such as convolution (see 
# http://www.scipy.org/). In this example, we show how to translate a Mamba
# image into an array and back and how to use it to perform a Gaussian blur.

## SCRIPT ######################################################################
# Importing mamba and associates
from mamba import *
# Importing the numpy and scipy packages
# You need to have them installed on your computer
import numpy as np
import scipy.signal

def getArrayFromImage(imIn):
    """
    Creates an 2D array containing the same data as in 'imIn'. Only
    works for greyscale and 32-bit images. Returns the array.
    """
    if imIn.getDepth()==8:
        dtype = np.uint8
    elif imIn.getDepth()==32:
        dtype = np.uint32
    else:
        import mambaCore
        raiseExceptionOnError(mambaCore.ERR_BAD_DEPTH)
        
    (w,h) = imIn.getSize()
    # First extracting the raw data out of image imIn
    data = imIn.extractRaw()
    # creating an array with this data
    # At this step this is a one-dimensional array
    array1D = np.fromstring(data, dtype=dtype)
    # Reshaping it to the dimension of the image
    array2D = array1D.reshape((h,w))
    return array2D
    
def fillImageWithArray(array, imOut):
    """
    Fills image 'imOut' with the content of two dimensional 'array'. Only
    works for greyscale and 32-bit images.
    """
    # Checking depth 
    if (imOut.getDepth()==8 and array.dtype != np.uint8) or \
       (imOut.getDepth()==32 and array.dtype != np.uint32) or \
       (imOut.getDepth()==1):
        import mambaCore
        raiseExceptionOnError(mambaCore.ERR_BAD_DEPTH)
    
    # image size
    (wi,hi) = imOut.getSize()
    # array size
    (ha,wa) = array.shape
    
    # Checking the sizes
    if wa!=wi or ha!=hi:
        import mambaCore
        raiseExceptionOnError(mambaCore.ERR_BAD_SIZE)
    
    # Extracting the data out of the array and filling the image with it
    data = array.tostring()
    imOut.loadRaw(data)
    
def gaussianBlur(imIn, imOut):
    """
    This function computes a Gaussian blur on 'imIn' using the scipy convolution
    with the appropriate kernel. The result is put into 'imOut'.
    """
    # Getting an array out of the snake image
    array = getArrayFromImage(imIn)
    # We then perform a convolution (here a gaussian blur)
    kernel = np.array( [ [ 0, 0, 5, 0, 0],
                         [ 0,11,16,11, 0],
                         [ 5,16,24,16, 5],
                         [ 0,11,16,11, 0],
                         [ 0, 0, 5, 0, 0] ])
    conv_array = scipy.signal.convolve2d(array, kernel, mode='same')
    # At this point conv_array contains value outside the rang of imOut.
    # Thus we rescale it.
    conv_array = conv_array - conv_array.min()
    conv_array = (conv_array * 255)/conv_array.max()
    # Changing its dtype to the original dtype
    conv_array = conv_array.astype(array.dtype)
    # Filling imOut with the result
    fillImageWithArray(conv_array, imOut)

im = imageMb("snake.png")
im1 = imageMb(im)
gaussianBlur(im, im1)
im1.save("blurred_snake.png")


