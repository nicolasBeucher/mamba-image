"""
3D Grids handling and setting functions.

This module defines various functions related to grid configurations and 
computations. It also defines the 3D grids (cubic, face-centered cubic ...)
used with the 3D operators.
"""

# Contributors : Nicolas BEUCHER, Serge BEUCHER

import mamba3D as m3D
import mamba
import mamba.core as core

# 3D Grid support ##############################################################
class _grid3D:

    def getEncodedDirs(self, directions, zindex):
        # The direction in 3D corresponds to
        # various elements : the plane offset (0 if the
        # direction does not change it, 1 to go to the
        # previous offset, ...), the 2D direction as defined
        # by mamba in the offset plane
        # 
        # The input is the direction in the 3D grid and the
        # actual position of the plane of the starting point
        return {-1:0,0:0,1:0}
        
    def convertFromDir(self, direction, zindex):
        # The direction in 3D corresponds to
        # various elements : the plane offset (0 if the
        # direction does not change it, 1 to go to the
        # previous offset, ...), the 2D direction as defined
        # by mamba in the offset plane
        # 
        # The input is the direction in the 3D grid and the
        # actual position of the plane of the starting point
        return (0,0)
        
    def getShiftDirsList(self, d, amp, zindex):
        # Returns a list containing the directions, the amplitude of
        # the horizontal shifts and the 2D grid on which they are
        # performed to shift the plane at position 'zindex' in direction
        # 'd' of the grid with an amplitude 'amp'.
        # This list contains tuples (dh, amph, grid2D), each one
        # containing the horizontal direction 'dh', the amplitude of the
        # shift 'amph' and the 2D grid 'grid2D' on which this shift
        # is performed.
        return ((d, amp, mamba.SQUARE))
        
    def get2DGrid(self):
        # Used to indicates the 2D grid on which the 3D grid is based.
        return mamba.HEXAGONAL
        
    def getTranDir(self, d):
        # Returns the transposed direction of d in the grid
        return d
        
    def getZExtension(self):
        # Returns the biggest distance in plane a neighbor pixel can be
        # from the central point
        return 0
        
    def getDirections(self, withoutZero=False):
        # Returns the available directions on the grid
        return []
        
    def maxNeighbors(self):
        # Returns the maximum of neighbors a point can have in this grid
        return 0
        
    def getCValue(self):
        # Returns the C core value corresponding to the grid
        #(see type MB3D_grid_t). Returns MB3D_INVALID_GRID if the
        # grid as no corresponding C core grid value.
        return core.MB3D_INVALID_GRID
        
    def __repr__(self):
        # The name of the grid
        return "mamba3D.3D_GRID_NAME"
        

