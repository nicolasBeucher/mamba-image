# exampleA14.py
# IN motor1.png motor2.png
# OUT motor1_check.png motor2_check.png

## TITLE #######################################################################
# Quality control of a clutch device

## DESCRIPTION #################################################################
# This example explains how a clutch device can be checked by computer vision.
# Two pieces are controlled in the process: a star-shaped spring at the center
# of the device and a seal surrounding the casing. The first one can be damaged
# (missing branches) and the second one can be missing. This example shows how
# the regions where these pieces are supposed to be can be emphasized by a
# geometrical and topological approach.

## SCRIPT ######################################################################
# Importing mamba
from mamba import *

# The main checking routine.
def checkClutch(imIn, springBranches, sealZone):
    """
    this operator checks the spring and the seal of a clutch device in 'imIn'.
    'springBranches' contains the branches of the spring which have been
    detected and 'sealZone' contains the region where the seal should be. This
    latter image is empty if the seal is present.
    This procedure returns a 2-item 'check' list. 'check[0]' indicates if the 
    spring is OK (1) or not (0). 'check[1]' indicates if the seal is missing (0)
    or not (1).
    """
    
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn, 1)
    imWrk4 = imageMb(imIn,1)
    imWrk5 = imageMb(imIn, 1)
    imWrk6 = imageMb(imIn, 1)
    imWrk7 = imageMb(imIn)
    check = [0, 0]
    # The initial image is filtered.
    buildClose(imIn, imWrk1, 2)
    buildOpen(imWrk1, imWrk1, 2)
    # copy for latter use.
    copy(imWrk1, imWrk7)
    # Firstly, we check the spring.
    # Parts of the casing touching the edges are removed.
    removeEdgeParticles(imWrk1, imWrk1)
    # The center region of the clutch is extracted.
    closeHoles(imWrk1, imWrk2)
    sub(imWrk2, imWrk1, imWrk2)  
    # The central region is extracted by an opening by reconstruction.
    threshold(imWrk2, imWrk3, 10, 255)
    buildOpen(imWrk3, imWrk4, 20)
    # Looking for the branches of the spring. Firstly, the spaces between
    # the branches are extracted.    
    dilate(imWrk4, imWrk5, 15)
    logic(imWrk3, imWrk5, imWrk6, "inf")
    dilate(imWrk6, imWrk3, 10)
    diff(imWrk5, imWrk3, imWrk5)
    logic(imWrk5, imWrk6, imWrk5, "sup")
    # The center region and 7 spaces between the branches should appear
    # if the spring is correct.
    check[0] = (computeConnectivityNumber(imWrk5) == 8)
    # This part of the procedure is just here to generate a binary image
    # showing the junctions of the different branches of the spring (not
    # necessary for the checking). These junctions correspond to multiple
    # points of the SKIZ of the previous image.
    fastSKIZ(imWrk5, imWrk5)
    negate(imWrk5, imWrk5)
    multiplePoints(imWrk5, imWrk5)
    removeEdgeParticles(imWrk5, imWrk5)
    # Eachmultiple point is reduced to a single point by thinning.
    thinD(imWrk5, springBranches)
    # The junctions are surrounded by a circle for a better view.
    dodecagonalDilate(springBranches, imWrk5, 9)
    dilate(imWrk5, springBranches, 2)
    diff(springBranches, imWrk5, springBranches)
    dilate(springBranches, springBranches)
    #
    # Secondly, the seal is checked.
    # The region of the image where the seal should be is generated from the
    # central region extracted above.
    dodecagonalDilate(imWrk4, imWrk5, 45)
    dodecagonalDilate(imWrk5, imWrk6, 30)
    diff(imWrk6, imWrk5, imWrk5)
    convert(imWrk5, imWrk2)
    # The corresponding region in the initial filtered image is selected.
    logic(imWrk7, imWrk2, imWrk7, "inf")
    # A black Top-Hat operator is applied (should emphasize the seal location
    # if missing.
    blackTopHat(imWrk7, imWrk2, 5)
    # The result is thresholded (a more robust threshold when applied to a
    # Top-Hat transform).
    threshold(imWrk2, imWrk3, 15, 255)
    # The binary image is cleaned (small holes filled).
    buildClose(imWrk3, imWrk3)
    # A SKIZ indicates if the seal is missing.
    negate(imWrk3, imWrk3)
    fastSKIZ(imWrk3, sealZone)
    negate(sealZone, sealZone)
    # The missing seal location is emphasized for display.
    dilate(sealZone, sealZone)
    # If the seal is missing, the sealZone image is not empty.
    check[1] = (computeVolume(sealZone) == 0)
    return check
    
# Reading the first image.
im1 = imageMb('motor1.png')

# Defining result images
spring = imageMb(im1, 1)
seal = imageMb(im1, 1)

# Checking the clutch.
check = checkClutch(im1, spring, seal)
# Printing the result and setting the color of the spring branches locations:
# green, all the branches are here, red, some branches are missing.
print("First image checking:")
if check[0]:
    print("Spring is OK.")
    pal1 = (0, 255, 0)
else:
    print("Spring is defective.")
    pal1 = (255, 0, 0)
if check[1]:
    print("Seal is OK.")
    pal2 = (0, 255, 0)
else:
    print("Seal is missing.")
    pal2 = (255, 0, 0)
# Superposing the seal and spring locations to the original image and saving
# the result.
multiSuperpose(im1, seal, spring)
pal = ()
for i in range(254):
    pal += (i,i,i)
pal += pal2
pal += pal1
im1.save('motor1_check.png', palette=pal)

# Reading the next image.
im1 = imageMb('motor2.png')

# Resetting the result images
spring.reset()
seal.reset()

# Checking it.
check = checkClutch(im1, spring, seal)
print("Second image checking:")
if check[0]:
    print("Spring is OK.")
    pal1 = (0, 255, 0)
else:
    print("Spring is defective.")
    pal1 = (255, 0, 0)
if check[1]:
    print("Seal is OK.")
    pal2 = (0, 255, 0)
else:
    print("Seal is missing.")
    pal2 = (255, 0, 0)
# Storing the resulting images.
multiSuperpose(im1, seal, spring)
pal = ()
for i in range(254):
    pal += (i,i,i)
pal += pal2
pal += pal1
im1.save('motor2_check.png', palette=pal)

