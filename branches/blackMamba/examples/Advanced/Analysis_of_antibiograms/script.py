# exampleA12.py
# IN antibio1.png antibio2.png
# OUT anti1_result.png anti2_result.png

## TITLE #######################################################################
# Analysis of antibiograms

## DESCRIPTION #################################################################
# Antibiograms are a methodology used to determine the efficiency of 
# various antibiotics against a specific bacteria. In a Petri dish where the
# bacteria has been cultivated, some discs containing antibiotics are
# scattered on. After a few days, some halos appear around the discs.
# The halo radius is a direct measurement of the antibiotics efficiency
# against the bacteria. The purpose of this example is to show how the
# radius of each halo can be determined automatically.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
from PIL import ImageDraw
from PIL import ImageFont

# The antibiotics are incorporated to the Petri dish using discs
# which appear with a certain size on our images
DISC_SIZE = 7

def drawingResults(imIn, results, path):
    """
    This function draws the result of the antibiograms measurement.
    """
    # First looking for the best result
    max_value = 0
    for (x,y,value) in results:
        max_value = max(max_value, value)
    # Now drawing the result
    pilim = Mamba2PIL(imIn).convert("RGB")
    draw = ImageDraw.Draw(pilim)
    font = ImageFont.truetype("FreeMonoBold.ttf", 20)
    for (x,y,value) in results:
        width, height = font.getsize(str(value))
        red = (255*(max_value-value))/max_value
        green = (255*value)/max_value
        color = "rgb(%d,%d,0)" % (red,green)
        r = value+DISC_SIZE
        draw.ellipse((x-r,y-r,x+r,y+r), outline=color)
        draw.text((x, y), str(value), color, font=font)
    pilim.save(path)

# Defining the operator which detects the antibiotics discs and measures the
# halos in the antibiograms images.

def checkAntibiograms(imIn, discCenters, halosRadii):
    """
    This procedure extracts the centers of the antibiotics discs scattered
    in image 'imIn' and puts them in 'discCenters' binary image. The radius
    of the corresponding halo is put in 'halosRadii' 32-bit image (the radii
    could be larger than 255).
    """
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn)
    imWrk4 = imageMb(imIn, 1)
    imWrk5 = imageMb(imIn, 1)
    imWrk6 = imageMb(imIn, 32)

    # We work on a filtered image.
    alternateFilter(imIn, imWrk1, 3, openFirst=False)
    # The discs are removed by erosion (the size of the discs is constant and known).
    erode(imWrk1, imWrk2, DISC_SIZE)
    # A reconstruction gives the grey level of the unaltered microbe culture.
    imWrk3.fill(255)
    build(imWrk3, imWrk2)
    t = computeRange(imWrk2)[1]
    # This intermediary background is subtracted from the initial filtered image.
    sub(imWrk1, imWrk2, imWrk3)
    # The result is thresholded (a threshold equal to 30 is a good value to insure
    # that the noise in the image will not be taken into account).
    threshold(imWrk3, imWrk4, 30, 255)
    # The centers of the discs are built.
    thinD(imWrk4, discCenters)
    # The center points are stored in a 8-bit image.
    convert(discCenters, imWrk2)
    # Building the unaltered part of the antibiogram.
    dilate(imWrk2, imWrk3, 10)
    sub(imWrk1, imWrk3, imWrk3)
    build(imWrk1, imWrk3)
    # This unaltered microbe culture image is thresholded. The
    # threshold value is half its grey value. We obtain the halos.
    threshold(imWrk3, imWrk5, 0, t/2)
    # the distance function of this set is computed.
    computeDistance(imWrk5, imWrk6)
    # The center points are stored in a 32-bit image.
    for i in range(4):
        copyBytePlane(imWrk2, i, halosRadii)
    # They are valued with the radius of their corresponding halo (the size
    # of the disc is subtracted).
    logic(halosRadii, imWrk6, halosRadii, "inf")
    floorSubConst(halosRadii, DISC_SIZE, halosRadii)
    
# Reading the initial image.
im1 = imageMb('antibio1.png')
# Defining working images.
imWrk1 = imageMb(im1, 32)
imWrk2 = imageMb(im1, 1)
imWrk3 = imageMb(im1, 1)

# Processing the image.
checkAntibiograms(im1, imWrk3, imWrk1)
# Each center and its corresponding radius are extracted.
# The radius value is printed in the result image.
results = []
while computeVolume(imWrk3) != 0:
    imWrk2.reset()
    x, y = compare(imWrk3, imWrk2, imWrk2)
    value = imWrk1.getPixel((x, y))
    diff(imWrk3, imWrk2, imWrk3)
    results.append((x,y,value))
# The result is saved.
drawingResults(im1, results, 'anti1_result.png')

# Processing the second image.
im1 = imageMb('antibio2.png')
checkAntibiograms(im1, imWrk3, imWrk1)
results = []
while computeVolume(imWrk3) != 0:
    imWrk2.reset()
    x, y = compare(imWrk3, imWrk2, imWrk2)
    value = imWrk1.getPixel((x, y))
    diff(imWrk3, imWrk2, imWrk3)
    results.append((x,y,value))
# Saving the result.
drawingResults(im1, results, 'anti2_result.png')

