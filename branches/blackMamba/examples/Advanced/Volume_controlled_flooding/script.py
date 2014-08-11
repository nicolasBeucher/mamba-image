# exampleA7.py
# OUT flood.png

## TITLE #######################################################################
# Volume controlled flooding

## DESCRIPTION #################################################################
# Watershed operators in Mamba can be used to compute flooding effects on
# Digital Elevation Model (DEM). In this example, we show how to create a volume
# controlled flooding operator. This is a very brutal approach as the low-level
# operators found in Mamba are controlled by water level rather than volume.
# This example also uses a DEM file that you can found at 
# http://www.mapmart.com/samples.aspx (NED 10 meter).

## SCRIPT ######################################################################
# Importing mamba and associates
from mamba import *
import mambaDisplay

def downscale(imIn, imOut):
    # Reuse from previous example
    imWrk = imageMb(imIn)
    (mi, ma) = computeRange(imIn)
    subConst(imIn, mi, imWrk)
    mulConst(imWrk, 255, imWrk)
    divConst(imWrk, ma-mi, imWrk)
    copyBytePlane(imWrk, 0, imOut)

def computeFloodVolume(imDEM, imFloodArea):
    """
    Computes and returns the volume of *water* needed to flood completely
    the area described by 'imFloodArea' in image 'imDEM'.
    """
    imWrk1 = imageMb(imDEM)
    imWrk2 = imageMb(imDEM)
    mul(imDEM, imFloodArea, imWrk1)
    (mi, ma) = computeRange(imWrk1)
    imWrk2.fill(ma)
    mul(imWrk2, imFloodArea, imWrk2)
    sub(imWrk2, imWrk1, imWrk1)
    return computeVolume(imWrk1)
    
def volumeControlledFlood(imDEM, imFlood, targetVolume, grid=DEFAULT_GRID):
    """
    This computes the flood area in imDEM given a certain amount of water
    as given by 'targetVolume'. The flood starting point must be given
    in 'imFlood'. This image will also contains the resulting flooded
    area. The function returns the level reached by water and the actual
    volume needed to perform the flood (greater or equal to targetVolume).
    """
    imWrk1 = imageMb(imFlood)
    imWrk2 = imageMb(imFlood, 1) # will be used to represent the flooded area
    
    (mi, ma) = computeRange(imDEM)
    (mit, mat) = computeRange(imFlood)
    
    # First we check if the targetVolume will flood the
    # maximum level. In this case the flooded area is the whole image
    imWrk2.fill(1)
    vol = computeFloodVolume(imDEM, imWrk2)
    if vol<targetVolume:
        # A complete flooding is not sufficient to reach
        # target volume. We stop here and return the maximum level
        # and the associated volume
        return (ma+1, vol)
    
    # Using a dichotomy approach, we determine the level for which 
    # the flood volume becomes equal or greater to target volume.
    inc = 100
    level = mi
    vol = 0
    while inc>0:
        while vol<targetVolume and level<ma+1:
            copy(imFlood, imWrk1)
            basinSegment(imDEM, imWrk1, max_level=level, grid=grid)
            threshold(imWrk1, imWrk2, 1, mat+1)
            vol = computeFloodVolume(imDEM, imWrk2)
            # next level
            level += inc
        # Changing the level to the previous level for which the flood volume
        # was below the target volume
        level -= 2*inc
        # Decreasing increment for better precision
        inc = inc/10
    
    copy(imWrk1, imFlood)
    return (level+2, vol)

imDEM = imageMb("NED10Meter.tif")
imFlood = imageMb(imDEM)

# Our flood starting point
imFlood.setPixel(255, (1337,81))

# Computing the flood area, level and actual volume needed to reach
# it with a control volume of 20000000. This is not of course a 'real'
# volume but you can compute its actual physical meaning if you have all
# the information regarding your DEM (such as grid resolution and pixel
# value metrics). Here we picked a SQUARE grid because it is most
# likely going to represent the grid used in the DEM.
print(volumeControlledFlood(imDEM, imFlood, 20000000, grid=SQUARE))

# Displaying the result
imDEM_8 = imageMb(imDEM, 8)
imFlood_8 = imageMb(imDEM, 8)
downscale(imDEM,imDEM_8)
copyBytePlane(imFlood, 0, imFlood_8)
logic(imDEM_8, imFlood_8, imDEM_8, "sup")
name = mambaDisplay.tagOneColorPalette(255,(0,100,255))
imDEM_8.save("flood.png", palette=mambaDisplay.getPalette(name))
