"""
Thinning and thickening 3D operators.

This module contains morphological thinning and thickening operators based on
the Hit-or-Miss transformation. The module also defines the double 3D
structuring element class which serves as a base for these operators.
"""

# Contributor: Nicolas BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

################################################################################
# Double (bi-phased) structuring elements definitions
################################################################################

class doubleStructuringElement3D:
    """
    This class allows to define a doublet of structuring elements used in a coded 
    format by Hit-or-Miss, thin and thick operations and their corresponding methods.
    """
    
    def __init__(self, *args):
        """
        Double structuring 3D element constructor. A double structuring
        element is defined by the first (background points) and second 
        (foreground points) structuring elements 3D.
        
        You can define it in two ways:
            * doubleStructuringElement3D(se0, se1): where 'se0' and 'se1' are 
            instances of the class structuringElement3D found in erodil3D
            module. These structuring elements must be defined on the same grid.
            * doubleStructuringElement3D(dse0, dse1, grid): where 'dse0' and
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
            self.se0 = m3D.structuringElement3D(args[0], args[2])
            self.se1 = m3D.structuringElement3D(args[1], args[2])
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
    
    def getStructuringElement3D(self, ground):
        """
        Returns the structuring element of the foreground if 'ground' is set to
        1 or the structuring element of the background otherwise.
        """
        
        if ground==1:
            return self.se1
        else:
            return self.se0
        
    def flip(self):
        """
        Flips the doublet of structuring elements. Flipping corresponds
        to a swap: the doublet (se0, se1) becomes (se1, se0).
        """
        
        return doubleStructuringElement3D(self.se1, self.se0)
    
################################################################################
# Hit-or-Miss, thin and thick binary operators
################################################################################
    
def hitOrMiss3D(imIn, imOut, dse, edge=mamba.EMPTY):
    """
    Performs a binary Hit-or-miss operation on 3D image 'imIn' using the 
    doubleStructuringElement3D 'dse'. Result is put in 'imOut'.
    
    WARNING! 'imIn' and 'imOut' must be different images.
    """
    
    (width,height,length) = imIn.getSize()
    depth = imIn.getDepth()
    if depth!=1:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DEPTH)
    if length!=len(imOut):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    zext = dse.grid.getZExtension()
    imWrk = m3D.image3DMb(width, height, length+zext*2, depth)
    
    # Border handling
    imWrk.reset()
    m3D.copy3D(imIn, imWrk, firstPlaneOut=1)
    if edge==mamba.FILLED:
        m3D.negate3D(imWrk, imWrk)
        for i in range(zext):
            imWrk[i].reset()
            imWrk[length+zext*2-1-i].reset()
        dse = dse.flip()

    # Central point
    if dse.se1.hasZero():
        m3D.copy3D(imWrk, imOut, firstPlaneIn=1)
    else:
        if dse.se0.hasZero():
            for i in range(length):
                mamba.negate(imWrk[i+1], imOut[i])
        else:
            imOut.fill(1)

    # Other directions
    dirs = m3D.getDirections3D(dse.getGrid(), True)
    dirs0 = dse.se0.getDirections()
    dirs1 = dse.se1.getDirections()
    grid2D = dse.getGrid().get2DGrid()
    for d in dirs:
        if d in dirs1:
            for i in range(length):
                (planeOffset, dc) = dse.getGrid().convertFromDir(d,i)
                mamba.infNeighbor(imWrk[i+1+planeOffset], imOut[i], 1<<dc, grid=grid2D, edge=edge)
        elif d in dirs0:
            for i in range(length):
                (planeOffset, dc) = dse.getGrid().convertFromDir(d,i)
                mamba.diffNeighbor(imWrk[i+1+planeOffset], imOut[i], 1<<dc, grid=grid2D, edge=edge)
    
def thin3D(imIn, imOut, dse, edge=mamba.EMPTY):
    """
    Elementary thinning operator with 'dse' double structuring element.
    'imIn' and 'imOut' are binary 3D images.
    
    'edge' is set to EMPTY by default.
    """
        
    imWrk = m3D.image3DMb(imIn)
    hitOrMiss3D(imIn, imWrk, dse, edge=edge)
    m3D.diff3D(imIn, imWrk, imOut)
    
def thick3D(imIn, imOut, dse):
    """
    Elementary thickening operator with 'dse' double structuring element.
    'imIn' and 'imOut' are binary 3D images.
    
    The edge is always EMPTY (as for mamba.hitOrMiss).
    """
        
    imWrk = m3D.image3DMb(imIn)
    hitOrMiss3D(imIn, imWrk, dse)
    m3D.logic3D(imIn, imWrk, imOut, "sup") 

