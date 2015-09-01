# exampleA2.py
# IN coffee_grains.jpg
# OUT segmented_grains_1.png segmented_grains_2.png

## TITLE #######################################################################
# Particles (coffee grains) separation and counting

## DESCRIPTION #################################################################
# This example shows how to separate touching or slightly overlapping
# particles (coffee grains in this example) in order to measure and count them.
# This example also illustrates how some small enhancements may deeply increase 
# the quality of the final result.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
import mambaDisplay

def autoThreshold(imIn, imOut):
    # Informations regarding this function can be found in previous
    # example.
    grad = imageMb(imIn)
    wrk = imageMb(imIn)
    level = imageMb(imIn, 1)
    gradient(imIn, grad)
    histo = getHistogram(imIn)
    distri = []
    for i in range(256):
        if histo[i]!=0:
            threshold(imIn, level, i, i)
            mul(level, grad, wrk)
            vol = computeVolume(wrk)/histo[i]
            distri.append(vol)
        else:
            distri.append(0)
    sd = sum(distri)
    sr = distri[0]
    threshval = 0
    while(sr<(sd/2)):
        threshval += 1
        sr += distri[threshval]
    threshold(imIn, imOut, threshval, 255)
    return threshval
    
def segmentGrains1(imIn, imOut):
    """
    Segments a binary image 'imIn' displaying grains using the distance 
    function and puts the result in binary image 'imOut'.
    """
    imDist = imageMb(imIn, 32)
    imDist8 = imageMb(imIn, 8)
    imWTS = imageMb(imIn, 8)
    
    # Segmentation of the grains with the distance function. Firstly, we 
    # compute the distance function (note the edge programming)
    computeDistance(imIn, imDist, edge=FILLED)
    
    # We verify (with computeRange) that the distance image is lower than
    # 256 and we copy it into a greyscale (8-bit) image
    computeRange(imDist)
    copyBytePlane(imDist, 0, imDist8)

    # The distance function is inverted and its valued watershed is computed
    negate(imDist8, imDist8)
    valuedWatershed(imDist8, imWTS)

    # The watershed lines are extracted (by thresholding) and subtracted from the 
    # initial image to give the first result
    threshold(imWTS, imOut, 1, 255)
    diff(imIn, imOut, imOut)
    
def segmentGrains2(imIn, imOut):
    """
    Segments a binary image 'imIn' displaying grains using the distance 
    function and puts the results in greyscale image 'imOut'.
    This segmentation uses a specific marker image and watershed segmentation
    to obtain better results than the previous function.
    This function returns the number of grains counted.
    """
    imMarker = imageMb(imIn, 1)
    imDist = imageMb(imIn, 32)
    imDist8 = imageMb(imIn, 8)
    imWTS32 = imageMb(imIn, 32)
    imWTS = imageMb(imIn, 8)
    
    # Segmentation of the grains with the distance function. Firstly, we 
    # compute the distance function (note the edge programming)
    computeDistance(imIn, imDist, edge=FILLED)
    
    # We verify (with computeRange) that the distance image is lower than
    # 256 and we copy it into a greyscale (8-bit) image
    computeRange(imDist)
    copyBytePlane(imDist, 0, imDist8)

    # The distance function is inverted and its valued watershed is computed
    negate(imDist8, imDist8)
    
    # Computing a marker image
    minima(imDist8, imMarker)
    dilate(imMarker, imMarker, 2)

    # Then, we compute the watershed of the inverted distance function controlled
    # by this marker set (note the number of connected components given by the 
    # labelling operator; they should correspond to the number of grains)
    nb = label(imMarker, imWTS32)
    watershedSegment(imDist8, imWTS32)

    # We build the labelled catchment basins
    copyBytePlane(imWTS32, 3, imWTS)
    negate(imWTS, imWTS)
    copyBytePlane(imWTS32, 0, imOut)
    logic(imOut, imWTS, imOut, "inf")

    # Then, we obtain the final (and better) result. Each grain is labelled
    convert(imIn, imWTS)
    logic(imOut, imWTS, imOut, "inf")
    
    return nb

# Loading the initial image and creating some working images
im = imageMb("coffee_grains.jpg")
imthresh = imageMb(im, 1)

# Using the function describes in exampleA1.py we compute the automatic
# threshold of our initial image
autoThreshold(im, imthresh)
# A bit of tidying
opening(imthresh, imthresh, 2)
negate(imthresh, imthresh)

# Computing the first segmentation of the coffee grains
imSeg1 = imageMb(im, 1)
segmentGrains1(imthresh, imSeg1)
# We store this result
imSeg1.save("segmented_grains_1.png")

# This first result is not perfect as some grains are badly segmented. This
# over-segmentation is due to parity problems affecting some maxima of the
# distance function. In order to cope with these defects, we use a marker
# controlled watershed of the inverted distance function. The markers are
# generated by a dilation of the minima of the inverted distance function

# Computing the second segmentation of the coffee grains
imSeg2 = imageMb(im, 8)
nb = segmentGrains2(imthresh, imSeg2)
# We store this result
# The palette can be changed before saving the result
imSeg2.save("segmented_grains_2.png", palette=mambaDisplay.getPalette("patchwork"))
print("number of grains : %d" % (nb))
# The result should be 50, however due to the black band on the right
# the function counts 51 coffee grains.

