# exampleA21.py
# IN traffic_sum.png traffic_diff.png
# OUT lanes_road_masks.png segmented_lanes.png

## TITLE #######################################################################
# Traffic lanes segmentation

## DESCRIPTION #################################################################
# This example illustrates the use of two images of a traffic scene to segment
# the traffic lanes. Firstly, the mean of successive difference images is used
# to define lanes markers. This image indicates the regions of the scene where
# some motion occurs. The lanes markers are then dilated to generate the road
# mask. The size of the dilation depends of the vertical coordinate of each
# pixel in order to take into account the apparent metrics due to the
# perspective view.
# Secondly, the lanes are segmented. This segmentation is performed by a 
# watershed of a distance function generated from the ground markings extracted
# from the mean image of the scene (moving objects have been removed).

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
from mambaDisplay.extra import *

# Special distance function generator.
def geodesicGreyDistance(imIn, imMask, imOut):
    """
    This operator computes a distance function from the greyscale image 'imIn'
    by performing a conic dilation until idempotence. Moreover, this dilation
    is a geodesic one, controlled by the 'imMask' image. The result is put in
    'imOut'.
    """
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    
    copy(imIn, imWrk1)
    convert(imMask, imWrk2)
    prev_vol = 0
    logic(imIn, imWrk2, imOut, "inf")
    vol = computeVolume(imOut)
    while vol > prev_vol:
        prev_vol = vol
        dilate(imOut, imWrk1)
        subConst(imWrk1, 1, imWrk1)
        logic(imWrk1, imOut, imOut, "sup")
        logic(imOut, imWrk2, imOut, "inf")
        vol = computeVolume(imOut)

# Loading initial images.
im1 = imageMb('traffic_sum.png')
im2 = imageMb('traffic_diff.png')
# Defining resulting images.
# This image will contain the lanes markers.
im3 = imageMb(im1, 1) 
# This image will contain the mask of the road.
im4 = imageMb(im1, 1)
# This image will contain the segmented lanes.
im5 = imageMb(im1, 1)
# Working images.
imWrk1 = imageMb(im1)
imWrk2 = imageMb(im1, 1)
imWrk3 = imageMb(im1, 32)
imWrk4 = imageMb(im1, 32)
imWrk5 = imageMb(im1, 32)
imWrk6 = imageMb(im1)

# Marking the lanes and generating the road mask.
# Filtering the mean of differences.
buildOpen(im2, imWrk1, 3)
# Thresholding it (the threshold value is equal to half the maximum grey value).
thrval = computeRange(imWrk1)[1] / 2
threshold(imWrk1, imWrk2, thrval, 255) 
# The image is filtered and gives the lanes markers.
closing(imWrk2, im3)
# The distance function of the complementary set is computed. Note that the
# edge is set to 'filled'.
negate(im3, imWrk2)
computeDistance(imWrk2, imWrk3, edge=FILLED)
# Generating two markers at right and left of the image window. Note that the
# linear dilations are performed with a FILLED edge (quite unusual...).
imWrk4.reset()
linearDilate(imWrk4, imWrk4, 2, edge=FILLED)
linearDilate(imWrk4, imWrk4, 5, edge=FILLED)
# Rebuilding parts of the distance function at left and right.
build(imWrk3, imWrk4)
diff(imWrk3, imWrk4, imWrk4)
# Filling an image with the maximum value of the remaining parts of the distance
# function on every horizontal line of the image. This is performed by means of
# directional horizontal reconstructions. 'val' is just used to swallow the
# unused value returned by 'buildNeighbor'. 
imWrk5.reset()
negate(imWrk5, imWrk5)
val = buildNeighbor(imWrk5, imWrk4, 2)
val = buildNeighbor(imWrk5, imWrk4, 5)
# The pixel values of the initial distance function which are lower than or
# equal to the previous mask image correspond to the road mask image. This
# approach allows to perform an adaptive dilation on each line in order to take
# the perspective into account (generalised distance). 
generateSupMask(imWrk4, imWrk3, im4, False)
# Displaying the result by superposing the road and the lanes markers.
superpose(im4, im3)

# Segmenting the lanes.
# Extracting the ground markings (their thickness is known, hence the parameter
# value equal to 8).
whiteTopHat(im1, imWrk1, 8)
# The zone separating the lanes is extracted.
diff(im4, im3, imWrk2)
# Computing a special quasi-distance from the ground markings.
geodesicGreyDistance(imWrk1, imWrk2, imWrk6)
# Segmenting the lanes with a watershed of this quasi-distance controlled by the
# lanes markers. The watershed lines pass through the ground markings.
markerControlledWatershed(imWrk6, im3, imWrk1)
# Generating the boundaries of the lanes.
threshold(imWrk1, imWrk2, 1, 255)
diff(im4, imWrk2, imWrk2)
dilate(imWrk2, im4)
diff(im4, imWrk2, im5)
# Displaying the result.
superpose(im1, im5)

