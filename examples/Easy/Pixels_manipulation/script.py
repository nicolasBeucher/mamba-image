# exampleE5.py
# OUT pixels.png

## TITLE #######################################################################
# Pixels manipulation

## DESCRIPTION #################################################################
# In this example, we use the pixels manipulation methods.

## SCRIPT ######################################################################
# Importing the mamba module
from mamba import *

# Creating a default image, 256x256 8-bit image
im = imageMb()

# Setting the pixel at (128,128) to value 50
im.setPixel(50, (128,128))
# Getting the pixel value at the same position
print(im.getPixel((128,128)))

# When trying to access a pixel outside image boundary an exception is raised
try:
    im.getPixel((256,256)) # position start at 0 to width-1 or height-1
except MambaError:
    print("error catch")

# The two methods to set a pixel vary on one aspect: the display update
im.show()
im.setPixel(255, (10,10)) # <- Pixel is set and visible in display
im.fastSetPixel(255, (20,20)) # <- Pixel is set but not visible
im.update() # Now it is

