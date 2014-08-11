# exampleM21.py
# IN seismic_section.png
# OUT gradient_modulus.png gradient_azimut.png 

## TITLE #######################################################################
# Modulus and azimut of a directional gradient

## DESCRIPTION #################################################################
# This example uses the linear operators defined in example M20 to compute a
# morphological gradient modulus and its azimut function. Directional gradients
# are calculated and the modulus corresponds to the supremum of all these
# directional gradients. The azimut corresponds to the direction where this
# supremum occurs. This example has been designed on the hexagonal grid but it
# could be adapted to the square grid without any difficulty.

## SCRIPT ######################################################################
# Importing mamba
import mamba
import mambaDisplay

# Operators defined in example M20 are duplicated here.
def conjugateDirectionalErode(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs the erosion of image 'imIn' in the conjugate direction 'd' of the
    grid and puts the result in image 'imOut'. The images can be binary, greyscale
    or 32-bit images. 'size' is a multiple of the distance between two adjacent
    points in the conjugate directions. 'edge' is set to FILLED by default (can
    be changed).
    Note that this operator is not equivalent to successive erosions by a doublet
    of points.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)

    j3 = mamba.transposeDirection(d, grid=grid)
    j2 = mamba.rotateDirection(d, grid=grid)
    j1 = mamba.transposeDirection(j2, grid=grid)
    val = mamba.computeMaxRange(imIn)[1] * int(edge == mamba.FILLED)
    for i in range(size):
        mamba.copy(imOut, imWrk1)
        mamba.copy(imOut, imWrk2)
        mamba.linearErode(imWrk1, imWrk1, d, n=1, grid=grid, edge=edge)
        mamba.shift(imWrk1, imWrk1, j1, 1, val, grid=grid)
        mamba.logic(imWrk1, imOut, imWrk1, "inf")
        mamba.linearErode(imWrk2, imWrk2, j2, n=1, grid=grid, edge=edge)
        mamba.shift(imWrk2, imWrk2, j3, 1, val, grid=grid)
        mamba.logic(imWrk2, imOut, imWrk2, "inf")
        mamba.logic(imWrk1, imWrk2, imOut, "sup")
    
def directionalErode(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    General directional erosion of image 'imIn', result in 'imOut'. The images
    can have any format. The direction 'd' is coded clockwise from 1 to 12 or
    16. Direction 1 corresponds to 60 degrees on the hexagonal grid and 90
    degrees on the square grid. 'size' corresponds to twice the normal size
    when standard directions are used. 'edge' is set to FILLED by default.
    """
    
    if (d & 1) == 0:
        conjugateDirectionalErode(imIn, imOut, d/2, size, grid=grid, edge=edge)
    else:
        mamba.linearErode(imIn, imOut, (d+1)/2, size*2, grid=grid, edge=edge) 

# similar operators are defined for the dilation.
def conjugateDirectionalDilate(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Performs the dilation of image 'imIn' in the conjugate direction 'd' of the
    grid and puts the result in image 'imOut'. The images can be binary, greyscale
    or 32-bit images. 'size' is a multiple of the distance between two adjacent
    points in the conjugate directions. 'edge' is set to EMPTY by default (can
    be changed).
    Note that the linear structuring element is not connected. Points connecting
    adjacent points in the conjugate directions are not present. This is normal
    if we want to insure that the result is identical when we iterate n size 1
    operations to get a size n one (the same remark applies to the erosion).
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    
    j3 = mamba.transposeDirection(d, grid=grid)
    j2 = mamba.rotateDirection(d, grid=grid)
    j1 = mamba.transposeDirection(j2, grid=grid)
    val = mamba.computeMaxRange(imIn)[1] * int(edge == mamba.FILLED)
    for i in range(size):
        mamba.copy(imOut, imWrk1)
        mamba.copy(imOut, imWrk2)
        mamba.linearDilate(imWrk1, imWrk1, d, 1, grid=grid, edge=edge)
        mamba.shift(imWrk1, imWrk1, j1, 1, val, grid=grid)
        mamba.logic(imWrk1, imOut, imWrk1, "sup")
        mamba.linearDilate(imWrk2, imWrk2, j2, 1, grid=grid, edge=edge)
        mamba.shift(imWrk2, imWrk2, j3, 1, val, grid=grid)
        mamba.logic(imWrk2, imOut, imWrk2, "sup")
        mamba.logic(imWrk1, imWrk2, imOut, "inf")
    
def directionalDilate(imIn, imOut, d, size, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    General directional dilation of image 'imIn', result in 'imOut'. The images
    can have any format. The direction 'd' is coded clockwise from 1 to 12 or
    16. Direction 1 corresponds to 60 degrees on the hexagonal grid and 90
    degrees on the square grid. 'size' corresponds to twice the normal size
    when standard directions are used. 'edge' is set to EMPTY by default.
    """
    
    if (d & 1) == 0:
        conjugateDirectionalDilate(imIn, imOut, d/2, size, grid=grid, edge=edge)
    else:
        mamba.linearDilate(imIn, imOut, (d+1)/2, size*2, grid=grid, edge=edge) 

# We define the vectorial gradient procedure.
def vectorGradient(imIn, imModul, imAzim, size=1):
    """
    Computes modulus (result in 'imModul') and azimut (in 'imAzim') of image
    'imIn'. The 'size' of each directional gradient is set to 1 by default.
    This operator is defined on the hexagonal grid (12 directions are used).
    Note that this operator belongs to the residual operators class.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    imWrk3 = mamba.imageMb(imIn)
    imWrk4 = mamba.imageMb(imIn, 1)
    
    mamba.copy(imIn, imWrk1)
    imModul.reset()
    imAzim.reset()
    for i in range(12):
        d = i + 1
        # Directional gradient obtained with linear erosions and dilations.
        directionalDilate(imWrk1, imWrk2, d, size)
        directionalErode(imWrk1, imWrk3, d, size)
        mamba.sub(imWrk2, imWrk3, imWrk2)
        # For each direction, maximal pixels are indexed in a mask image.
        mamba.generateSupMask(imWrk2, imModul, imWrk4, True)
        mamba.convertByMask(imWrk4, imWrk3, 0, d)
        # Modulus and azimut are calculated.
        mamba.logic(imWrk2, imModul, imModul, "sup")
        mamba.logic(imWrk3, imAzim, imAzim, "sup")
        
# Using this operator on a seismic section image.

# Reading the initial image and defining results images.
imA = mamba.imageMb('seismic_section.png')
imB = mamba.imageMb(imA)
imC = mamba.imageMb(imA)

# Calculating the vectorial gradient. 
vectorGradient(imA, imB, imC)

# A palette for displaying the 12 possible directions is defined.
dirpal = (0, 0, 0, 255, 0, 0, 255, 128, 0, 255, 255, 0, 128, 255, 0, 0, 255, 0)
dirpal += (0, 255, 128, 0, 255, 255, 0, 128, 255, 0, 0, 255)
dirpal += (128, 0, 255, 255, 0, 255, 255, 0, 128)
dirpal += 243 * (0, 0, 0)
mambaDisplay.addPalette("direction palette", dirpal)

# Saving the results.
# Applying the new palette to the azimut image (and the classical
# rainbow palette to the modulus).
imB.save('gradient_modulus.png', palette=mambaDisplay.getPalette("rainbow"))
imC.save('gradient_azimut.png', palette=mambaDisplay.getPalette("direction palette"))
# The last line could have been
# imC.save('gradient_azimut.png', palette=dirpal)
