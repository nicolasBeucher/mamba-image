# exampleA24.py
# IN Solvay_conference_1927.jpg
# OUT faces_of_physic.jpg

## TITLE #######################################################################
# Face recognition : connecting Mamba and OpenCV

## DESCRIPTION #################################################################
# This example shows how to transform a Mamba image into an OpenCV image
# and reverse. This is used to apply a face recognition algorithm offered 
# in OpenCV to our image. The picture used to try our algorithm was taken
# during the Solvay conference in 1927 
# (http://en.wikipedia.org/wiki/Solvay_Conference)

## SCRIPT ######################################################################
# Importing mamba
from mamba import *
import mambaDisplay

# Importing opencv.
import cv

# Defining the image conversions from mamba to openCv and the reverse.
def Mamba2OpenCV(imIn):
    """
    Creates an OpenCV image from the mamba image 'imIn'. The function only
    works with 8-bit images (other cases will return None).
    """
    if imIn.getDepth()!=8:
        return None

    (w, h) = imIn.getSize()
    cvImOut = cv.CreateImage((w,h), cv.IPL_DEPTH_8U, 1)
    cv.SetData(cvImOut, imIn.extractRaw())
    
    return cvImOut

def OpenCV2Mamba(cvImIn, imOut):
    """
    Loads the data contained in the openCV image 'cvImOut' into mamba image
    'imOut'. Images size and depth must be identical for the function to
    operate (the function will quit silently otherwise).
    """
    if cvImIn.depth!=cv.IPL_DEPTH_8U:
        return
    if imOut.getDepth()!=8:
        return
    if cv.GetSize(cvImIn)!=imOut.getSize():
        return
    imOut.loadRaw(cvImIn.tostring())

# Modify this line so that it points to your local installation of the
# cascade file
FACE_CASCADE_PATH = '/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml'

def detectFaces(imIn):
    """
    This function detects faces inside Mamba image 'imIn' by first converting
    it into an OpenCV image and then applying the appropriate functions.
    The function returns a tuple containing the coordinates of the bounding
    box around all the faces in the image. 
    """
    
    cvim = Mamba2OpenCV(imIn)
    size = cv.GetSize(cvim)

    # Preparing the image.
    storage = cv.CreateMemStorage(0)
    cv.EqualizeHist(cvim, cvim)
    # Detecting objects (faces).
    cascade = cv.Load(FACE_CASCADE_PATH)
    faces = cv.HaarDetectObjects(cvim,
                                 cascade,
                                 storage,
                                 1.1, 2,
                                 cv.CV_HAAR_DO_CANNY_PRUNING,
                                 (20, 20))
 
    faces_bb = ()
    for face in faces:
        face_coord = face[0]
        faces_bb += ((face_coord[0],
                      face_coord[1],
                      face_coord[0]+face_coord[2],
                      face_coord[1]+face_coord[3]),)
        
    return faces_bb

# Applying the operator on the Solvay conference image.
imIn = imageMb("Solvay_conference_1927.jpg")
imOut = imageMb(imIn)
imbin = imageMb(imIn, 1)
faces = detectFaces(imIn)
# Drawing a box around each detected face.
for f in faces:
    drawBox(imbin, f, 1)
    drawBox(imbin, map(lambda x : x+1, f), 1)
    drawBox(imbin, map(lambda x : x-1, f), 1)
copy(imIn, imOut)
multiSuperpose(imOut, imbin)
name = mambaDisplay.tagOneColorPalette(255, (255,0,0))
imOut.save("faces_of_physic.jpg", palette=mambaDisplay.getPalette(name))
