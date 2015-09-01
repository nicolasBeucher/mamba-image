# exampleA17.py
# IN binary_foam.png
# OUT area_labelling.png

## TITLE #######################################################################
# Area labelling and area opening

## DESCRIPTION #################################################################
# This example explains how particles can be labelled by their area with a fast
# algorithm which does not use a particle analysis. It uses look-up tables to
# achieve this. Getting instantaneously all the particles with an area lower
# than a given value is made by a simple threshold of the result image. This
# operator allows to obtain area openings of the initial image. This operator is
# applied to an image of bubbles in Champagne wine.
# Initial image, courtesy of 0. Lordereau, Dept of Physics, Rennes University).

## SCRIPT ######################################################################
# Importing mamba.
from mamba import *
import mambaDisplay

# The area labelling procedure is defined.
def areaLabelling(imIn, imOut):
    """
    Labelling of each particle of the binary image 'imIn' with the value of its
    area. The result is put is the 32-bit image 'imOut'.
    """
    
    # Working images.
    imWrk1 = imageMb(imIn, 32)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn, 8)
    imWrk4 = imageMb(imIn, 8)
    imWrk5 = imageMb(imIn, 8)
    imWrk6 = imageMb(imIn, 32)
    
    # Output image is emptied.
    imOut.reset()
    # Labelling the initial image.
    nbParticles = label(imIn, imWrk1)
    # Defining output LUTs.
    outLuts = [[0 for i in range(256)] for i in range(4)]
    while nbParticles > 0:
        # particles with labels between 1 and 255 are extracted.
        threshold(imWrk1, imWrk2, 0, 255)
        convert(imWrk2, imWrk3)
        copyBytePlane(imWrk1, 0, imWrk4)
        logic(imWrk3, imWrk4, imWrk3, "inf")
        # The histogram is computed.
        histo = getHistogram(imWrk3)
        # The same operation is performed for the 255 particles. 
        for i in range(1, 256):
            # The area of each particle is obtained from the histogram.
            value = histo[i]
            j = 3
            # The area value is splitted in powers of 256 and stored in the four 
            # output LUTs.
            while j >= 0:
                n = 2 ** (8 * j)
                outLuts[j][i] = value / n
                value = value % n
                j -= 1
        # each LUT is used to label each byte plane of a temporary image with the
        # corresponding value.
        for i in range(4):
            lookup(imWrk3, imWrk5, outLuts[i])
            copyBytePlane(imWrk5, i, imWrk6)
        # The intermediary result is accumulated in the final image.
        logic(imOut, imWrk6, imOut, "sup")
        # 255 is subtracted from the initial labelled image in order to process
        # the next 255 particles.
        floorSubConst(imWrk1, 255, imWrk1)
        nbParticles -= 255

# This operator is applied to an image of bubbles.
# Reading and converting the initial image.
imA = imageMb('binary_foam.png')
imA.convert(1)

# Result image.
imB = imageMb(imA, 32)

# Labelling by area.
areaLabelling(imA, imB)

# Normalizing the final result in the range (0, 255)
# to be able to display it in a greyscale image (it's
# just a trick..).
imC = imageMb(imA, 32)
imD = imageMb(imA, 8)
# The maximum area is 2067 (determined by computeRange).
# So, a division by 9 is sufficient.
divConst(imB, 9, imC)
copyBytePlane(imC, 0, imD)
# Saving the result.
imD.save('area_labelling.png', palette=mambaDisplay.getPalette("rainbow"))
 
