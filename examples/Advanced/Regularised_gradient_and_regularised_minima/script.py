# exampleA19.py
# IN car.png
# OUT reg_minima.png car_contours1.png car_contours2.png

## TITLE #######################################################################
# Regularised gradient and regularised minima

## DESCRIPTION #################################################################
# This example shows how regularised gradients can be used to define better
# markers for image segmentation. More details about the algorithm presented 
# here can be found in http://cmm.ensmp.fr/~beucher/publi/SB_these.pdf, pages
# 63-65. A marker-controlled gradient watershed segmentation is performed to
# show the benefit of this operator compared to the use of a classical gradient.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

# Defining a regularised minima extractor.
def regularisedMinima(imIn, imOut, maxSize=8):
    """
    This operator performs regularised gradients of image 'imIn' for sizes in 
    the range [1, maxSize - 1]. The influence zone of the regularised gradient
    is taken into account by dilating it (dilation of size i - 1). Then the 
    supremum of all the dilated gradients is computed. This allows to absorb
    contours of small height which are in the vicinity of more contrasted ones.
    At the end, the minima of the supremum are extracted and stored in the 
    binary image 'imOut'.
    """

    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk2.reset()
    for i in range(1, maxSize + 1):
        regularisedGradient(imIn, imWrk1, i)
        n = i - 1
        dilate(imWrk1, imWrk1, n)
        logic(imWrk2, imWrk1, imWrk2, "sup")
    minima(imWrk2, imOut)
 
# Testing the algorithm.
# Reading the initial image.
im1 = imageMb('car.png')
imMarkers = imageMb(im1, 1)

# Extracting the regularised minima. Applying the operator in the range (1, 4)
# is sufficient.
regularisedMinima(im1, imMarkers, 4)
# Storing the result.
imMarkers.save('reg_minima.png')
# Computing the classical gradient.
im2 = imageMb(im1)
gradient(im1, im2)
# Performing the classical gradient watershed segmentation.
im3 = imageMb(im1)
valuedWatershed(im2, im3)
imbin = imageMb(im1, 1)
threshold(im3, imbin, 0, 0)
# Saving the result.
imbin.save('car_contours1.png')
# Using the previous markers to perform a marker-controlled segmentation.
im32 = imageMb(im1, 32)
nb = label(imMarkers, im32)
watershedSegment(im2, im32)
copyBytePlane(im32, 3, im3)
threshold(im3, imbin, 0, 0)
# Saving this segmentation.
imbin.save('car_contours2.png')

