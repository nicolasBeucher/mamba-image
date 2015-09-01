# exampleE12.py
# IN burner.png
# OUT squeezed_burner.png

## TITLE #######################################################################
# Squeezing an image

## DESCRIPTION #################################################################
# This very simple example shows how to use the conversion by mask to force the
# pixel values of an image to be in a given range. This can be useful when
# incrusting a mixed information in an image as it allows to let room for this
# information.

## SCRIPT ######################################################################
# Importing the mamba module.
from mamba import *

# Defining the squeeze operator.
def squeeze(imIn, imOut, value1, value2):
    """
    Squeezes the pixel values of 'imIn' between 'value1' and 'value2'. If the
    pixel value is larger than 'value2', it is replaced by 'value2'. If it lower
    than 'value1', it is replaced by 'value1'. In-between values are unchanged.
    'imIn' and 'imOut' must have the same depth.
    """
    
    imWrk1 = imageMb(imIn, 1)
    imWrk2 = imageMb(imIn)
    # Replacing values lower than value1 by value1.
    threshold(imIn, imWrk1, 0, value1)
    convertByMask(imWrk1, imWrk2, 0, value1)
    logic(imIn, imWrk2, imOut, "sup")
    # Replacing values higher than value2 by value2.
    threshold(imOut, imWrk1, 0, value2)
    convertByMask(imWrk1, imWrk2, value2, computeMaxRange(imOut)[1])
    logic(imOut, imWrk2, imOut, "inf")

# Squeezing an image between 80 and 150.
im1 = imageMb('burner.png')
im2 = imageMb(im1)
squeeze(im1, im2, 80, 150)
# Saving the result.
im2.save('squeezed_burner.png')