class _gridFCCubic3D(_grid3D):

    def __init__(self):
        self.name = "FACE_CENTER_CUBIC"
        self.basegrid = mamba.HEXAGONAL
                     #0     #1     #2     #3     #4     #5     #6
        listConv0 = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6),
                     #7      #8      #9
                     (-1,0), (-1,5), (-1,6),
                     #10    #11    #12
                     (1,6), (1,1), (1,0)
                    ]
                     #0     #1     #2     #3     #4     #5     #6
        listConv1 = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6),
                     #7      #8      #9
                     (-1,3), (-1,4), (-1,0),
                     #10    #11    #12
                     (1,5), (1,0), (1,4)
                    ]
                     #0     #1     #2     #3     #4     #5     #6
        listConv2 = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6),
                     #7      #8      #9
                     (-1,2), (-1,0), (-1,1),
                     #10    #11    #12
                     (1,0), (1,2), (1,3)
                    ]
        self.listConvs = [listConv0, listConv1, listConv2]
    
    def getEncodedDirs(self, directions, zindex):
        dirs = {-1:0,0:0,1:0}
        try:
            for d in directions:
                conv = self.listConvs[zindex%3][d]
                dirs[conv[0]] |= (1<<(conv[1]))
        except IndexError:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        return dirs
    
    def convertFromDir(self, direction, zindex):
        try:
            conversion = self.listConvs[zindex%3][direction]
        except IndexError:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        return conversion
    
    def getShiftDirsList(self, d, amp, zindex):
        if d < 0 or d > 12:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        elif d < 7:
            dirList = [(d, amp, mamba.HEXAGONAL)]
        elif d < 9:
            extraS = (((0,0,0),(1,0,0),(1,0,1)),((0,0,0),(0,1,0),(1,1,0)),((0,0,0),(0,0,1),(0,1,1)))
            hdList = [self.convertFromDir(d, i)[1] for i in range(3)]
            usedDir = [0, 1, 2]
            del usedDir[hdList.index(0)]
            amph = amp//3 + extraS[zindex%3][amp%3][usedDir[0]]
            dirList = [(hdList[usedDir[0]], amph, mamba.HEXAGONAL)]
            amph = amp//3 + extraS[zindex%3][amp%3][usedDir[1]]
            dirList.append((hdList[usedDir[1]], amph, mamba.HEXAGONAL))
        elif d == 9:
            extraS = (((0,0),(0,1),(1,0)),((0,0),(0,0),(0,1)),((0,0),(0,1),(0,1)))
            (sc, sh) = extraS[zindex%3][amp%3]
            nc = (amp//3 + sc) * 2
            dirList = [(1, nc, mamba.SQUARE)]
            if sh != 0:
                if (zindex%3) == 2:
                    hd = 1
                else:
                    hd = 6
                dirList.append((hd, 1, mamba.HEXAGONAL))
        elif d < 12:
            extraS = (((0,0,0),(1,0,0),(1,1,0)),((0,0,0),(0,1,0),(0,1,1)),((0,0,0),(0,0,1),(1,0,1)))
            hdList = [self.convertFromDir(d, i)[1] for i in range(3)]
            usedDir = [0, 1, 2]
            del usedDir[hdList.index(0)]
            amph = amp//3 + extraS[zindex%3][amp%3][usedDir[0]]
            dirList = [(hdList[usedDir[0]], amph, mamba.HEXAGONAL)]
            amph = amp//3 + extraS[zindex%3][amp%3][usedDir[1]]
            dirList.append((hdList[usedDir[1]], amph, mamba.HEXAGONAL))
        elif d == 12:
            extraS = (((0,0),(0,0),(0,1)),((0,0),(0,1),(1,0)),((0,0),(0,1),(0,1)))
            (sc, sh) = extraS[zindex%3][amp%3]
            nc = (amp//3 + sc) * 2
            dirList = [(5, nc, mamba.SQUARE)]
            if sh != 0:
                if (zindex%3) == 2:
                    hd = 3
                else:
                    hd = 4
                dirList.append((hd, 1, mamba.HEXAGONAL))
        return dirList
    
    def getZExtension(self):
        return 1
        
    def get2DGrid(self):
        return self.basegrid
    
    def getTranDir(self, d):
        if d==0:
            return 0
        elif d<7:
            return ((d+2)%6)+1
        elif d<10:
            return d+3
        else:
            return d-3
    
    def getDirections(self, withoutZero=False):
        return range(withoutZero and 1 or 0, len(self.listConvs[0]), 1)
    
    def maxNeighbors(self):
        return len(self.listConvs[0])-1
    
    def getCValue(self):
        return core.MB3D_FCC_GRID
    
    def __repr__(self):
        return "mamba3D."+self.name
    
    def __eq__(self, other):
        return other.getCValue()==core.MB3D_FCC_GRID
    
    def __ne__(self, other):
        return other.getCValue()!=core.MB3D_FCC_GRID
    
FACE_CENTER_CUBIC = _gridFCCubic3D()

class _gridCCubic3D(_grid3D):

    def __init__(self):
        self.name = "CENTER_CUBIC"
        self.basegrid = mamba.SQUARE
                     #0     #1     #2     #3     #4     #5     #6     #7     #8
        listConv0 = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8),
                     #9      #10     #11     #12
                     (-1,0), (-1,7), (-1,8), (-1,1),
                     #13    #14    #15    #16
                     (1,8), (1,1), (1,0), (1,7)
                    ]
                     #0     #1     #2     #3     #4     #5     #6     #7     #8
        listConv1 = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8),
                     #9      #10     #11     #12
                     (-1,4), (-1,5), (-1,0), (-1,3),
                     #13    #14    #15    #16
                     (1,0), (1,3), (1,4), (1,5)
                    ]
        self.listConvs = [listConv0, listConv1]
    
    def getEncodedDirs(self, directions, zindex):
        dirs = {-1:0,0:0,1:0}
        try:
            for d in directions:
                conv = self.listConvs[zindex%2][d]
                dirs[conv[0]] |= (1<<(conv[1]))
        except IndexError:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        return dirs
    
    def convertFromDir(self, direction, zindex):
        try:
            conversion = self.listConvs[zindex%2][direction]
        except IndexError:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        return conversion
    
    def getShiftDirsList(self, d, amp, zindex):
        if d < 0 or d > 16:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        elif d < 9:
            dirList = [(d, amp, mamba.SQUARE)]
        else:
            dirList =[]
            dh1 = self.convertFromDir(d, 0)[1]
            if dh1!=0:
                amph1 = amp//2 + (amp%2)*(1 - zindex%2)
                dirList.append((dh1, amph1, mamba.SQUARE))
            dh2 = self.convertFromDir(d, 1)[1]
            if dh2!=0:
                amph2 = amp//2 + (amp%2)*(zindex%2)
                dirList.append((dh2, amph2, mamba.SQUARE))
        return dirList
        
    def getZExtension(self):
        return 1
        
    def get2DGrid(self):
        return self.basegrid
    
    def getTranDir(self, d):
        if d==0:
            return 0
        elif d<9:
            return ((d+3)%8)+1
        elif d<13:
            return d+4
        else:
            return d-4
    
    def getDirections(self, withoutZero=False):
        return range(withoutZero and 1 or 0, 17, 1)
    
    def maxNeighbors(self):
        return 16
    
    def getCValue(self):
        return core.MB3D_INVALID_GRID
    
    def __repr__(self):
        return "mamba3D."+self.name
    
    def __eq__(self, other):
        comp  = other.getCValue()==core.MB3D_INVALID_GRID
        comp &= other.maxNeighbors()==16
        return comp
    
    def __ne__(self, other):
        comp  = other.getCValue()==core.MB3D_INVALID_GRID
        comp &= other.maxNeighbors()==16
        return not comp

