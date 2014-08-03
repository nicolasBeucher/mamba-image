"""
Thinning and thickening operators.

This module contains morphological thinning and thickening operators based on
the Hit-or-Miss transformation, together with various homotopic and geodesic
functions derived from these operators. The module also defines the double
structuring element class which serve as a base for these operators.
"""

import mamba
import mamba.core as core

# Contributor: Serge BEUCHER

################################################################################
# Double (bi-phased) structuring elements definitions
################################################################################

class doubleStructuringElement:
    """
    This class allows to define a doublet of structuring elements used in a coded 
    format by Hit-or-Miss, thin and thick operations and their corresponding methods.
    The coding corresponds to the output of the 'hitormissPatternSelector' tool 
    available in the extra module (mambaDisplay package).
    """
    
    def __init__(self, *args):
        """
        Double structuring element constructor. A double structuring element is
        defined by the first (background points) and second (foreground points) 
        structuring elements.
        
        You can define it in two ways:
            * doubleStructuringElement(se0, se1): where 'se0' and 'se1' are 
            instances of the class structuring element found in erodil module.
            These structuring elements must be defined on the same grid.
            * doubleStructuringElement(dse0, dse1, grid): where 'dse0' and
            'dse1' are direction lists and 'grid' defines the grid on which the
            two structuring elements are defined.
            
        If the constructor is called with inapropriate arguments, it raises a
        ValueError exception.
        """
        
        if len(args)==2:
            if args[0].getGrid()!=args[1].getGrid():
                raise ValueError("Grid value mismatch")
            self.se0 = args[0]
            self.se1 = args[1]
            self.grid = self.se0.getGrid()
        elif len(args)==3:
            self.se0 = mamba.structuringElement(args[0], args[2])
            self.se1 = mamba.structuringElement(args[1], args[2])
            self.grid = args[2]
        else:
            raise ValueError("Incorrect constructor call")
        
    def __repr__(self):
        return "doubleStructuringElement("+repr(self.se0)+", "+repr(self.se1)+")"
        
    def getGrid(self):
        """
        Returns the grid on which the double stucturing element is defined.
        """
        
        return self.grid
    
    def getStructuringElement(self, ground):
        """
        Returns the structuring element of the foreground if 'ground' is set to
        1 or the structuring element of the background otherwise.
        """
        
        if ground==1:
            return self.se1
        else:
            return self.se0
    
    def getCSE(self):
        """
        Returns the coded values corresponding to the background and
        foreground structuring elements se0 and se1 in a tuple so they can
        be used with the HitOrMiss function.
        """
        
        return (self.se0.enc_dirs, self.se1.enc_dirs)
    
    def rotate(self, step=1):
        """
        Rotates the double structuring element 'step' times (default=1). When 'step'
        is positive, rotation is clockwise. When 'step' is negative, rotation is
        counterclockwise. No rotation occurs when 'step' equals zero.
        """
        
        rot_se0 = self.se0.rotate(step)
        rot_se1 = self.se1.rotate(step)
        return doubleStructuringElement(rot_se0, rot_se1)
        
    def flip(self):
        """
        Flips the doublet of structuring elements. Flipping corresponds
        to a swap: the doublet (se0, se1) becomes (se1, se0).
        """
        
        return doubleStructuringElement(self.se1, self.se0)
    
################################################################################
# Hit-or-Miss, thin and thick binary operators
################################################################################
    
def hitOrMiss(imIn, imOut, dse, edge=mamba.EMPTY):
    """
    Performs a binary Hit-or-miss operation on image 'imIn' using the double
    structuring element 'dse'. Result is put in 'imOut'.
    
    WARNING! 'imIn' and 'imOut' must be different images.
    
    'edge' value can be EMPTY or FILLED.
    
    You can also find a helper function (hitormissPatternSelector) in the 
    mambaExtra module.
    """
    es0, es1 = dse.getCSE()
    err = core.MB_BinHitOrMiss(imIn.mbIm, imOut.mbIm, es0, es1, dse.getGrid().id, edge.id)
    mamba.raiseExceptionOnError(err)
    imOut.update()
    
def thin(imIn, imOut, dse, edge=mamba.EMPTY):
    """
    Elementary thinning operator with 'dse' double structuring element.
    
    'imIn' and 'imOut' are binary images.
    
    'edge' is set to EMPTY by default.
    """
    
    imWrk = mamba.imageMb(imIn)
    hitOrMiss(imIn, imWrk, dse, edge=edge)
    mamba.diff(imIn, imWrk, imOut)
    
