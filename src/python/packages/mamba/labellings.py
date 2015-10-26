"""
This module contains various labelling procedures for sets and for partitions.
They use the label operator now available for sets and for grey images.
"""

# Contributor: Serge BEUCHER

import mamba
import mamba.core as core
  
def partitionLabel(imIn, imOut):
    """
    This procedure labels each cell of image 'imIn' and puts the result in
    'imOut'. The number of cells is returned. 'imIn' can be a 1-bit, 8-bit or a
    32-bit image. 'imOut' is a 32-bit image. When 'imIn' is a binary image, all the
    connected components of the background are also labelled. When 'imIn' is a grey
    image, the 0-valued cells are also labelled (which is not the case with the label
    operator.
    Warning! The label values of adjacent cells are not necessarily consecutive.
    """
    
    imWrk1 = mamba.imageMb(imIn, 1)
    imWrk2 = mamba.imageMb(imIn, 32)
    
    if imIn.getDepth() == 1:
        mamba.negate(imIn, imWrk1)
    else:
        mamba.threshold(imIn, imWrk1, 0, 0)
    nb1 = mamba.label(imWrk1, imWrk2)
    mamba.convertByMask(imWrk1, imOut, mamba.computeMaxRange(imOut)[1], 0)
    mamba.logic(imOut, imWrk2, imOut, "sup")
    nb2 = mamba.label(imIn, imWrk2)
    mamba.addConst(imWrk2, nb1, imWrk2)
    mamba.logic(imOut, imWrk2, imOut, "inf")
    return nb1 + nb2
    
def measureLabelling(imIn, imMeasure, imOut):
    """
    Labelling each particle of the binary image or each cell of the partition 'imIn'
    with the number of pixels in the binary image 'imMeasure' contained in each particle
    or each cell of the partition. The result is put is the 32-bit image 'imOut'.
    """
    
    imWrk1 = mamba.imageMb(imIn, 32)
    imWrk2 = mamba.imageMb(imIn, 1)
    imWrk3 = mamba.imageMb(imIn, 8)
    imWrk4 = mamba.imageMb(imIn, 8)
    imWrk5 = mamba.imageMb(imIn, 8)
    imWrk6 = mamba.imageMb(imIn, 32)
    
    # Output image is emptied.
    imOut.reset()
    # Labelling the initial image.
    if imIn.getDepth() == 1:
        nbParticles = mamba.label(imIn, imWrk1)
    else:
        nbParticles = partitionLabel(imIn, imWrk1)
    # Defining output LUTs.
    outLuts = [[0 for i in range(256)] for i in range(4)]
    # Converting the imMeasure image to 8-bit.
    mamba.convert(imMeasure, imWrk4)
    while nbParticles > 0:
        # Particles with labels between 1 and 255 are extracted.
        mamba.threshold(imWrk1, imWrk2, 0, 255)
        mamba.convert(imWrk2, imWrk3)
        mamba.copyBytePlane(imWrk1, 0, imWrk5)
        mamba.logic(imWrk3, imWrk5, imWrk3, "inf")
        # The points contained in each particle are labelled.
        mamba.logic(imWrk3, imWrk4, imWrk5, "inf")
        # The histogram is computed.
        histo = mamba.getHistogram(imWrk5)
        # The same operation is performed for the 255 particles. 
        for i in range(1, 256):
            # The number of points in each particle is obtained from the histogram.
            value = histo[i]
            j = 3
            # This value is splitted in powers of 256 and stored in the four 
            # output LUTs.
            while j >= 0:
                n = 2 ** (8 * j)
                outLuts[j][i] = value // n
                value = value % n
                j -= 1
        # Each LUT is used to label each byte plane of a temporary image with the
        # corresponding value.
        for i in range(4):
            mamba.lookup(imWrk3, imWrk5, outLuts[i])
            mamba.copyBytePlane(imWrk5, i, imWrk6)
        # The intermediary result is accumulated in the final image.
        mamba.logic(imOut, imWrk6, imOut, "sup")
        # 255 is subtracted from the initial labelled image in order to process
        # the next 255 particles.
        mamba.floorSubConst(imWrk1, 255, imWrk1)
        nbParticles -= 255
 
def areaLabelling(imIn, imOut):
    """
    Special case of measure labelling where each connected component of the binary image
    'imIn' or each cell of the partition 'imIn'	is labelled with its area. The label image
    is stored in the 32-bit image 'imOut'.
    """
	
    imWrk = mamba.imageMb(imIn, 1)
    
    if imIn.getDepth() == 1:
        mamba.copy(imIn, imWrk)
    else:
        imWrk.fill(1)
    measureLabelling(imIn, imWrk, imOut)
	
