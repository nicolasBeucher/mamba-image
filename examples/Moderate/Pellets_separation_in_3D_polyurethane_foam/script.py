# exampleM17.py
# IN foam3D.png
# OUT segmented_pellets.png

## TITLE #######################################################################
# Pellets separation in a 3D polyurethane foam

## DESCRIPTION #################################################################
# This 3D segmentation example shows that a process which has been designed
# for 2D images can be applied directly to 3D images thanks to availability in
# mamba3D module of operators which are the simple transposition of 2D operators.
# The initial image represents a foam made of polyurethane pellets. However,
# these pellets are so compressed that the separation walls between them have
# disappeared. Only corners at the junction of adjacent pellets are still
# visible. Nevertheless, it is possible to rebuild the separation walls with a
# procedure which is, in 3D, similar, indeed identical, to the approach used to
# segment coffee grains in exampleA2.py (coffee grains separation and counting).

## SCRIPT ######################################################################
# Importing the mamba and mamba3D modules.
from mamba import *
from mamba3D import *

# Importing the initial image and converting it to binary.
imA = image3DMb('foam')
imA.convert(1)
# The initial image is filtered (holes are closed and a reconstruction opening
# is performed to remove small artifacts which could be present in th 3D volume.
imB = image3DMb(imA)
closeHoles3D(imA, imB)
imC = image3DMb(imA)
supOpen3D(imB, imC, 2)
build3D(imB, imC)
# The filtered image is inverted and its 3D distance function is performed.
imD = image3DMb(imA)
negate3D(imC, imD)
imE = image3DMb(imA, 32)
computeDistance3D(imD, imE, edge=FILLED)
# We verify that the maximum distance is less than 256 so that the result can
# be transferred into a greyscale image.
tMax = computeRange3D(imE)[1]
print("maximum size of pellets: %d" % (tMax))
imF = image3DMb(imA, 8)
copyBytePlane3D(imE, 0, imF)
# The distance function is filtered in order to keep its most significant
# maxima (markers of the pellets). Their number gives the number of pellets.
imG = image3DMb(imA, 8)
opening3D(imF, imG, 3)
maxima3D(imG, imB)
# The distance function is inverted.
negate3D(imF, imF)
# labelling the markers and printing the number of pellets.
nbPellets = label3D(imB, imE)
print("Number of polyurethane pellets : %d" % (nbPellets))
# A 3D watershed of the inverted distance function is performed.
watershedSegment3D(imF, imE)
copyBytePlane3D(imE, 3, imG)
imH = image3DMb(imA)
# The watershed is displayed. Watershed surfaces correspond to the separations
# between the pellets.
threshold3D(imG, imH, 0, 0)
imH.show(mode="VOLUME")