def thick(imIn, imOut, dse):
    """
    Elementary thickening operator with 'dse' double structuring element. The
    
    'imIn' and 'imOut' are binary images.
    
    The edge is always EMPTY (as for hitOrMiss).
    """
    
    imWrk = mamba.imageMb(imIn)
    hitOrMiss(imIn, imWrk, dse, edge=mamba.EMPTY)
    mamba.logic(imIn, imWrk, imOut, "or") 
    
def rotatingThin(imIn, imOut, dse, edge=mamba.FILLED):
    """
    Performs a complete rotation of thinnings , the initial 'dse' double
    structuring element being turned one step clockwise after each thinning.
    At each rotation step, the previous result is used as input for the next
    thinning (chained thinnings). Depending on the grid where 'dse' is defined,
    6 or 8 rotations are performed.
    
    'imIn' and 'imOut' are binary images.
    
    'edge' is set to FILLED by default (default value is EMPTY in simple thin).
    """
    
    imWrk = mamba.imageMb(imIn)
    if edge == mamba.FILLED:
        mamba.negate(imIn, imOut)
        for d in mamba.getDirections(dse.getGrid(), True):
            hitOrMiss(imOut, imWrk, dse.flip(), edge=mamba.EMPTY)
            mamba.logic(imWrk, imOut, imOut, "sup")
            dse = dse.rotate()
        mamba.negate(imOut, imOut)
    else:
        mamba.copy(imIn, imOut)
        for d in mamba.getDirections(dse.getGrid(), True):
            hitOrMiss(imOut, imWrk, dse, edge=mamba.EMPTY)
            mamba.diff(imOut, imWrk, imOut)
            dse = dse.rotate()

def rotatingThick(imIn, imOut, dse):
    """
    Performs a complete rotation of thickenings, the initial 'dse' double
    structuring element being turned one step clockwise after each thickening.
    At each rotation step, the previous result is used as input for the next
    thickening (chained thickenings). Depending on the grid where 'dse' is defined,
    6 or 8 rotations are performed.
    
    'imIn' and 'imOut' are binary images.
    
    The edge is always set to EMPTY.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    for d in mamba.getDirections(dse.getGrid(), True):
        hitOrMiss(imOut, imWrk, dse, edge=mamba.EMPTY)
        mamba.logic(imWrk, imOut, imOut, "sup")
        dse = dse.rotate()

def infThin(imIn, imOut, dse, edge=mamba.EMPTY):
    """
    Performs an inf of thinnings, each thinning being made with the successive 
    rotations of 'dse'. The initial image 'imIn' is used at each step of 
    thinning (intersection of thinnings).
    
    'imIn' and 'imOut' are binary images.
    
    'edge' is set to EMPTY by default.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    mamba.copy(imIn, imWrk1)
    for i in range(mamba.gridNeighbors(dse.getGrid())):
        hitOrMiss(imWrk1, imWrk2, dse, edge=edge)
        mamba.diff(imOut, imWrk2, imOut)
        dse = dse.rotate()

