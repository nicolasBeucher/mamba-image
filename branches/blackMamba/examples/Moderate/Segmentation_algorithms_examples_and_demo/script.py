# exampleM12.py
# IN tools.png
# OUT tools_segP.png tools_segEW.png tools_segStd_g20.png tools_segStd_g15.png tools_segStd_g10.png tools_segExt.png

## TITLE #######################################################################
# Segmentation algorithms : examples and demo

## DESCRIPTION #################################################################
# This example shows the effect of the various segmentation algorithms
# embedded in the hierarchies module. These algorithms can produce
# quite impressive results but their usage is a bit tricky. This example is
# intended as a showroom of their results and to illustrate some of their
# properties (quality, speed, ...). Keep in mind that the results presented
# here are only valid for our test image and may be completely different
# on other images. See http://cmm.ensmp.fr/~beucher/publi/Unified_Segmentation.pdf
# and http://cmm.ensmp.fr/~beucher/publi/P-Algorithm_SB_BM.pdf for more
# information on these algorithms.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

im = imageMb("tools.png")

im1 = imageMb(im)
im2 = imageMb(im)
im3 = imageMb(im)
im4 = imageMb(im, 1)
im5 = imageMb(im)

# First computing the valued watershed of our image gradient
gradient(im, im1)
valuedWatershed(im1, im2)

# Enhanced Waterfalls
#####################
n = enhancedWaterfalls(im2, im3)
threshold(im3, im4, 0, n-1)
print("Enhanced waterfalls, levels = %d" % (n))
im4.save("tools_segEW.png")

# Standard algorithm
####################
# With a gain of 2 (default), it does not produce very better results
# than the enhanced waterfalls.
n = standardSegment(im2, im3)
threshold(im3, im4, 0, n-1)
print("Standard algorithm, levels = %d" % (n))
im4.save("tools_segStd_g20.png")
# Let's try with a smaller gain, like 1.5
# It produces what seems to be a better result
n = standardSegment(im2, im3, gain=1.5)
threshold(im3, im4, 0, n-1)
print("Standard algorithm, levels = %d" % (n))
im4.save("tools_segStd_g15.png")
# So why not lower the gain again ? 
# Well if the result seems equal to the enhanced it's because
# standardSegment with a 1.0 gain is equal to
# enhancedWaterfalls.
n = standardSegment(im2, im3, gain=0.5)
threshold(im3, im4, 0, n-1)
print("Standard algorithm, levels = %d" % (n))
im4.save("tools_segStd_g10.png")
# Regarding the gain, you should note that a greater gain will
# produce a more segmented image. Gains below 1.0 produces the
# same result as 1.0.

# P algorithm
#############
# Note that in this case, the P algorithm produces the best result.
# It is however one of the slowest (more hierarchical levels).
n = segmentByP(im2, im3)
threshold(im3, im4, 0, n-1)
print("P algorithm, levels = %d" % (n))
im4.save("tools_segP.png")

# Extended algorithm (experimental)
###################################
# This algorithm is allowing you to control the gain for
# each pixel of your image. This can produce interesting
# result such as segmenting only the object inside
# a certain focus area (objects outside or too big to fit
# are removed).
(w, h) = im.getSize()
im5.fill(1)
drawFillCircle(im5, (w/2, h/2, w/4), 2)
mul(im5, im2, im5)
n = extendedSegment(im2, im5, im3)
threshold(im3, im4, 0, n-1)
print("Extended algorithm, levels = %d" % (n))
im4.save("tools_segExt.png")

