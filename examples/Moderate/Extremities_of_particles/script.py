# exampleM14.py
# IN eutectic.png hand.png 
# OUT eutectic_extremities.png hand_extremities.png

## TITLE #######################################################################
# Extremities of particles

## DESCRIPTION #################################################################
# This example illustrates the use of a geodesic distance function to extract
# the extremities of simply connected particles (without holes). Firstly, the
# centroid of each particle is obtained with an homotopic thinning with a D
# structuring element (this centroid is a sufficient approximation of the
# geodesic center). Then a geodesic distance function of each particle without
# its centroid is computed, the geodesic space being the particle itself.
# Finally, the extremities correspond to the maxima of this geodesic distance. 

## SCRIPT ######################################################################
# Importing the mamba modules
from mamba import *

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
    
# The procedure is applied on two different images    
# Opening and creating the first image 
im1 = imageMb('eutectic.png')
imTemp = imageMb(im1, 1)
imResult = imageMb(im1, 32)
im1.convert(1)
# A small filtering is performed to remove irregularities.
opening(im1, imTemp)
# Extraction of the extremities. In this case, the particles are considered
# to be inside the window. So extremities are detected on the edge.
extremities(imTemp, imResult, innerParticles=True)
# The binary image of the extremities is saved (slightly dilated to make
# them visible).
threshold(imResult, imTemp, 1, computeMaxRange(imResult)[1])
dilate(imTemp, imTemp)
imTemp.save('eutectic_extremities.png')
# The same operation is performed on the second image. The only difference
# concerns 'innerParticles'. Here, the hand is supposed to extend outside
# the window.
im2 = imageMb('hand.png')
imTemp = imageMb(im2, 1)
imResult = imageMb(im2, 32)
im2.convert(1)
opening(im2, imTemp)
extremities(imTemp, imResult)
threshold(imResult, imTemp, 1, computeMaxRange(imResult)[1])
dilate(imTemp, imTemp)
imTemp.save('hand_extremities.png')