def supThick(imIn, imOut, dse):
    """
    Performs a sup of thickenings, each thickening being made with the successive 
    rotations of 'dse'. The initial image 'imIn' is used at each step of 
    thickening (union of thickenings).

    'imIn' and 'imOut' are binary images.
    
    The edge is always set to EMPTY.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk1)
    mamba.copy(imIn, imOut)
    for i in range(mamba.gridNeighbors(dse.getGrid())):
        hitOrMiss(imWrk1, imWrk2, dse)
        mamba.logic(imWrk2, imOut, imOut, "sup")
        dse = dse.rotate()
    
def fullThin(imIn, imOut, dse, edge=mamba.EMPTY):
    """
    Performs a complete thinning of 'imIn' with the successive rotations of 'dse'
    (until idempotence) and puts the result in 'imOut'.
    
    'imIn' and 'imOut' are binary images.
    
    'edge' is set to EMPTY by default.
    """
    
    if edge == mamba.EMPTY:
        imWrk = mamba.imageMb(imIn)
        mamba.copy(imIn, imOut)
        v1 = mamba.computeVolume(imOut)
        v2 = 0
        while v1 != v2:
            v2 = v1
            for i in range(mamba.gridNeighbors(dse.getGrid())):
                hitOrMiss(imOut, imWrk, dse)
                mamba.diff(imOut, imWrk, imOut)
                dse = dse.rotate()
            v1 = mamba.computeVolume(imOut)
    else:
        mamba.negate(imIn, imOut)
        v1 = mamba.computeVolume(imOut)
        v2 = 0
        while v1 != v2:
            v2 = v1
            rotatingThick(imOut, imOut, dse.flip())
            v1 = mamba.computeVolume(imOut)
        mamba.negate(imOut, imOut)

def fullThick(imIn, imOut, dse):
    """
    Performs a complete thickening of 'imIn' with the successive rotations of 'dse'
    (until idempotence) and puts the result in 'imOut'. 
    
    'imIn' and 'imOut' are binary images.
    
    The edge is always set to EMPTY.
    """
    
    mamba.copy(imIn, imOut)
    v1 = mamba.computeVolume(imOut)
    v2 = 0
    while v1 != v2:
        v2 = v1
        rotatingThick(imOut, imOut, dse)
        v1 = mamba.computeVolume(imOut)


################################################################################
# Double structuring elements definitions (most useful ones).
# Modifying the definitions of these structuring elements is a VERY BAD idea!
################################################################################

# L, M, D and E structuring elements
hexagonalL = doubleStructuringElement([1,6], [3,4], mamba.HEXAGONAL)
squareL = doubleStructuringElement([1,2,8], [4,5,6], mamba.SQUARE)
hexagonalM = doubleStructuringElement([1], [3,4,5], mamba.HEXAGONAL)
squareM = doubleStructuringElement([1,8], [3,4,5,6], mamba.SQUARE)
hexagonalD = doubleStructuringElement([3,4,5], [1], mamba.HEXAGONAL)
squareD = doubleStructuringElement([3,4,5,6], [1,8], mamba.SQUARE)
hexagonalE = doubleStructuringElement([3,4,5,6], [0], mamba.HEXAGONAL)
squareE = doubleStructuringElement([3,4,5,6,7], [0], mamba.SQUARE)
# Some other specific structuring elements used for multiple points extraction
hexagonalS1 = doubleStructuringElement([2,3,5,6], [0,1,4], mamba.HEXAGONAL)
hexagonalS2 = doubleStructuringElement([2,4,5,6], [0,1,3], mamba.HEXAGONAL)
squareS1 = doubleStructuringElement([3,7], [0,1,5], mamba.SQUARE)
squareS2 = doubleStructuringElement([2,5,6,7], [0,1,3], mamba.SQUARE)
# Special pattern used to perform SKIZ
squareS3 = doubleStructuringElement([3,4,5,6,7], [1], mamba.SQUARE)
# Isolated points detection
hexagonalI = doubleStructuringElement([1,2,3,4,5,6], [0], mamba.HEXAGONAL)
squareI = doubleStructuringElement([1,2,3,4,5,6,7,8], [0], mamba.SQUARE)

################################################################################
# Specific thinnings and thickenings (homotopic operators and utilities).
################################################################################

def thinL(imIn, imOut, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Complete thinning with L structuring element. Depending on the grid in use,
    hexagonalL or squareL will be used. This operator is also called skeleton,
    as it produces a result which looks like a connected skeleton of each 
    connected component of 'imIn'.
    
    This operator must be used with binary images.
    
    The edge is set to EMPTY by default.
    """
    
    if grid == mamba.HEXAGONAL:
        dse = hexagonalL
    else:
        dse = squareL
    fullThin(imIn, imOut, dse, edge=edge)

