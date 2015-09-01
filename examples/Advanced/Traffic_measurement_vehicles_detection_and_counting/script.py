# exampleA22.py
# IN traffic.png traffic_sum.png traffic_road_mask.png
# OUT detected_vehicles.png

## TITLE #######################################################################
# Traffic measurement, vehicles detection and counting

## DESCRIPTION #################################################################
# This example is the sequel of example A21. It shows how to detect vehicles in
# a traffic image. Although the process uses a simple feature to characterize a
# vehicle (namely the shadow in front of each car), it is rather robust. The
# mean image of example A21 is used again and is subtracted from the current
# image. Then the maxima of the resulting image which are sufficiently high are
# extracted as vehicles markers.
# The other interest of this example comes from the fact that an adaptive linear
# opening is defined to filter the previous minima. The size of the filtering
# varies according to the position of each pixel in the image. This size is
# controlled by an image which has been generated with the mask of the road
# obtained in example A21.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
from mambaDisplay.extra import *

# Defining the extended maxima extractor.
def deepMaxima(imIn, imOut, d):
    """
    This function extracts the maxima (or domes) of the greyscale image 'imIn'
    whose depth (or height) is higher than 'd'. The result is put in binary
    image 'imOut'.
    (Note that this operator is different from the 'maxima' operator).
    """
    
    imWrk = imageMb(imIn)
    subConst(imIn, d, imWrk)
    hierarBuild(imIn, imWrk)
    maxima(imWrk, imOut)

# Defining an adaptive linear opening.
def adaptiveHorizontalOpen(imIn, scaleIm, imOut):
    """
    This operator performs an horizontal linear opening of binary image 'imIn'
    and puts the result in binary image 'imOut'. The size of the opening is given
    for each pixel of 'imIn' by the value of the corresponding pixel in image
    'scaleIm'.
    This operator belongs to the generalized geodesic operators class.
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(scaleIm)
    imWrk4 = imageMb(imIn)
    copy(imIn, imWrk1)
    copy(scaleIm, imWrk3)
    # Computing an adaptive linear erosion. After each step of erosion, image
    # scaleIm is decremented. Only the pixels of imIn for which scaleIm is not
    # equal to zero are eroded. The other pixels are unchanged.
    while computeVolume(imWrk3) != 0:
        linearErode(imWrk1, imWrk2, 2, edge=EMPTY)
        threshold(imWrk3, imWrk4, 1, 255)
        logic(imWrk2, imWrk4, imWrk2, "inf")
        diff(imWrk1, imWrk4, imWrk1)
        logic(imWrk1, imWrk2, imWrk1, "sup")
        subConst(imWrk3, 1, imWrk3)
    # Linear horizontal dilation performed with a linear geodesic reconstruction.
    buildNeighbor(imIn, imWrk1, 2)
    copy(imWrk1, imOut)

# The vehicles extraction process is now defined.
# Firstly, the scale image used by the aadaptive opening is built from the mask
# of the road. 
imb1 = imageMb('traffic_road_mask.png')
imb1.convert(1)
imb2 = imageMb(imb1)
imb3 = imageMb(imb1)
imW = imageMb(imb1, 32)
im1 = imageMb(imb1, 8)
im2 = imageMb(imb1, 8)
# A vertical marker is defined in image imb2.
linearDilate(imb2, imb2, 2, edge=FILLED)
# The right border of the image is rebuilt and added to the marker.
negate(imb1, imb3)
build(imb3, imb2)
logic(imb1, imb2, imb2, "sup")
# The distance function of this set is computed and transferred in a greyscale
# image. The restriction of this distance to the mask of the road is calculated.
computeDistance(imb2, imW, edge=FILLED)
copyBytePlane(imW, 0, im1)
convert(imb1, im2)
logic(im1, im2, im1, "inf")
# A linear reconstruction labels each line of the image window with the width
# of the road.
im2.fill(255)
# v is used to swallow the area returned by buildNeighbor (not used).
v = buildNeighbor(im2, im1, 2)
v = buildNeighbor(im2, im1, 5)
# The traffic image and the mean image are loaded.
im2 = imageMb('traffic.png')
im3 = imageMb('traffic_sum.png')
# Their difference (limited to zero) is performed.
sub(im3, im2, im3)
# The height of the maxima which are considered as salient ones is calculated.
# This height corresponds to half the range of values of the difference image.
height = computeRange(im3)[1]/2
# The salient maxima are extracted.
deepMaxima(im3, imb2, height)
# Holes in the maxima are closed.
closeHoles(imb2, imb2)
# The real width of the road is approximately equal to 9 meters. So, by dividing
# the im1 image by 9, each pixel of the resulting image is given a value equal
# to the number of iterations needed to achieve a linear erosion of size equal
# to one meter (the minimal width of a vehicle is about 1.5 m).
divConst(im1, 9, im3)
# An adaptive opening controlled by the previously defined scale function is
# performed.
adaptiveHorizontalOpen(imb2, im3, imb3)
# A small closing allows to connect close connected components of markers.
closing(imb3, imb3)
# Each vehicle marker is reduced to a point and dilated to enhance its display.
thinD(imb3, imb3)
dilate(imb3, imb3, 5)
# The result is displayed.
superpose(im2, imb3)


