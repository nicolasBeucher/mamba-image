# exampleM11.py
# IN lena_noisy.png
# OUT lena_FAF.png lena_FBAF.png

## TITLE #######################################################################
# Noise reduction using alternate filters

## DESCRIPTION #################################################################
# This example introduces a new full alternate filter based on 
# buildOpen and buildClose operators. The new filter reduces efficiently
# noise while producing a much less fuzzy image than the classic full
# alternate filter.

## SCRIPT ######################################################################
# Importing mamba
import mamba

def fullBuildAlternateFilter(imIn, imOut, n, openFirst, se=mamba.DEFAULT_SE):
    """
    Performs a full alternate filter operation (successive alternate filters of
    increasing sizes, from 1 to 'n') on image 'imIn' and puts the result 
    in 'imOut'. 'n' controls the filter size. If 'openFirst' is True, the filter
    begins with an opening, a closing otherwise. This operator uses the
    buildOpen and buildClose operators instead of the classic open and close.
    """
    
    mamba.copy(imIn, imOut)
    for i in range(1,n+1):
        if openFirst:
            mamba.buildOpen(imOut, imOut, i, se=se)
            mamba.buildClose(imOut, imOut, i, se=se)
        else:
            mamba.buildClose(imOut, imOut, i, se=se)
            mamba.buildOpen(imOut, imOut, i, se=se)
    
im = mamba.imageMb("lena_noisy.png")
imFilter = mamba.imageMb(im)

# First we compute the result of the standard full alternate filter
# on the noisy lena image
mamba.fullAlternateFilter(im, imFilter, 3, True)
imFilter.save("lena_FAF.png")
# Then we compute the result of the reconstruction based full alternate filter
# on the noisy lena image
fullBuildAlternateFilter(im, imFilter, 3, True)
imFilter.save("lena_FBAF.png")


