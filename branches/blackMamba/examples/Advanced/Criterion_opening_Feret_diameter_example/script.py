# exampleA20.py
# IN binary_eutectic.png
# OUT H_Feret_label.png V_Feret_label.png bbox_filter.png

## TITLE #######################################################################
# Criterion opening, Feret diameter (bounding boxes) example

## DESCRIPTION #################################################################
# This example introduces another criterion opening: the bounding boxes opening.
# The feretDiameterOpening operator allows to label each connected component of
# a binary set with its Feret horizontal or vertical diameter. Then, sorting
# each component included in a bounding box of a given size is performed by a
# simple thresholding of the resulting images. 

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *
import mambaDisplay

def feretDiameterOpening(imIn, imOut, direc):
    """
    The Feret diameter of each connected component of the binary image 'imIn'
    is computed and its value labels the corresponding component. The labelled
    image is stored in the 32-bit image 'imOut'.
    If 'direc' is 'vertical', the vertical Feret diameter is computed. If it is
    set to 'horizontal', the corresponding diameter is used.    
    """
    
    imWrk1 = imageMb(imIn, 1)
    imWrk2 = imageMb(imIn, 32)
    imWrk3 = imageMb(imIn, 32)
    imWrk4 = imageMb(imIn, 32)
    
    imWrk1.fill(1)
    if direc == "horizontal":
        dir = 7    
    elif direc == "vertical":
        dir = 1
    else:
        dir = -1
        # The above statement generates an error ('direc' is not horizontal or 
        # vertical.
    # An horizontal or vertical distance function is generated.
    linearErode(imWrk1, imWrk1, dir, grid=SQUARE, edge=EMPTY)
    computeDistance(imWrk1, imOut, grid=SQUARE, edge=FILLED)
    addConst(imOut, 1, imOut)
    # Each particle is valued with the distance.
    convertByMask(imIn, imWrk2, 0, computeMaxRange(imWrk3)[1])
    logic(imOut, imWrk2, imWrk3, "inf")
    # The valued image is preserved.
    copy(imWrk3, imWrk4)
    # Each component is labelled by the maximal coordinate.
    build(imWrk2, imWrk3)
    # Using the dual reconstruction, we label the particles with the
    # minimal ccordinate.
    negate(imWrk2, imWrk2)
    logic(imWrk2, imWrk4, imWrk4, "sup")
    dualBuild(imWrk2, imWrk4)
    # We subtract 1 because the selected coordinate must be outside the particle.
    subConst(imWrk4, 1, imWrk4)
    negate(imWrk2, imWrk2)
    logic(imWrk2, imWrk4, imWrk4, "inf")
    # Then, the subtraction gives the Feret diameter.
    sub(imWrk3, imWrk4, imOut)
    
# Reading the initial image.
im1 = imageMb('binary_eutectic.png', 1)
im2 = imageMb(im1, 32)
im3 = imageMb(im1, 32)
# Labelling the connected components with the horizontal Feret diameter.
feretDiameterOpening(im1, im2, "horizontal")
# Same operation with the vertical Feret diameter.
feretDiameterOpening(im1, im3, "vertical")
# Coloring the results for a better view.
# Saving the results.
im2.save('H_Feret_label.png', palette=mambaDisplay.getPalette("rainbow"))
im3.save('V_Feret_label.png', palette=mambaDisplay.getPalette("rainbow"))
# Example of extraction of the connected components included in a square box
# of size 100.
temp1 = imageMb(im1)
temp2 = imageMb(im1)
threshold(im2, temp1, 1, 100)
threshold(im3, temp2, 1, 100)
logic(temp1, temp2, temp1, "inf")
# Saving the result.
temp1.save('bbox_filter.png')

