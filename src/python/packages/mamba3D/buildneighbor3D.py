import mamba
import mamba3D as m3D

def buildNeighbor3D(imMask, imInOut, d, grid=m3D.DEFAULT_GRID3D):
    """
    Builds  3D image 'imInout' in direction 'd' according to 'grid' using 'imMask'
    as a mask (the propagation is performed only in 'd' direction).
    
    The function also returns the volume of the image 'imInout' after the
    build operation.
    
    'grid' value can be any 3D grid.
    """
    
    (width, height, length) = imInOut.getSize()
    if length!=len(imMask):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    imWrk = mamba.imageMb(imInOut[0])
    grid2D = grid.get2DGrid()
    scan = grid.convertFromDir(d,0)[0]
    volume = 0L
    if scan == 0:
        for i in range(length):
            vol = mamba.buildNeighbor(imMask[i], imInOut[i], dh, grid2D)
            volume += vol
    else:
        if scan == 1:
            startPlane, endPlane = 0, length - 1
        else:
            startPlane, endPlane = length - 1, 0
        for i in range(startPlane, endPlane, scan):
            mamba.logic(imInOut[i], imMask[i], imWrk, "inf")
            vol = mamba.computeVolume(imWrk)
            volume += vol
            td = grid.getTranDir(d)
            dh = grid.converFromDir(td,i+scan)[1]
            mamba.supNeighbor(imWrk, imInOut[i+scan], dh, grid2D)
        mamba.logic(imInOut[endPlane], imMask[endPlane], imInOut[endPlane], "inf")
        vol = mamba.computeVolume(imInOut[length - 1])
        volume += vol           
    return volume
    
def dualbuildNeighbor3D(imMask, imInout, d, grid=m3D.DEFAULT_GRID3D):
    """
    Dual builds image 'imInout' in direction 'd' according to 'grid' using 
    'imMask' as a mask (the propagation is performed only in 'd' direction).
    
    The function also returns the volume of the image 'imInout' after the
    build operation.
    
    'grid' value can be any 3D grid.
    """
    
    (width, height, length) = imInOut.getSize()
    if length!=len(imMask):
        mamba.raiseExceptionOnError(core.MB_ERR_BAD_SIZE)
    imWrk = mamba.imageMb(imInOut[0])
    grid2D = grid.get2DGrid()
    scan = grid.convertFromDir(d,0)[0]
    volume = 0L
    if scan == 0:
        for i in range(length):
            vol = mamba.buildNeighbor(imMask[i], imInOut[i], dh, grid2D)
            volume += vol
    else:
        if scan == 1:
            startPlane, endPlane = 0, length - 1
        else:
            startPlane, endPlane = length - 1, 0
        for i in range(startPlane, endPlane, scan):
            mamba.logic(imInOut[i], imMask[i], imWrk, "sup")
            vol = mamba.computeVolume(imWrk)
            volume += vol
            td = grid.getTranDir(d)
            dh = grid.converFromDir(td,i+scan)[1]
            mamba.infNeighbor(imWrk, imInOut[i+scan], dh, grid2D)
        mamba.logic(imInOut[endPlane], imMask[endPlane], imInOut[endPlane], "sup")
        vol = mamba.computeVolume(imInOut[length - 1])
        volume += vol           
    return volume
    
    
