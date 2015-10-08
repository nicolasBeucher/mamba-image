# exampleA15.py
# IN eutectic.png
# OUT eutectic_disloc.png eutectic_cells.png

## TITLE #######################################################################
# Dislocations in an eutectic lamellar alloy

## DESCRIPTION #################################################################
# The problem addressed here is a problem of detection of dislocations in an
# eutectic lamellar alloy. This structure is characterised by a two-phase
# lamination with some discontinuities due to dislocations in the cristalline
# assembly. These dislocations induce loss of strength which is all the more
# important as their lengths are important. Moreover, the size of the cells 
# delimited by these dislocations is also important. This example shows that
# it is possible to build, by an appropriate sequence of operations, features
# which are not visible at the first sight.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
import mambaDisplay

# The extremities extractor designed in exampleM14 will also be necessary.
# It is duplicated below.

def extremities(imIn, imOut, innerParticles=False, grid=DEFAULT_GRID):
    """
    This operation performs the computation of the extremities (maxima of a
    geodesic distance function) and puts the result in imOut.
    'imIn' must be a binary image and 'imOut' is a 32-bit image containing the
    extremities and their geodesic distance to the centroid (allowing thus to
    sort them according to their distance to the center).
    If 'innerParticles' is set to False(default), the particles touching the
    edge are considered as extending outside the image window. Therefore, no
    extremity is detected on the edge of the image. If 'innerParticles' is True,
    all the particles are supposed to be included in the image, so extremities
    may appear on the edge.    
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn, 32)
    
    # Computation of the centroids.
    thinD(imIn, imWrk1, grid=grid) 
    # These centroids are removed from the initial image (each particle contains
    # a hole.
    diff(imIn, imWrk1, imWrk1)
    # Computing the geodesic distance (the elementary structuring element is
    # determined by the grid in use).
    se = structuringElement(getDirections(grid), grid)
    geodesicDistance(imWrk1, imIn, imOut, se=se)
    # The extremities correspond to the maxima.
    maxima(imOut, imWrk1, grid=grid)
    # Extremities on the edge are removed if 'innerParticles' is set to False.
    if not(innerParticles):
        removeEdgeParticles(imWrk1, imWrk1, grid=grid)
    # The extremities are given their corresponding distance to the center.
    convert(imWrk1, imWrk2)
    logic(imOut, imWrk2, imOut, "inf")
    
# To solve this problem, we need to define two new functions.
def geodesicAdaptiveDilate(imIn, imMask, imOut):
    """
    This operator performs a binary adaptive dilation. The greyscale image
    'imIn' indicates for each pixel the size of the geodesic dilation (by the 
    default structuring element) which will be applied on it. The geodesic
    mask is defined by the binary image 'imMask'. The result of the dilation is
    put in the binary image 'imOut'. It is called adaptive because its size is
    given locally for each pixel by the value of this pixel in 'imIn'.
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn)
    convert(imMask, imWrk1)
    copy(imIn, imWrk2)
    v1 = 0
    v2 = computeVolume(imWrk2)
    # At each step, the dilated image is decreased. So each pixel value
    # indicates how many steps of dilation remain. When the image volume
    # does not change, the process is finished.
    while v2 > v1:
        v1 = v2
        geodesicDilate(imWrk2, imWrk1, imWrk3)
        subConst(imWrk3, 1, imWrk3)
        logic(imWrk2, imWrk3, imWrk2, "sup")
        v2 = computeVolume(imWrk2)
    threshold(imWrk2, imOut, 1, 255)