def diameterLabelling(imIn, imOut, dir, grid=mamba.DEFAULT_GRID):
    """
    Labels each connected component of the binary image 'imIn' with its diameter in 
    direction 'dir'. The labelled image is stored in the 32-bit image 'imOut'.
    If 'imIn' is a 8-bit or 32-bit image, this function works too. However, the
    0-valued connected components are labelled with 0.
    This procedure works on hexagonal or square grid.
    'dir' can be any strictly positive integer value.
    """
    
    imWrk1 = mamba.imageMb(imIn, 1)
    imWrk2 = mamba.imageMb(imIn)
    
    ed = 1 << ((dir - 1)%(mamba.gridNeighbors(grid)//2)) +1
    if imIn.getDepth() == 1:
        mamba.copy(imIn, imWrk1)
        mamba.diffNeighbor(imIn, imWrk1, ed, grid=grid)
    else:
        mamba.nonEqualNeighbors(imIn, imWrk2, ed, grid=grid, edge= mamba.EMPTY)
        mamba.threshold(imWrk2, imWrk1, 1, mamba.computeMaxRange(imWrk2)[1])
    # They are used for the labelling.
    measureLabelling(imIn, imWrk1, imOut)
 
def feretDiameterLabelling(imIn, imOut, direc):
    """
    The Feret diameter of each connected component of the binary image or the
    partition image 'imIn' is computed and its value labels the corresponding
    component. The labelled image is stored in the 32-bit image 'imOut'.
    If 'direc' is "vertical", the vertical Feret diameter is computed. If it is
    set to "horizontal", the corresponding diameter is used.    
    """
    
    imWrk1 = mamba.imageMb(imIn, 1)
    imWrk2 = mamba.imageMb(imIn, 32)
    imWrk3 = mamba.imageMb(imIn, 32)
    imWrk4 = mamba.imageMb(imIn, 32)
    
    imWrk1.fill(1)
    if direc == "horizontal":
        dir = 7    
    elif direc == "vertical":
        dir = 1
    else:
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        # The above statement generates an error ('direc' is not horizontal or 
        # vertical.
    # An horizontal or vertical distance function is generated.
    mamba.linearErode(imWrk1, imWrk1, dir, grid=mamba.SQUARE, edge=mamba.EMPTY)
    mamba.computeDistance(imWrk1, imOut, grid=mamba.SQUARE, edge=mamba.FILLED)
    mamba.addConst(imOut, 1, imOut)
    if imIn.getDepth() == 1:
	    # Each particle is valued with the distance.
        mamba.convertByMask(imIn, imWrk2, 0, mamba.computeMaxRange(imWrk3)[1])
        mamba.logic(imOut, imWrk2, imWrk3, "inf")
        # The valued image is preserved.
        mamba.copy(imWrk3, imWrk4)
        # Each component is labelled by the maximal coordinate.
        mamba.build(imWrk2, imWrk3)
        # Using the dual reconstruction, we label the particles with the
        # minimal ccordinate.
        mamba.negate(imWrk2, imWrk2)
        mamba.logic(imWrk2, imWrk4, imWrk4, "sup")
        mamba.dualBuild(imWrk2, imWrk4)
        # We subtract 1 because the selected coordinate must be outside the particle.
        mamba.subConst(imWrk4, 1, imWrk4)
        mamba.negate(imWrk2, imWrk2)
        mamba.logic(imWrk2, imWrk4, imWrk4, "inf")
        # Then, the subtraction gives the Feret diameter.
        mamba.sub(imWrk3, imWrk4, imOut)
    else:
        mamba.copy(imOut, imWrk3)
        if imIn.getDepth() == 32:
            mamba.copy(imIn, imWrk2)
        else:
            mamba.convert(imIn, imWrk2)
	# Using the cells builds (direct and dual to label the cells with the maximum
        # and minimum distance.
        mamba.cellsBuild(imWrk2, imWrk3)
        mamba.cellsBuild(imWrk2, imWrk3)
        mamba.negate(imOut, imOut)
        mamba.cellsBuild(imWrk2, imOut)
        mamba.negate(imOut, imOut)
        # Subtracting 1...
        mamba.subConst(imOut, 1, imOut)
        # ... and getting the final result.
        mamba.sub(imWrk3, imOut, imOut)
		
def volumeLabelling(imIn1, imIn2, imOut):
    """
    Each connected component of the binary image  or the partition 'imIn1' is
    labelled with the volume of the greyscale or 32-bit image 'imIn2' inside
    this component. The result is put in the 32-bit image 'imOut'.
    """
    
    imWrk1 = mamba.imageMb(imIn1, 1)
    imWrk2 = mamba.imageMb(imIn1, 32)
    imWrk3 = mamba.imageMb(imIn1, 8)
    
    imOut.reset()
    n = imIn2.getDepth()
    # Case of a 8-bit image.
    if n == 8:
        for i in range(8):
            # Each bit plane is extracted and used in the labelling.
            mamba.copyBitPlane(imIn2, i, imWrk1)
            measureLabelling(imIn1, imWrk1, imWrk2)
            # The resulting labels are combined to obtain the final one.
            v = 2 ** i
            mamba.mulConst(imWrk2, v, imWrk2)
            mamba.add(imOut, imWrk2, imOut)
    else:
        for j in range(4):
            # Each byte plane is treated.
            mamba.copyBytePlane(imIn2, j, imWrk3)
            for i in range(8):
                mamba.copyBitPlane(imWrk3, i, imWrk1)
                measureLabelling(imIn1, imWrk1, imWrk2)
                v = 2 ** (8 * j + i)
                mamba.mulConst(imWrk2, v, imWrk2)
                mamba.add(imOut, imWrk2, imOut) 

