# exampleA3.py
# IN gallery.png
# OUT binary_segmentation.png segmented_gallery.png

## TITLE #######################################################################
# Color image segmentation with quasi-distance of the gradient

## DESCRIPTION #################################################################
# This example illustrates the use of the quasi-distance operator applied on a 
# color gradient to segment a scene. It also uses the Python Imaging Library (PIL)
# and the Mamba split operator to extract the three channels of a color image.
# 
# The gallery image is coming from the EC Funded CAVIAR (Context Aware Vision
# using Image-based Active Recognition) project/IST 2001 37540, found at 
# URL: http://homepages.inf.ed.ac.uk/rbf/CAVIAR/.

## SCRIPT ######################################################################
# Importing PIL Image module and mamba
from PIL import Image
from mamba import *

# Opening the image (PIL format) and splitting it into three color channels
pilim = Image.open('gallery.png')
imRed = imageMb(pilim.size[0], pilim.size[1], 8)
imGreen = imageMb(imRed)
imBlue = imageMb(imRed)
split(pilim, imRed, imGreen, imBlue)

# We will perform a thick gradient on each color channel (contours in original
# picture are more or less fuzzy) and we add all these gradients
gradIm = imageMb(imRed)
imWrk1 = imageMb(imRed)
gradIm.reset()
gradient(imRed, imWrk1, 2)
add(imWrk1, gradIm, gradIm)
gradient(imGreen, imWrk1, 2)
add(imWrk1, gradIm, gradIm)
gradient(imBlue, imWrk1, 2)
add(imWrk1, gradIm, gradIm)

# Then we invert the gradient image and we compute its quasi-distance
qDist = imageMb(gradIm, 32)
negate(gradIm, gradIm)
quasiDistance(gradIm, imWrk1, qDist)

# The maxima of the quasi-distance are extracted and filtered (too close maxima,
# less than 6 pixels apart, are merged) 
imWrk2 = imageMb(imRed)
imMark = imageMb(gradIm, 1)
copyBytePlane(qDist, 0, imWrk1)
subConst(imWrk1, 3, imWrk2)
build(imWrk1, imWrk2)
maxima(imWrk2, imMark)

# The marker-controlled watershed of the gradient is performed
imWts = imageMb(gradIm)
label(imMark, qDist)
negate(gradIm, gradIm)
watershedSegment(gradIm, qDist)
copyBytePlane(qDist, 3, imWts)

# The segmented binary and color image are stored
logic(imRed, imWts, imRed, "sup")
logic(imGreen, imWts, imGreen, "sup")
logic(imBlue, imWts, imBlue, "sup")
pilim = mix(imRed, imGreen, imBlue)
pilim.save('segmented_gallery.png')
negate(imWts, imWts)
imWts.save('binary_segmentation.png')


