# exampleA18.py
# IN topography.png
# OUT rendering.png

## TITLE #######################################################################
# Topographic rendering of an image

## DESCRIPTION #################################################################
# This example illustrates the use of morphological operators for performing a
# topographic rendering of a grey scale image. To achieve this, we use the arrow
# encoding operator defined in example M18. 

## SCRIPT ######################################################################
# Importing the mamba module.
from mamba import *

# The arrowing operator is used in this example (see exampleM18.py).    
def arrowEncoding(imIn, imOut, oper, grid=DEFAULT_GRID):
    """
    This operator encodes the neighborhood of image 'imIn' and puts the result
    in greyscale image 'imOut'. The operator 'oper' may be one of the following:
    'sup', 'supeq', 'inf' or 'infeq'. 
    The 'grid' may be an hexagonal or square one. In the first case, the range
    of encodings is [0, 63], in the second case, it is [0, 255].
    """
   
    imWrk = imageMb(imIn)
    imMask = imageMb(imIn, 1)
    imOut.reset()
    if oper in ["inf", "sup"]:
        strict = True
    elif oper in ["infeq", "supeq"]:
        strict = False
    else:
        strict = ""
        # The above statement generates an error if 'oper' is not one of the
        # allowed ones.
    for i in range(gridNeighbors(grid)):
        dir = i + 1
        if oper in ["sup", "supeq"]:
            shift(imIn, imWrk, dir, 1, computeMaxRange(imIn)[1], grid=grid)
            generateSupMask(imWrk, imIn, imMask, strict)
        else:
            shift(imIn, imWrk, dir, 1, 0, grid=grid)
            generateSupMask(imIn, imWrk, imMask, strict)
        copyBitPlane(imMask, i, imOut)
                 
# Topographic rendering transform.
def shadowing(imIn, imOut, dir, brightness, height=(3,1)):
    """
    This operator takes the initial image 'imIn' and generates in image 'imOut'
    a topographic rendering of it. To enhance this rendering, a shadowing effect
    is superposed to the topography. The height of the sun is given by a tuple
    'height'. The two values correspond to the tangent of the angle of the sun
    rays. 'dir' is the direction of the light and 'brightness' indicates its
    intensity (contrast between sunny and shady regions). 
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn, 1)    
    copy(imIn, imWrk2)
    copy(imIn, imWrk1)
    # This part of the process aims at defining the region where the
    # shadow appears. This is done by calculating the residue between
    # the dilation of the image by an oblique segment until idempotence
    # and the original image.
    while computeVolume(imWrk1) !=0:
        shift(imWrk1, imWrk1, dir, height[1], 0)
        subConst(imWrk1, height[0], imWrk1)
        logic(imWrk2, imWrk1, imWrk2, "sup")
    # imWrk3 contains the shadow region.
    sub(imWrk2, imIn, imWrk1)
    threshold(imWrk1, imWrk3, 1, 255)
    closing(imWrk3, imWrk3)
    # The topography is built by arrowing (on hexagonal grid).
    arrowEncoding(imIn, imWrk1, "sup")
    mulConst(imWrk1, 4, imWrk1)
    # A constant value is added to the pixels outside the shadow.
    convertByMask(imWrk3, imWrk2, brightness, 0)
    add(imWrk1, imWrk2, imOut)

# Defining a new color palette, the sepia palette (old photographs colors).
# This color palette will be used with the topographic rendering image.
sepia = ()
for i in range(64):
    sepia = sepia + (4 * i, 2 * i, 0)
for i in range(64):
    sepia = sepia + (255, 2 * (i + 64), 0)
for i in range(128):
    sepia = sepia + (255, 255, 2 * i)

# Reading the initial image.
im1 = imageMb('topography.png')
im2 = imageMb(im1)
# Defining the new palette.
# Performing the rendering process. The sun is supposed to shine from the
# north east.
shadowing(im1, im2, 4, 25)
# Saving the result.
im2.save('rendering.png', palette=sepia)

