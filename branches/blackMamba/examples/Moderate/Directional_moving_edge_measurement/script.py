# exampleM7.py
# IN tennis/001.png tennis/002.png tennis/003.png
# OUT mcm_d1_n1.png mcm_d1_n10.png mcm_d3_n1.png

## TITLE #######################################################################
# Directional moving edge measurement

## DESCRIPTION #################################################################
# This example implements a directional MEM algorithm (also called T-Rex
# vision). This allows to identify the movement in a sequence of images
# using their gradients. Among other things, this example shows how to use
# sequenceMb. You can find a description of this algorithm in 
# http://cmm.ensmp.fr/~beucher/publi/Ibpria_camera_ready.pdf.

## SCRIPT ######################################################################
# Importing mamba and mamba3D
from mamba3D import *
from mamba import *
import mambaDisplay
    
def dirMEM(seqIn, imOut, d, n=1, grid=DEFAULT_GRID):
    """
    Directional MEM algorithm. This algorithm will indicates the
    boundaries of objects moving in the direction 'd'. To work it needs
    a sequence 'seqIn' with at least three images in it.
    """
    grad0 = imageMb(seqIn[0])
    grad1 = imageMb(seqIn[0])
    grad2 = imageMb(seqIn[0])
    imWrk1 = imageMb(seqIn[0])
    imWrk2 = imageMb(seqIn[0])
    
    # direction d converted into a structuring element
    sed = structuringElement([0,d], grid)
    
    # Computing the gradients of the first three images of the sequence
    halfGradient(seqIn[0], grad0, n=n, se=sed)
    halfGradient(seqIn[1], grad1, n=n, se=sed)
    halfGradient(seqIn[2], grad2, n=n, se=sed)

    # First we compute the absolute difference between the first two
    # gradients
    sub(grad0, grad1, imWrk1)
    sub(grad1, grad0, imWrk2)
    logic(imWrk1, imWrk2, imOut, "sup") # imOut = abs(grad1-grad0)
    # Then we compute the absolute difference between the last two
    # gradients
    sub(grad2, grad1, imWrk1)
    sub(grad1, grad2, imWrk2)
    logic(imWrk1, imWrk2, imWrk1, "sup") # imWrk1 = abs(grad1-grad0)
    
    # And last imOut is set to the inf of this two differences
    logic(imOut, imWrk1, imOut, "inf")
    
seq = sequenceMb("tennis")
im = imageMb(seq[0])

# Testing it with various direction and size
dirMEM(seq, im, d=1, n=1, grid=SQUARE)
im.save("mcm_d1_n1.png", palette=mambaDisplay.getPalette("rainbow"))
dirMEM(seq, im, d=1, n=10, grid=SQUARE)
im.save("mcm_d1_n10.png", palette=mambaDisplay.getPalette("rainbow"))
dirMEM(seq, im, d=3, n=1, grid=SQUARE)
im.save("mcm_d3_n1.png", palette=mambaDisplay.getPalette("rainbow"))

