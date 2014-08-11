# exampleM8.py
# IN particles.png
# OUT first_particle.png

## TITLE #######################################################################
# Extraction of the first particle

## DESCRIPTION #################################################################
# Extraction of the first particle (in scanning order) of a binary image.

## SCRIPT ######################################################################
# Importing mamba
import mamba

def firstParticle(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Extraction of the first particle (in scanning order) of binary image imIn.
    The particle is put into image imOut and removed from imIn.
    
    If imIn is empty, imOut is also empty.
    imIn and imOut must be different.
    """

    imWrk = mamba.imageMb(imIn)
    mamba.compare(imIn, imWrk, imWrk)
    mamba.build(imIn, imWrk, grid=grid)
    mamba.diff(imIn, imWrk, imIn)
    mamba.copy(imWrk, imOut) 
    
im = mamba.imageMb("particles.png", 1)
imFP = mamba.imageMb(im)
firstParticle(im, imFP)
imFP.save("first_particle.png")

