# exampleE14.py
# IN galaxy.png
# OUT cropped_galaxy.png

## TITLE #######################################################################
# Cropping and copying images

## DESCRIPTION #################################################################
#   The cropCopy operator is very useful to modify the size of an image, to
# select regions of interest or to compose a new image by assembling elements
# coming from other images. In this example, this operator is simply used to
# reduce the size of the image as most of it is black and without interest.
# The image used in this example comes from the Galaxy Zoo web site. This site
# allows you to contribute to the classification of galaxies. Visit it at:
# http://www.galaxyzoo.org.

## SCRIPT ######################################################################
# Importing the mamba and mambComposed modules
from mamba import *

# Opening the initial image.
imA = imageMb('galaxy.png')

# The galaxy visible in the image can be easily contained in a 256x256 image.
# The center of the galaxy is located at image coordinates (253, 256).
# Therefore, we calculate the initial position (upper left corner) of the 
# cropping window (x = 253 - 128 and y = 256 - 128).
posin = (125, 128)

# Then we define a new image of size 256x256.
imB = imageMb(256, 256)

# We crop and copy the initial image into the new one.
cropCopy(imA, posin, imB, (0, 0), (256, 256))

# Then, we save the new image.
imB.save("cropped_galaxy.png")
