# exampleA1.py
# IN coffee_grains.jpg
# OUT threshold_coffee_grains.jpg

## TITLE #######################################################################
# Automatic thresholding using gradient

## DESCRIPTION #################################################################
# This example shows how to compute an automatic threshold value using
# the gradient, histogram and volume computations.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

def autoThreshold(imIn, imOut):
    """
    Computes an automatic threshold image using the gradient.
    This function works well with greyscale images displaying two
    highly contrasted sets.
    It produces a binary image that sort of *segment* the two sets in two.
    """
    
    grad = imageMb(imIn)
    wrk = imageMb(imIn)
    level = imageMb(imIn, 1)
    # First the gradient is computed
    gradient(imIn, grad)
    
    # Then the histogram
    histo = getHistogram(imIn)
    
    distri = []
    for i in range(256):
        # First no point at looking at a particular value if there is no
        # pixel in it.
        if histo[i]!=0:
        
            # for each each possible pixel value, we extract the pixels
            # in imIn with that value
            threshold(imIn, level, i, i)
            # then we compute the volume of their corresponding pixels
            # in the gradient image (normalised by the number of
            # pixels)
            mul(level, grad, wrk)
            vol = computeVolume(wrk)/histo[i]
            # The volume is added to a distribution function
            distri.append(vol)
        else:
            distri.append(0)
            
    # Finding the median of the distribution
    sd = sum(distri)
    sr = distri[0]
    threshval = 0
    while(sr<(sd/2)):
        threshval += 1
        sr += distri[threshval]
            
    # Final computation
    threshold(imIn, imOut, threshval, 255)
    
    return threshval

im = imageMb("coffee_grains.jpg")
imbin = imageMb(im, 1)

# Computing the automatic threshold image
autoThreshold(im, imbin)
# And saving it
# The resulting image has a black band on the right because
# Mamba padded the original image so its width is a multiple of 64
# for performance reasons. This has a no impact on the quality of the result.
# Also notice that the result is not a very good segmentation as different
# coffee grains are connected in a unique set.
imbin.save("threshold_coffee_grains.jpg")