def thinM(imIn, imOut, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Complete thinning with M structuring element. Depending on the grid in use,
    hexagonalM or squareM will be used. This operator produces skeletons with
    lots of fishbones.
    
    This operator must be used with binary images.
    
    The edge is set to EMPTY by default.
    """
    
    if grid == mamba.HEXAGONAL:
        dse = hexagonalM
    else:
        dse = squareM
    fullThin(imIn, imOut, dse, edge=edge)

def thinD(imIn, imOut, grid=mamba.DEFAULT_GRID, edge=mamba.EMPTY):
    """
    Complete thinning with D structuring element. Depending on the grid in use,
    hexagonalD or squareD will be used. This operator is mainly used to simplify
    each connected component to the simplest homotopic equivalent set (see
    homotopicReduction in this module).
    
    This operator must be used with binary images.
    
    The edge is set to EMPTY by default.
    """
    
    if grid == mamba.HEXAGONAL:
        dse = hexagonalD
    else:
        dse = squareD
    fullThin(imIn, imOut, dse, edge=edge)

def thickL(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Complete thickening with L structuring element. Depending on the grid in use,
    hexagonalL or squareL will be used. Note that L is equal to its flipping (same
    structuring element is used in thinning and thickening).
    
    This operator must be used with binary images.
    
    The edge is always EMPTY.
    """
    
    if grid == mamba.HEXAGONAL:
        dse = hexagonalL
    else:
        dse = squareL
    fullThick(imIn, imOut, dse)

def thickM(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Complete thickening with M structuring element. Depending on the grid in use,
    hexagonalD or squareD will be used. D structuring element is the flipping of
    M structuring element for the thickening.
    
    This operator must be used with binary images.
    """
    
    if grid == mamba.HEXAGONAL:
        dse = hexagonalD
    else:
        dse = squareD
    fullThick(imIn, imOut, dse)

def thickD(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Complete thickening with D structuring element. Depending on the grid in use,
    hexaM or squareM will be used. M structuring element is the flipping of
    D for the thickening.
    
    This operator must be used with binary images.
    """
    
    if grid == mamba.HEXAGONAL:
        dse = hexagonalM
    else:
        dse = squareM
    fullThick(imIn, imOut, dse)

def endPoints(imIn, imOut, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Extracts end points in 'imIn', supposed to be a "skeleton" image (connected 
    components without thickness), and puts them in 'imOut'.
    
    'edge' is FILLED by default and it can be modified to take into account
    extremities touching the edge.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    if grid == mamba.HEXAGONAL:
        dse1 = hexagonalE
        dse2 = hexagonalL
        nb = 6
        step = 1
    else:
        dse1 = squareE
        dse2 = squareL
        nb = 4
        step = 2
    rotatingThin(imIn, imWrk1, dse2, edge=edge)
    # added to avoid blocking of the process in clipping
    mamba.diff(imIn, imWrk1, imOut)
    for i in range(nb):
        hitOrMiss(imWrk1, imWrk2, dse1, edge=edge)
        mamba.logic(imOut, imWrk2, imOut, "sup")
        dse1 = dse1.rotate(step)

def multiplePoints(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Extracts multiple points in 'imIn', supposed to be a "skeleton" image (connected 
    components without thickness), and puts the result in 'imOut'.
    
    Note that, on a square grid, the resulting skeleton is supposed to be defined 
    on a 4-connectivity grid. if it is not the case, some multiple points are likely
    to be missed.
    """
    
    imWrk1 = mamba.imageMb(imIn)
    imWrk2 = mamba.imageMb(imIn)
    endPoints(imIn, imWrk2)
    if grid == mamba.HEXAGONAL:
        dse_list = [hexagonalS1, hexagonalS2]
        step = 1
        nb = 6
    else:
        dse_list = [squareS1, squareS2]
        step = 2
        nb = 4
    for dse in dse_list:
        for i in range(nb):
            hitOrMiss(imIn, imWrk1, dse)
            mamba.logic(imWrk1, imWrk2, imWrk2, "sup")
            dse = dse.rotate(step)
    mamba.diff(imIn, imWrk2, imOut)

def whiteClip(imIn, imOut, step=0, grid=mamba.DEFAULT_GRID, edge=mamba.FILLED):
    """
    Performs a skeleton clipping of 'imIn' (supposed to contain a skeleton image)
    and puts the result in 'imOut'. If 'step' is not defined (or equal to 0), the 
    clipping is performed until idempotence. If 'step' is defined, 'step' points
    (if possible) will be removed from each branch of the skeleton.
    
    'edge' is set to FILLED by default.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    if step == 0:
        v1 = mamba.computeVolume(imOut)
        v2 = 0
        while v1 != v2:
            v2 = v1
            endPoints(imOut, imWrk, grid=grid, edge=edge)
            mamba.diff(imOut, imWrk, imOut)
            v1 = mamba.computeVolume(imOut)
    else:
        for i in range(step):
            endPoints(imOut, imWrk, grid=grid, edge=edge)
            mamba.diff(imOut, imWrk, imOut)

def blackClip(imIn, imOut, step=0, grid=mamba.DEFAULT_GRID):
    """
    Performs a black skeleton clipping (clipping of a black skeleton image). 
    If 'step' is not defined (or equal to 0), the clipping is performed until 
    idempotence. If 'step' is defined, 'step' black points (if possible) will be 
    removed from each branch of the black skeleton.
    
    'edge' is always set to FILLED.
    """
    
    imWrk = mamba.imageMb(imIn)
    mamba.negate(imIn, imOut)
    if step == 0:
        v1 = mamba.computeVolume(imOut)
        v2 = 0
        while v1 != v2:
            v2 = v1
            endPoints(imOut, imWrk, grid=grid, edge=mamba.FILLED)
            mamba.diff(imOut, imWrk, imOut)
            v1 = mamba.computeVolume(imOut)
    else:
        for i in range(step):
            endPoints(imOut, imWrk, grid=grid, edge=mamba.FILLED)
            mamba.diff(imOut, imWrk, imOut)
    mamba.negate(imOut, imOut)
    
def homotopicReduction(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Reduces any simply connected component of 'imIn' (component without holes) 
    to a single point. All other components are reduced to simpler ones, with 
    same homotopy as the initial ones. This transformation is simply thinD on 
    the hexagonal grid. It is a combination of thinnings with D and E structuring 
    elements on square grid.
    """

    thinD(imIn, imOut, grid=grid)
    if grid == mamba.SQUARE:
        fullThin(imOut, imOut, squareS3)


def computeSKIZ(imIn, imOut, grid=mamba.DEFAULT_GRID):
    """
    Computes the influence zones of each connected component of 'imIn' and puts
    the result in 'imOut'. Inverting the result produces the skeleton by influence
    zones (SKIZ).
    
    There exists a much faster way to compute the SKIZ operation (see segment.py
    module).
    """

    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imWrk)
    if grid == mamba.SQUARE:
        dse = squareS3
        thick(imWrk, imWrk, dse)
        thick(imWrk, imWrk, dse.rotate(2))
        thick(imWrk, imWrk, dse.rotate(4))
        thick(imWrk, imWrk, dse.rotate(6))
    thickM(imWrk, imWrk, grid=grid)
    blackClip(imWrk, imOut, grid=grid)

    
################################################################################
# Geodesic thinnings and thickenings
################################################################################

def geodesicThin(imIn, imMask, imOut, dse):
    """
    Geodesic thinning of image 'imIn' inside 'imMask' by the double structuring
    element 'dse'. The result is stored in 'imOut'.
    
    'imIn', 'imMask' and 'imOut' are binary images.
    """
    
    mamba.diff(imMask, imIn, imOut)
    thick(imOut, imOut, dse.flip())
    mamba.diff(imMask, imOut, imOut)
    
def geodesicThick(imIn, imMask, imOut, dse):
    """
    Geodesic thickening of image 'imIn' inside 'imMask' by the double
    structuring element 'dse'. The result is stored in 'imOut'.
    
    'imIn', 'imMask' and 'imOut' are binary images.
    """
    
    thick(imIn, imOut, dse)
    mamba.logic(imOut, imMask, imOut, "inf")
    
def rotatingGeodesicThick(imIn, imMask, imOut, dse):
    """
    Performs successive geodesic thickenings of 'imIn' inside 'imMask' with 
    clockwise rotations of the double structuring element 'dse'. The number of 
    rotations is either 6 or 8 according to the grid where 'dse' is defined.
    All the thickenings are concatenated.
    
    'imIn', 'imMask' and 'imOut' are binary images.
    """

    imWrk = mamba.imageMb(imIn)
    mamba.copy(imIn, imOut)
    for i in range(mamba.gridNeighbors(dse.getGrid())):
        hitOrMiss(imOut, imWrk, dse)
        mamba.logic(imWrk, imOut, imOut, "sup")
        mamba.logic(imMask, imOut, imOut, "inf")
        dse = dse.rotate()

def rotatingGeodesicThin(imIn, imMask, imOut, dse):
    """
    Performs successive geodesic thinnings of 'imIn' inside 'imMask' with 
    clockwise rotations of the double structuring element 'dse'. The number of 
    rotations is either 6 or 8 according to the grid where 'dse' is defined.
    All the thinnings are concatenated.
    
    'imIn', 'imMask' and 'imOut' are binary images.
    """

    mamba.diff(imMask, imIn, imOut)
    rotatingGeodesicThick(imOut, imMask, imOut, dse.flip())
    mamba.diff(imMask, imOut, imOut)

def fullGeodesicThick(imIn, imMask, imOut, dse):
    """
    Performs a complete geodesic thickening (until idempotence) of image 'imIn'
    inside mask 'imMask' with all the rotations of the double structuring
    element 'dse'. The result is put in 'imOut'.
    """
    
    mamba.copy(imIn, imOut)
    v1 = mamba.computeVolume(imOut)
    v2 = 0
    while v1 != v2:
        v2 = v1
        rotatingGeodesicThick(imOut, imMask, imOut, dse)
        v1 = mamba.computeVolume(imOut)

def fullGeodesicThin(imIn, imMask, imOut, dse):
    """
    Performs a complete geodesic thinning (until idempotence) of image 'imIn'
    inside mask 'imMask' with all the rotations of the double structuring
    element 'dse'. The result is put in 'imOut'.
    """
    
    mamba.diff(imMask, imIn, imOut)
    fullGeodesicThick(imOut, imMask, imOut, dse.flip())
    mamba.diff(imMask, imOut, imOut)

