# exampleM16.py
# IN retina.png
# OUT aneurisms.png

## TITLE #######################################################################
# Simple and coarse extraction of micro-aneurisms in retina

## DESCRIPTION #################################################################
# Micro-aneurisms are abnormal inflations of blood vessels in the retina (eye
# fundus). They appear as white dots in the retina image. This example shows a 
# simple extraction technique based on a Top-Hat transform built with linear
# openings and geodesic reconstructions.

## SCRIPT ######################################################################
# Importing the mamba modules
from mamba import *
import mambaDisplay

# Top-hat operator built with linear openings and a geodesic reconstruction.
def buildSupWhiteTopHat(imIn, imOut, size):
    """
    Top-hat operator applied on image 'imIn' obtained by a supremum of linear
    openings of size 'size' and a reconstruction. The result is put in 'imOut'.
    This operator extracts white objects with a thickness less than 2*'size'
    in all directions.
    """
    imWrk = imageMb(imIn)
    supOpen(imIn, imWrk, size)
    build(imIn, imWrk)
    sub(imIn, imWrk, imOut)

# Reading the initial image. 
imIn = imageMb('retina.png')

# Working image and result image.
imWrk = imageMb(imIn)
aneurisms = imageMb(imIn, 1)

# Extraction of aneurisms.
buildSupWhiteTopHat(imIn, imWrk, 10)
# Thresholding of the image (the value of the threshold is half the maximum
# grey value in the top-hat image.
t = computeRange(imWrk)[1]/2
threshold(imWrk, aneurisms, t, 255)

# Superposing the result to the original image and saving the result.
multiSuperpose(imIn, aneurisms)
name = mambaDisplay.tagOneColorPalette(255, (255,0,0))
imIn.save('aneurisms.png', palette=mambaDisplay.getPalette(name))