CENTER_CUBIC = _gridCCubic3D()

class _gridCubic3D(_grid3D):

    def __init__(self):
        self.name = "CUBIC"
        self.basegrid = mamba.SQUARE
        self.transpDict={
            0:0,1:5,5:1,2:6,6:2,3:7,7:3,4:8,8:4,
            9:18,18:9,19:14,14:19,20:15,15:20,
            21:16,16:21,22:17,17:22,23:10,10:23,
            24:11,11:24,25:12,12:25,26:13,13:26
            }
    
    def getEncodedDirs(self, directions, zindex):
        dirs = {-1:0,0:0,1:0}
        for d in directions:
            if d>26 or d<0:
                mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
            if d<9:
                dirs[0] |= (1<<d)
            elif d<18:
                dirs[-1] |= (1<<(d-9))
            else:
                dirs[1] |= (1<<(d-18))
        return dirs
    
    def convertFromDir(self, direction, zindex):
        if direction>26 or direction<0:
            mamba.raiseExceptionOnError(core.MB_ERR_BAD_DIRECTION)
        if direction<9:
            return (0,direction)
        elif direction<18:
            return (-1,direction-9)
        else:
            return (1,direction-18)
    
    def getShiftDirsList(self, d, amp, zindex):
        dh = self.convertFromDir(d, 0)[1]
        return [(dh, amp, mamba.SQUARE)]
        
    def getZExtension(self):
        return 1
        
    def get2DGrid(self):
        return self.basegrid
    
    def getTranDir(self, d):
        return self.transpDict[d]
    
    def getDirections(self, withoutZero=False):
        return range(withoutZero and 1 or 0, 27, 1)
    
    def maxNeighbors(self):
        return 26
    
    def getCValue(self):
        return core.MB3D_CUBIC_GRID
    
    def __repr__(self):
        return "mamba3D."+self.name
    
    def __eq__(self, other):
        return other.getCValue()==core.MB3D_CUBIC_GRID
    
    def __ne__(self, other):
        return other.getCValue()!=core.MB3D_CUBIC_GRID

