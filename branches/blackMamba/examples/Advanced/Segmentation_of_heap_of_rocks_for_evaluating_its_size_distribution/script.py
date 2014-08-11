# exampleA16.py
# IN rocks.png
# OUT rocks_granu.png rocks_markers.png rocks_segment.png

## TITLE #######################################################################
# Segmentation of a heap of rocks for evaluating its size distribution

## DESCRIPTION #################################################################
# Measuring the size distribution of heaps of rocks is an important task for
# a quarry manager. This information is crucial to optimize the efficiency of
# rocks crushers. The best and fastest way to get this information is by means
# of an image of the rocks taken from the skip of a lorry or from a conveyor
# belt. However, obtaining the size distribution from the image is far from
# being easy. This example shows that the use of the ultimate opening operator
# allows to get not so bad results. 

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
import mambaDisplay

# Reading the image.
im1 = imageMb('rocks.png')

# Defining working images.
imWrk0 = imageMb(im1)
imWrk1 = imageMb(im1)
imWrk2 = imageMb(im1, 32)
imWrk3 = imageMb(im1)
imWrk4 = imageMb(im1)
imWrk5 = imageMb(im1, 1)
imWrk6 = imageMb(im1)
imWrk7 = imageMb(im1)
imWrk8 = imageMb(im1, 1)
imWrk9 = imageMb(im1, 1)

# The initial image is filtered by an alternate filter by reconstruction.
buildOpen(im1, imWrk0)
buildClose(imWrk0, imWrk0)
# The ultimate opening residual operator is applied to the image. In order
# to obtain results of better quality, operators with dodecagons are used.
ultimateIsotropicOpening(imWrk0, imWrk1, imWrk2)
# The granulometric image is extracted.
copyBytePlane(imWrk2, 0, imWrk3)
# This image is saved with a color palette.
imWrk3.save('rocks_granu.png', palette=mambaDisplay.getPalette("patchwork"))
# The flat zones of the granulometric image are extracted (these zones have
# a gradient equal to zero).
gradient(imWrk3, imWrk4)
threshold(imWrk4, imWrk5, 1, 255)
negate(imWrk5, imWrk5)
# Holes in these zones are filled (they correspond to artifacts).
closeHoles(imWrk5, imWrk5)
# The real size of these flat zones is determined by a dodecagonal distance
# function.
isotropicDistance(imWrk5, imWrk2, edge=FILLED)
copyBytePlane(imWrk2, 0, imWrk6)
# We add one to correct the bias brought by the gradient.
addConst(imWrk6, 1, imWrk6)
# The real size is compared to the size given by the granulometric function.
# When the real size is less than half the size of the granulometric function,
# the corresponding flat zone cannot be considered as a marker of a block.
divConst(imWrk3, 2, imWrk7)
generateSupMask(imWrk6, imWrk7, imWrk8, False)
# The extracted markers are filtered with an alternate filter by reconstruction
# to connect the closest ones and to remove the smallest ones. 
buildClose(imWrk8, imWrk9)
buildOpen(imWrk8, imWrk9)
# The result is saved.
imWrk9.save('rocks_markers.png')

# In this second part, we shall use the previous markers to segment the blocks
# in the heap of rocks.

# The gradient of the original filtered image is computed.
gradient(imWrk0, imWrk1)
# In order to get a better result, we must also introduce markers for the
# background. These markers correspond the highest flat zones of the
# granulometric function.
t = computeRange(imWrk3)[1]
threshold(imWrk3, imWrk5, t, 255)
# A small correction is applied to insure that blocks markers and background
# markers are not touching each other.
dilate(imWrk5, imWrk8)
diff(imWrk9, imWrk8, imWrk9)
# To be sure that background markers mark only the background, they are reduced
# to a point (after filling of their holes).
closeHoles(imWrk5, imWrk5)
thinD(imWrk5, imWrk5)
# The rocks markers are labelled.
nbStones = label(imWrk9, imWrk2)
print("Number of stones : %d" % (nbStones))
# We add 1 to the label values to let room for the background marker.
add(imWrk2, imWrk9, imWrk2)
# The background marker is added (label 1). Note that all the connected
# components of the background marker share the same label value.
add(imWrk2, imWrk5, imWrk2)
# The watershed of the gradient is performed.
watershedSegment(imWrk1, imWrk2)
copyBytePlane(imWrk2, 3, imWrk4)
threshold(imWrk4, imWrk8, 0,0)
# The background marker is used to build the catchment basins corresponding
# to the background. Then, they are removed from the segmented image.
build(imWrk8, imWrk5)
diff(imWrk8, imWrk5, imWrk5)
# The segmented image is saved.
imWrk5.save('rocks_segment.png')