def extremePoints(imIn, imOut):
    """
    This operator is a refinement of the 'extremities' operator. It determines
    points of the connected components of the binary set 'imIn' which are the
    farthest extremity points. The result is put in 'imOut'.
    Note that this operator needs that the connected components be inside the
    image and not touching the edges (a more refine operation could be designed
    but it is useless in this case).
    """
    
    imWrk1 = imageMb(imIn, 32)
    imWrk2 = imageMb(imIn, 8)
    imWrk3 = imageMb(imIn, 8)
    imWrk4 = imageMb(imIn, 8)
    imWrk5 = imageMb(imIn)
    imWrk6 = imageMb(imIn)
    imWrk7 = imageMb(imIn)
    # Extraction of extremities of initial image.
    extremities(imIn, imWrk1)
    convert(imIn, imWrk2)
    # Valued extremities are copied in 8-bit images.
    copyBytePlane(imWrk1, 0, imWrk3)
    copy(imWrk3, imWrk4)
    # Each particle is valued with the maximum extremity (may be more than one).
    build(imWrk2, imWrk4)
    # Farthest extremity is extracted.
    generateSupMask(imWrk3, imWrk4, imWrk5, False)
    logic(imWrk5, imIn, imWrk5, "inf")
    convert(imWrk5, imWrk2)
    logic(imWrk3, imWrk2, imWrk2, "inf")
    # This extremity is dilated by a geodesic dilation of size equal to its
    # value.
    geodesicAdaptiveDilate(imWrk2, imIn, imWrk6)
    # determination of points which are not reached yet.
    diff(imIn, imWrk6, imWrk6)
    # Remaining extremities are selected.
    convert(imWrk6, imWrk2)
    logic(imWrk3, imWrk2, imWrk3, "inf")
    # They are copied in a binary image.
    threshold(imWrk3, imWrk7, 1, 255)
    copy(imWrk3, imWrk4)
    # The process is run again to extract the farthest extremity among those
    # which remain (it is possible that the result be empty).
    build(imWrk2, imWrk4)
    generateSupMask(imWrk3, imWrk4, imWrk6, False)
    logic(imWrk6, imWrk7, imWrk6, "inf") 
    # This extremity is added to the previous sone(s).
    logic(imWrk5, imWrk6, imOut, "sup")

# Reading and converting the initial image.
im1 = imageMb('eutectic.png')
im1.convert(1)

# working images.
imWrk1 = imageMb(im1)
imWrk2 = imageMb(im1)
imWrk3 = imageMb(im1)
imWrk4 = imageMb(im1)
imWrk5 = imageMb(im1)
imWrk6 = imageMb(im1)
imWrk7 = imageMb(im1)
imWrk8 = imageMb(im1)
imWrk9 = imageMb(im1)
imWrk10 = imageMb(im1, 32)
imWrk11 = imageMb(im1, 8)
imWrk12 = imageMb(im1, 8)

# Performing the SKIZ of the lamellae.
fastSKIZ(im1, imWrk1)
# Extracting multiple points.
negate(imWrk1, imWrk2)
multiplePoints(imWrk2, imWrk3)
removeEdgeParticles(imWrk3, imWrk3)
# Separatng each arc of the boundaries.
diff(imWrk2, imWrk3, imWrk4)
# Arcs touching the edges are removed. They do not belong to dislocations.
removeEdgeParticles(imWrk4, imWrk5)
# Closed cells are rebuilt.
logic(imWrk5, imWrk3, imWrk2, "sup")
closeHoles(imWrk2, imWrk6)
diff(imWrk6, imWrk2, imWrk6)
# Isolated arcs (not surrounding cells) are kept separately.
dilate(imWrk6, imWrk2)
diff(imWrk5, imWrk2, imWrk7)
# Farthest extremities of these closed cells are extracted.
extremePoints(imWrk6, imWrk8)
# these extremities should mark arcs belonging to dislocations. These
# arcs are rebuilt.
dilate(imWrk8, imWrk2)
build(imWrk5, imWrk2)
# They are added to the isolated arcs. Multiple points are also introduced
# again.
logic(imWrk2, imWrk7, imWrk9, "sup")
logic(imWrk9, imWrk3, imWrk9, "sup")
# A small clipping allows to remove remaining barbs after the reintroduction
# of the multiple points.
whiteClip(imWrk9, imWrk9, step=1)
# The result image is saved.
imWrk9.save('eutectic_disloc.png')

# We can also build the cells containing stacked lamellae. This is done
# by adding boundaries connecting the edge and the end points of the previous
# dislocations image.
diff(imWrk4, imWrk5, imWrk5)
endPoints(imWrk9, imWrk2)
dilate(imWrk2, imWrk2, 2)
build(imWrk5, imWrk2)
logic(imWrk9, imWrk2, imWrk2, "sup")
# the lamellae belonging to the same cell are labelled and displayed in the
# same color.
negate(imWrk2, imWrk2)
erode(imWrk2, imWrk2, n=2, edge=EMPTY)
fastSKIZ(imWrk2, imWrk2)
nCells = label(imWrk2, imWrk10)
copyBytePlane(imWrk10, 0, imWrk11)
v = 256/nCells
mulConst(imWrk11, v, imWrk11)
convert(im1, imWrk12)
logic(imWrk11, imWrk12, imWrk11, "inf")
# The result image is saved (with different colors for the different cells).
# Note that the lamella at the upper right is ambiguous. Therefore, it has
# been given a different color.
imWrk11.save('eutectic_cells.png', palette=mambaDisplay.getPalette("rainbow"))