CUBIC = _gridCubic3D()
        
class _gridDefault3D(_grid3D):

    def __init__(self):
        self.name = "DEFAULT_GRID3D"
        self.proxyGrid = None
    
    def setProxyGrid(self, grid):
        if isinstance(grid, _grid3D):
            self.proxyGrid = grid
        else:
            raise ValueError("Invalid 3D grid for default")
    
    def getEncodedDirs(self, directions, zindex):
        return self.proxyGrid.getEncodedDirs(directions,zindex)
    
    def convertFromDir(self, direction, zindex):
        return self.proxyGrid.convertFromDir(direction,zindex)
    
    def getShiftDirsList(self, d, amp, zindex):
        return self.proxyGrid.getShiftDirsList(d, amp, zindex)
        
    def getZExtension(self):
        return self.proxyGrid.getZExtension()
        
    def get2DGrid(self):
        return self.proxyGrid.get2DGrid()
    
    def getTranDir(self, d):
        return self.proxyGrid.getTranDir(d)
    
    def getDirections(self, withoutZero=False):
        return self.proxyGrid.getDirections(withoutZero)
    
    def maxNeighbors(self):
        return self.proxyGrid.maxNeighbors()
    
    def getCValue(self):
        return self.proxyGrid.getCValue()
    
    def __repr__(self):
        return repr(self.proxyGrid)

DEFAULT_GRID3D = _gridDefault3D()
DEFAULT_GRID3D.setProxyGrid(FACE_CENTER_CUBIC)

###############################################################################
# Public functions to deal with grids

def setDefaultGrid3D(grid):
    """
    This function will change the value of the default grid used in each 
    operator that needs to specify one.
    
    'grid' must be a valid 3D grid.
    
    You can of course manually change the variable DEFAULT_GRID3D by yourself.
    Using this function is however recommended if you are not sure of what you 
    are doing.
    """
    global DEFAULT_GRID3D
    DEFAULT_GRID3D.setProxyGrid(grid)

def getDirections3D(grid=DEFAULT_GRID3D, withoutZero=False):
    """
    Returns a range of all the possible directions available in 'grid' 
    (set to DEFAULT_GRID3D by default). If 'withoutZero' is set to True, the
    direction 0 is omitted.
    
    If the 'grid' value is incorrect, the function returns an empty list.
    """
    if isinstance(grid, _grid3D):
        return grid.getDirections(withoutZero)
    else:
        return []

def gridNeighbors3D(grid=DEFAULT_GRID3D):
    """
    Returns the number of neighbors of a point in 'grid'.
    
    If the 'grid' value is incorrect, the function returns 0.
    """
    if isinstance(grid, _grid3D):
        return grid.maxNeighbors()
    else:
        return 0
        
def transposeDirection3D(d, grid=DEFAULT_GRID3D):
    """
    Calculates the transposed (opposite) direction value of direction 'd' 
    """
    return grid.getTranDir(d)
    
