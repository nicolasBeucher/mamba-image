# exampleA8.py
# IN is-paris-burning.jpg
# OUT filter-text.png

## TITLE #######################################################################
# Embedded text filtering

## DESCRIPTION #################################################################
# Image indexation is quite a complex job. Being able to find text in an
# image may help categorize it. This example implements a very simple
# filtering algorithm that makes text stands out. If you are interested
# in the subject, visit http://cmm.ensmp.fr/~marcoteg/ImagEval.htm.

## SCRIPT ######################################################################
# Importing mamba and associates
from mamba import *

def textFiltering(imIn, imOut, textSize=16, textDir="HORZ"):
    """
    Filters image 'imIn' so that text comes out more brillant in 'imOut'.
    The text size inside the image must be identified with 'textSize', default
    value is 16. The direction of the text is given with 'textDir', possible
    values are "HORZ" for horizontal text or "VERT" for vertical text.
    """
    imWrk1 = imageMb(imIn)
    imWrk32 = imageMb(imIn, 32)
    imWrkb = imageMb(imIn, 1)
    
    if textDir=="VERT":
        dir1 = structuringElement([0,1], SQUARE)
    else:
        dir1 = structuringElement([0,3], SQUARE)
        
    ultimateOpening(imIn, imWrk1, imWrk32)
    whiteTopHat(imWrk32, imWrk32, textSize)
    closing(imWrk32, imWrk32, textSize*2, dir1)
    opening(imWrk32, imWrk32, textSize*10, dir1)
    closeHoles(imWrk32, imWrk32)
    threshold(imWrk32, imWrkb, 1, 0xffffffff)
    mul(imIn, imWrkb, imOut)
    
im = imageMb("is-paris-burning.jpg")
imText = imageMb(im)

textFiltering(im, imText, textSize=8)

imText.save("filter-text.png")
