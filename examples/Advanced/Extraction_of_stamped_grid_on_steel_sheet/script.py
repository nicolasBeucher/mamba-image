# exampleA13.py
# IN steel_sheet.png
# OUT grid_image.png grid_crossings.png grid_result.png

## TITLE #######################################################################
# Extraction of a stamped grid on a steel sheet

## DESCRIPTION #################################################################
# A regular grid has been printed on a steel sheet before its stamping.
# This example shows how the crossing points of this grid after stamping can be
# extracted. The new position of each point indicates its displacement during
# stamping and therefore the degree of stress exerted locally on the steel sheet.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

# The markers of the grid cells are extracted by successive filterings. 
def extractMarkers(imIn, imOut):
    """
    This procedure extracts markers of the cells of the printed grid in image
    'imIn' and puts the result in binary image 'imOut'.
    
    """
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn, 1)
    # A first filtering with a strong levelling produces first seeds for the
    # markers (maxima of the filtered image).
    strongLevelling(imIn, imWrk1, 2, eroFirst=False)
    maxima(imWrk1, imOut)
    # The same filtering is iterated for increasing sizes. Only the inner
    # maxima are preserved and added to the markers image.
    for i in range(4, 16, 2):
        strongLevelling(imIn, imWrk1, i, eroFirst=False)
        maxima(imWrk1, imWrk2)
        removeEdgeParticles(imWrk2, imWrk2)
        logic(imWrk2, imOut, imOut, "sup")

# Reading the image.
im1 = imageMb('steel_sheet.png')
# Defining working images.
imWrk1 = imageMb(im1, 1)
imWrk2 = imageMb(im1)
imWrk3 = imageMb(im1, 32)
imWrk4 = imageMb(im1, 1)
imWrk5 = imageMb(im1, 1)
imWrk6 = imageMb(im1, 1)
crossings = imageMb(im1, 1)

# Extracting the markers of the cells in the image.
extractMarkers(im1, imWrk1)
# Performing the marker-controlled watershed transform of the inverted
# initial image.
negate(im1, imWrk2)
label(imWrk1, imWrk3)
watershedSegment(imWrk2, imWrk3)
copyBytePlane(imWrk3, 3, imWrk2)
threshold(imWrk2, imWrk1, 1, 255)
# Saving the grid image.
imWrk1.save('grid_image.png')
# Crossing points extraction.
multiplePoints(imWrk1, imWrk4)
dilate(imWrk4, imWrk4, 2)
# The crossing points which are not at the intersection of 4 cells
# are removed. This procedure is applied separately on each dot.
negate(imWrk1, imWrk1)
while computeVolume(imWrk4) != 0:
    imWrk5.reset()
    p = compare(imWrk4, imWrk5, imWrk5)
    build(imWrk4, imWrk5)
    dilate(imWrk5, imWrk6)
    diff(imWrk6, imWrk5, imWrk6)
    logic(imWrk6, imWrk1, imWrk6, "inf")
    if computeConnectivityNumber(imWrk6) == 4:
        logic(imWrk5, crossings, crossings, "sup")  
    diff(imWrk4, imWrk5, imWrk4)
# The remaining dots are reduced to a point and slightly dilated (for
# a better view).
thinD(crossings, crossings)
dilate(crossings, crossings, 3)
# The result is saved.
crossings.save('grid_crossings.png')

# Superposing the various results to the original image and saving the result.
negate(imWrk1, imWrk1)
multiSuperpose(im1, imWrk1, crossings)
pal = ()
for i in range(254):
    pal += (i,i,i)
pal += (255,0,0)
pal += (0,255,0)
im1.save('grid_result.png', palette=pal)

