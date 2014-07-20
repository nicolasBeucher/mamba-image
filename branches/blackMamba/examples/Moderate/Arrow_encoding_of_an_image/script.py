# exampleM18.py
# IN burner.png
# OUT arrowedBurner.png

## TITLE #######################################################################
# Arrow encoding of an image

## DESCRIPTION #################################################################
# This example explains how a grey scale image can be arrowed. Arrowing an image
# consists in drawing arrows from each pixel to their corresponding neighbors if
# a given condition is fulfilled. Four conditions are possible: the center
# point value may be higher, higher or equal, lower or lower or equal to the 
# neighbor value. The arrows are encoded by a numerical value equal to the sum
# of the powers of 2 of the corresponding direction. If, for instance, an arrow
# exists in directions 1, 4 and 5, the encoded value will be (2 + 16 + 32) = 50.
# This representation of neighborhood relationships is interesting for building
# various operators simulating propagation phenomena or for designing adaptive
# transforms (generalised geodesy).

## SCRIPT ######################################################################
# Importing the mamba module.
from mamba import *

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
        # This statement generates an error if 'oper' is not one of the
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
       
# Loading the initial image.
im1 = imageMb('burner.png')

# Arrowing the image, result in im2. The operaton is the supremum (an arrow is
# drawn if the neighbor value is greater than the center value), the grid in
# use is the square one.
im2 = imageMb(im1)
arrowEncoding(im1, im2, "sup", grid=SQUARE)
# Storing the encoded image.
im2.save("arrowedBurner.png")  
           
   
