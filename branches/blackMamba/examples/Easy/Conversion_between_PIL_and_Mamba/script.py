# exampleE7.py
# IN colorful.jpg
# OUT colorful_transposed.png

## TITLE #######################################################################
# Conversion between PIL image format and Mamba image format

## DESCRIPTION #################################################################
# This example shows how to convert your Mamba image into a PIL image
# enabling you to use PIL functionnalities and how to convert the result
# back into a Mamba image.
# 
# Image source is
# http://commons.wikimedia.org/wiki/File:Ebenthal_Schlosswirt_20052010_06.jpg.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

# Opening an image and storing it in Mamba format
im = imageMb('colorful.jpg')

# Converting the image in PIL format
pilim = Mamba2PIL(im)

# Doing a bit of computation using the PIL library
pilim = pilim.transpose(Image.FLIP_LEFT_RIGHT)

# Then converting back into mamba format
PIL2Mamba(pilim, im)

# And saving it, notice that color disappeared
im.save("colorful_transposed.png")
