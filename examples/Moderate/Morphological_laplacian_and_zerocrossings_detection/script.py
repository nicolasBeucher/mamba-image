# exampleM19.py
# IN flocs.png
# OUT laplacian.png zero-crossings.png

## TITLE #######################################################################
# Morphological laplacian and zero-crossings detection

## DESCRIPTION #################################################################
# This example shows how to define the morphological equivalent of the Laplacian
# operator. This morphological Laplacian is normalised and limited to the range
# [0, 255].
# The example also shows how the zero-crossings of this Laplacian (supposed to
# correspond to contours of salient objects) can be obtained by a SKIZ.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

# The Laplacian will use the squeeze operator which has been introduced in 
# example E12.
def squeeze(imIn, imOut, value1, value2):
    """
    Squeezes the pixel values of 'imIn' between 'value1' and 'value2'. If the
    pixel value is larger than 'value2', it is replaced by 'value2'. If it lower
    than 'value1', it is replaced by 'value1'. In-between values are unchanged.
    'imIn' and 'imOut' must have the same depth.
    """
    
    imWrk1 = imageMb(imIn, 1)
    imWrk2 = imageMb(imIn)
    # Replacing values lower than value1 by value1.
    threshold(imIn, imWrk1, 0, value1)
    convertByMask(imWrk1, imWrk2, 0, value1)
    logic(imIn, imWrk2, imOut, "sup")
    # Replacing values higher than value2 by value2.
    threshold(imOut, imWrk1, 0, value2)
    convertByMask(imWrk1, imWrk2, value2, computeMaxRange(imOut)[1])
    logic(imOut, imWrk2, imOut, "inf")

def laplacian(imIn, imOut, n=1, se=DEFAULT_SE):
    """
    Computes the morphological Laplacian (difference of outer and inner
    gradients) of greyscale image 'imIn' and puts the result in greyscale
    image 'imOut'. The result is normalised (squeezed) between 0 and 255.
    Negative values are shifted between 0 and 127, positive ones between
    129 and 255. The value 128 corresponds to the zeros of the Laplacian.
    The size 'n' of the Laplacian can be defined (default value is 1).
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn, 32)
    halfGradient(imIn, imWrk1, "extern", n=n, se=se)
    halfGradient(imIn, imWrk2, "intern", n=n, se=se)
    sub(imWrk1, imWrk2, imWrk3)
    addConst(imWrk3, 512, imWrk3)
    squeeze(imWrk3, imWrk3, 384, 639)
    subConst(imWrk3, 384, imWrk3)
    copyBytePlane(imWrk3, 0, imOut)

# Loading the initial image and defining the resulting image.
im1 = imageMb('flocs.png')
im2 = imageMb(im1)
# Performing a laplacian of size 3.
laplacian(im1, im2, 3)
# Storing the resulting image.
im2.save('laplacian.png')
# Defining other working images.
im3 = imageMb(im1)
imMarkers = imageMb(im1, 32)
imbin1 = imageMb(im1, 1)
imbin2 = imageMb(im1, 1)
# Determining the zero-crossings pixels.
imMarkers.reset()
# Mask of pixels corresponding to positive laplacian.
threshold(im2, imbin1, 129, 255)
# Removing small connected components.
buildOpen(imbin1, imbin1, 2)
# Giving them value equal to 2.
add(imMarkers, imbin1, imMarkers)
add(imMarkers, imbin1, imMarkers)
# Mask of negative pixels and filtering.
threshold(im2, imbin2, 0, 127)
buildOpen(imbin2, imbin2, 2)
# Generating the labels image...
add(imMarkers, imbin2, imMarkers)
# ...and the image to be processed.
logic(imbin1, imbin2, imbin1, "sup")
convertByMask(imbin1, im3, 1, 0)
# The SKIZ is obtained by means of a watershed transform.
basinSegment(im3, imMarkers)
# The boudaries between catchment basins correspond to
# zero-crossing pixels.
copyBytePlane(imMarkers, 0, im3)
halfGradient(im3, im3)
threshold(im3, imbin1, 0, 0)
# Saving the contours.
imbin1.save('zero-crossings.png')

