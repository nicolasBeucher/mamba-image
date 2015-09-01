# exampleA10.py
# IN boron1.png boron2.png
# OUT fibers_connectivity.png

## TITLE #######################################################################
# Analysis of the distribution of boron fibers

## DESCRIPTION #################################################################
# This example illustrates the judicious use of connectivity measures for
# solving a problem of quality control. The images represent boron fibers in
# a composite material. These fibers reinforce the mechanical resistance of
# the material. The resistance increases in proportion of the evenness of
# the fibers layout. Therefore, during industrial production, they are as
# far as possible placed according to a regular hexagonal network. However,
# irregularities occur. The problem consists in quantifying these
# irregularities by means of an appropriate measurement.
# This example illustrates the use of the matplotlib library with Mamba
# (to run this example, you must install this library).

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *

# Importing the plot function from matplotlib
import matplotlib.pyplot as plot

def closeFibers(imIn, imOut):
    """
    This operation cleans the original fibers image by closing their contours
    and by closing their interiors. Note that this operation also fill the
    fibers which are cutting the edges of the image.
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn)
    
    negate(imIn, imWrk1)
    # Linear dilation of size 2 in horizontal direction to connect fibers
    # contours.
    linearDilate(imWrk1, imWrk1, 5, 2)
    # Filling true holes (interior fibers)
    closeHoles(imWrk1, imWrk2)
    # Extracting all the fibers cutting the edges.
    removeEdgeParticles(imWrk2, imWrk3)
    diff(imWrk2, imWrk3, imWrk3)
    # The image is inverted and eroded to get a background marker.
    negate(imWrk3, imWrk3)
    erode(imWrk3, imOut, n=20, edge=EMPTY)
    # Reconstructing the background and adding fibers cutting the edges to
    # the previous ones.
    build(imWrk3, imOut)
    diff(imOut, imWrk2, imWrk2)
    # Another linear dilation in transposed direction to recover the initial
    # sizes of the fibers.
    linearDilate(imWrk2, imWrk2, 2, 2)
    # final result
    negate(imWrk2, imOut)    

def checkEvenness(imIn, maxSize):
    """
    Checks the regularity of the boron fibers arrangement by computing
    successive closings ans by determining at each step the connectivity
    number of the closing. The variation of this measure from a positive
    to a negative value indicates the evenness of the arrangement. The
    more it is regular, the more this variation is fast and important.
    The successive connectivity numbers are returned in a list.
    """
    
    imWrk = imageMb(imIn)
    ncList =[]
    for i in range(maxSize + 1):
        closing(imIn, imWrk, i)
        nc = computeConnectivityNumber(imWrk)
        ncList.append(nc)
    return ncList

# The whole procedure is applied on two different images
# Warning! this example works only on the hexagonal grid.
setDefaultGrid(HEXAGONAL)
# Opening and creating the first image 
im1 = imageMb('boron1.png')
imtemp = imageMb(im1, 1)
im1.convert(1)
# Closing holes in the fibers.
closeFibers(im1, imtemp)
# Then, the connectivity numbers of the successive closings are computed
# and stored in a list.
maxSize = 20
ncList1 = checkEvenness(imtemp, maxSize)
# The same operation is performed on the second image
im2 = imageMb('boron2.png')
imtemp = imageMb(im2, 1)
im2.convert(1)
# Closing holes in the fibers
closeFibers(im2, imtemp)
# Then, the connectivity numbers of the successive closings are computed
# and stored in a list.
maxSize = 20
ncList2 = checkEvenness(imtemp, maxSize)
# Plotting the two curves with mathplotlib and showing them.
xs = range(maxSize + 1)
ys = ncList1
zs = ncList2
plot.xlabel('Size of closing')
plot.ylabel('Connectivity number')
plot.title('Boron images connectivity numbers variations after closings')
plot.plot(xs, ys, label='Boron1 image', color='red')
plot.plot(xs, zs, label='Boron2 image', color='blue')
plot.legend(loc='upper right')
# The slope of the curves is an indicator of the regularity of the arrangement.
# A perfectly regular arrangement would exhibit a sudden transition between
# positive connectivity numbers and negative ones. The transition for the
# boron2 image is steeper than for the boron1 image as the arrangement of fibers
# is more regular in this latter image.
plot.savefig('fibers_connectivity.png')
