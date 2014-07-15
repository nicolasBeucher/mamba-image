# exampleE1.py
# IN snake.png

## TITLE #######################################################################
# Opening and creating images

## DESCRIPTION #################################################################
# This example shows various ways to open or create image using the constructor
# of the imageMb class. This example is meant to be replayed inside a Python
# console. If you run this script directly, nothing will happen.

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *

# Opening an existing image (will be greyscale, 8-bit)
im1 = imageMb('snake.png')
# Creating a 8-bit image with the same size
im2 = imageMb(im1, 8)
# Then a binary image (still same size)
im3 = imageMb(im1, 1)
# And a 32-bit image (same size but do I need to be more specific ?)
im4 = imageMb(im1, 32)

# Opening an existing image but as binary image
im5 = imageMb('snake.png', 1)
# or as a 32-bit image
im6 = imageMb('snake.png', 32)
# For the last two examples, this might not be pertinent because of the 
# properties of the example image.

# Creating an image with a specified size
im7 = imageMb(200, 340)
# In this example, the created image will have a corrected size of 256x340.

# Creating an image without option
im8 = imageMb()
# im8 is now a greyscale image (8-bit) of size 256x256. These are the default
# values when they are not overriden in the constructor.

# Images are automatically garbage collected by Python once there is no more
# reference pointing to it.
