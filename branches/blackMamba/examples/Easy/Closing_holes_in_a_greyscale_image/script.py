# exampleE13.py
# IN alumina.png
# OUT filtered_alumina.png

## TITLE #######################################################################
# Closing holes in a grey scale image

## DESCRIPTION #################################################################
# This simple example shows that the holes closing procedure can be applied on a
# grey scale image without any problem. A hole is simply a region in the image
# surrounded by brighter pixels. In this example, the operator is used to clean
# an alumina grains image by removing the white inclusions inside the grains.

## SCRIPT ######################################################################
# Importing the mamba and mambComposed modules
from mamba import *

# Opening the initial image.
im = imageMb('alumina.png')

# Inverting the image (so that inclusions really correspond to holes).
negate(im, im)

# Applying the holes closing operator (note that the result can be stored in
# same image.
closeHoles(im, im)

# Inverting the image again.
negate(im, im)

# And saving the result.
im.save("filtered_alumina.png")
