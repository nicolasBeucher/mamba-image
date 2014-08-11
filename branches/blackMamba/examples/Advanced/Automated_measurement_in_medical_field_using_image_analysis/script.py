# exampleA9.py
# IN medical.png
# OUT delaunay.jpg

## TITLE #######################################################################
# Automated measurement in medical field using image analysis

## DESCRIPTION #################################################################
# This example demonstrates how mathematical morphology and Mamba can be
# used to perform relevant automated measurements on medical images. This
# example implements part of the algorithm described in paper
# http://www.diagnosticpathology.org/content/5/1/7. Courtesy of Michel Jondet.

## SCRIPT ######################################################################
# Importing mamba and associates
from mamba import *

# Reusing functions from previous examples
def firstParticle(imIn, imOut, grid=mamba.DEFAULT_GRID):
    imWrk = mamba.imageMb(imIn)
    mamba.compare(imIn, imWrk, imWrk)
    build(imIn, imWrk, grid=grid)
    mamba.diff(imIn, imWrk, imIn)
    mamba.copy(imWrk, imOut) 

def autoThreshold(imIn, imOut):
    grad = imageMb(imIn)
    wrk = imageMb(imIn)
    level = imageMb(imIn, 1)
    gradient(imIn, grad)
    histo = getHistogram(imIn)
    distri = []
    for i in range(256):
        if histo[i]!=0:
            threshold(imIn, level, i, i)
            mul(level, grad, wrk)
            vol = computeVolume(wrk)/histo[i]
            distri.append(vol)
        else:
            distri.append(0)
    sd = sum(distri)
    sr = distri[0]
    threshval = 0
    while(sr<(sd/2)):
        threshval += 1
        sr += distri[threshval]
    threshold(imIn, imOut, threshval, 255)
    return threshval

def segmentGrains2(imIn, imOut):
    imMarker = imageMb(imIn, 1)
    imDist = imageMb(imIn, 32)
    imDist8 = imageMb(imIn, 8)
    imWTS32 = imageMb(imIn, 32)
    imWTS = imageMb(imIn, 8)
    computeDistance(imIn, imDist, edge=FILLED)
    computeRange(imDist)
    copyBytePlane(imDist, 0, imDist8)
    negate(imDist8, imDist8)
    minima(imDist8, imMarker)
    dilate(imMarker, imMarker, 2)
    nb = label(imMarker, imWTS32)
    watershedSegment(imDist8, imWTS32)
    copyBytePlane(imWTS32, 3, imWTS)
    negate(imWTS, imWTS)
    copyBytePlane(imWTS32, 0, imOut)
    logic(imOut, imWTS, imOut, "inf")
    convert(imIn, imWTS)
    logic(imOut, imWTS, imOut, "inf")
    return nb
    
def drawDelaunay(imIn, imOut):
    """
    Draws Delaunay triangles using neighbors particles.
    Returns the ridges length in a list.
    """
    imZero = imageMb(imIn)
    imZero.reset()
    imWrk1 = imageMb(imIn)
    imWrk2 = imageMb(imIn)
    imWrk3 = imageMb(imIn)
    imWrk4 = imageMb(imIn)
    
    list_ridges = []
    copy(imIn, imWrk1)
    while computeVolume(imWrk1) != 0:
        firstParticle(imWrk1, imWrk2)
        dilate(imWrk2, imWrk3, 2)
        build(imWrk1,imWrk3)
        logic(imWrk3, imWrk2, imWrk3, "sup")
        thinD(imWrk3, imWrk4)
        negate(imWrk2, imWrk2)
        diff(imWrk4,imWrk2,imWrk2)
        diff(imWrk4,imWrk2,imWrk3)
        (x1,y1) = compare(imWrk2, imZero, imZero)
        imZero.reset()
        while computeVolume(imWrk3) != 0:
            firstParticle(imWrk3, imWrk4)
            (x2,y2) = compare(imWrk4, imZero, imZero)
            imZero.reset()
            drawLine(imWrk4,(x1,y1,x2,y2),1)
            a = computeVolume(imWrk4)
            add(imWrk4, imOut, imOut)
            list_ridges.append(a)
            
    return list_ridges


im = imageMb("medical.png")

nuclei = imageMb(im, 1)
skiz = imageMb(im, 1)
voronoi = imageMb(im, 1)
delaunay = imageMb(im, 1)

imbin1 = imageMb(im, 1)
imbin2 = imageMb(im, 1)
imbin3 = imageMb(im, 1)
im1 = imageMb(im, 8)
im2 = imageMb(im, 8)

# Finding the nuclei
################################################################################
autoThreshold(im, imbin1)
# Instead of autoThreshold you could ask the user to select the best threshold
# image (making sure the nuclei are in black) .
# Using his keyboard (with w,q,x and s) to adjust the threshold value to its
# liking
#threshold(im,imbin1,*dynamicThreshold(im))
negate(imbin1, imbin1)
removeEdgeParticles(imbin1, imbin1) # border artefact removal
closeHoles(imbin1, imbin1) # Closes holes in nuclei
opening(imbin1, imbin1, 2) # Removes small artefacts
# Segmentations : returns the number of nuclei
nb_nuclei = segmentGrains2(imbin1, im1)
threshold(im1, imbin1, 1, 255)
copy(imbin1, nuclei)
nuclei.show()
#nuclei.save("nuclei_segmentation.jpg")

# Building the voronoi tesselation, skiz and geodesic center
################################################################################
drawEdge(imbin2)
add(imbin2, imbin1, imbin1)
fastSKIZ(imbin1, imbin2)
removeEdgeParticles(imbin2, imbin2)
copy(imbin2, skiz)
skiz.show()
#skiz.save("skiz.jpg")
thinD(imbin2,imbin3)
sub(imbin2, imbin3, imbin2)
copy(imbin2, voronoi)
voronoi.show()
#voronoi.save("voronoi.jpg")

# Delaunay triangulation
################################################################################
edges = drawDelaunay(skiz, delaunay)
delaunay.show()
delaunay.save("delaunay.jpg")

# Reporting all the measurements
################################################################################
print("number of nuclei %d" % (nb_nuclei))
print("nuclei mean area %d" % (computeVolume(nuclei)/nb_nuclei))
print("cytoplasmic mean area %d" % (computeVolume(voronoi)/nb_nuclei))
print("nucleo-cytoplasmic ratio %d" % (computeVolume(voronoi)/computeVolume(nuclei)))
print("mean edge length %d" % (sum(edges)/len(edges)))

