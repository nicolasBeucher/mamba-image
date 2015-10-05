"""
Test cases for the grids facilities functions found in the
grids3D module of mamba3D package.

Python functions:
    setDefaultGrid3D
    getDirections3D
    gridNeighbors3D
    transposeDirection3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestGrids3D(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def testDummyGrid(self):
        """Verifies the dummy grid class"""
        grid = grids3D._grid3D()
        
        self.assertEqual(grid.getEncodedDirs([], 1), {-1:0,0:0,1:0})
        self.assertEqual(grid.convertFromDir(1, 1), (0,0))
        self.assertEqual(grid.getShiftDirsList(1, 1, 1), (1, 1, SQUARE))
        self.assertEqual(grid.get2DGrid(), HEXAGONAL)
        self.assertEqual(grid.getTranDir(15), 15)
        self.assertEqual(grid.getZExtension(), 0)
        self.assertEqual(grid.getDirections(), [])
        self.assertEqual(grid.maxNeighbors(), 0)
        self.assertEqual(grid.getCValue(), core.MB3D_INVALID_GRID)
        self.assertEqual(repr(grid), "mamba3D.3D_GRID_NAME")
        
    def testFCCubicGrid(self):
        """Verifies the face center cubic grid"""
        grid = FACE_CENTER_CUBIC
        
        self.assertEqual(grid.getEncodedDirs(range(13), 0), {-1:0x61,0:0x7f,1:0x43})
        self.assertEqual(grid.getEncodedDirs(range(13), 1), {-1:0x19,0:0x7f,1:0x31})
        self.assertEqual(grid.getEncodedDirs(range(13), 2), {-1:0x7,0:0x7f,1:0xd})
        self.assertRaises(MambaError,grid.getEncodedDirs,[14],0)
        self.assertRaises(MambaError,grid.getShiftDirsList,13,1,1)
        self.assertEqual(grid.convertFromDir(1, 0), (0,1))
        self.assertEqual(grid.convertFromDir(1, 1), (0,1))
        self.assertEqual(grid.convertFromDir(1, 2), (0,1))
        self.assertEqual(grid.convertFromDir(7, 0), (-1,0))
        self.assertEqual(grid.convertFromDir(7, 1), (-1,3))
        self.assertEqual(grid.convertFromDir(7, 2), (-1,2))
        self.assertRaises(MambaError,grid.convertFromDir,13,0)
        self.assertEqual(grid.get2DGrid(), HEXAGONAL)
        self.assertEqual(grid.getTranDir(1), 4)
        self.assertEqual(grid.getTranDir(7), 10)
        self.assertEqual(grid.getTranDir(8), 11)
        self.assertEqual(grid.getTranDir(9), 12)
        self.assertEqual(grid.getZExtension(), 1)
        self.assertEqual(grid.getDirections(), range(13))
        self.assertEqual(grid.maxNeighbors(), 12)
        self.assertEqual(grid.getCValue(), core.MB3D_FCC_GRID)
        self.assertEqual(repr(grid), "mamba3D.FACE_CENTER_CUBIC")
        
    def testCCubicGrid(self):
        """Verifies the center cubic grid"""
        grid = CENTER_CUBIC
        
        self.assertEqual(grid.getEncodedDirs(range(17), 0), {-1:0x183,0:0x1ff,1:0x183})
        self.assertEqual(grid.getEncodedDirs(range(17), 1), {-1:0x39,0:0x1ff,1:0x39})
        self.assertRaises(MambaError,grid.getEncodedDirs,[17],0)
        self.assertEqual(grid.convertFromDir(1, 0), (0,1))
        self.assertEqual(grid.convertFromDir(1, 1), (0,1))
        self.assertEqual(grid.convertFromDir(1, 2), (0,1))
        self.assertEqual(grid.convertFromDir(9, 0), (-1,0))
        self.assertEqual(grid.convertFromDir(9, 1), (-1,4))
        self.assertEqual(grid.convertFromDir(9, 2), (-1,0))
        self.assertRaises(MambaError,grid.convertFromDir,17,0)
        self.assertRaises(MambaError,grid.getShiftDirsList,17,1,1)
        self.assertEqual(grid.get2DGrid(), SQUARE)
        self.assertEqual(grid.getTranDir(0), 0)
        self.assertEqual(grid.getTranDir(1), 5)
        self.assertEqual(grid.getTranDir(9), 13)
        self.assertEqual(grid.getTranDir(10), 14)
        self.assertEqual(grid.getTranDir(15), 11)
        self.assertEqual(grid.getTranDir(12), 16)
        self.assertEqual(grid.getZExtension(), 1)
        self.assertEqual(grid.getDirections(), range(17))
        self.assertEqual(grid.maxNeighbors(), 16)
        self.assertEqual(grid.getCValue(), core.MB3D_INVALID_GRID)
        self.assertEqual(repr(grid), "mamba3D.CENTER_CUBIC")
        
    def testCubicGrid(self):
        """Verifies the cubic grid"""
        grid = CUBIC
        
        self.assertEqual(grid.getEncodedDirs(range(27), 0), {-1:0x1ff,0:0x1ff,1:0x1ff})
        self.assertRaises(MambaError,grid.getEncodedDirs,[27],0)
        for i in range(27):
            if i>=18:
                res = (1,i-18)
            elif i>=9:
                res = (-1,i-9)
            else:
                res = (0,i)
            self.assertEqual(grid.convertFromDir(i, 0), res)
            self.assertEqual(grid.convertFromDir(i, 1), res)
            self.assertEqual(grid.convertFromDir(i, 2), res)
        self.assertRaises(MambaError,grid.convertFromDir,27,0)
        self.assertEqual(grid.get2DGrid(), SQUARE)
        self.assertEqual(grid.getTranDir(1), 5)
        self.assertEqual(grid.getTranDir(9), 18)
        self.assertEqual(grid.getTranDir(14), 19)
        self.assertEqual(grid.getZExtension(), 1)
        self.assertEqual(grid.getDirections(), range(27))
        self.assertEqual(grid.maxNeighbors(), 26)
        self.assertEqual(grid.getCValue(), core.MB3D_CUBIC_GRID)
        self.assertEqual(repr(grid), "mamba3D.CUBIC")
        
    def testDefaultGrid(self):
        """Verifies the default grid"""
        grid = DEFAULT_GRID3D
        
        self.assertEqual(grid.getEncodedDirs(range(13), 0), {-1:0x61,0:0x7f,1:0x43})
        self.assertEqual(grid.getEncodedDirs(range(13), 1), {-1:0x19,0:0x7f,1:0x31})
        self.assertEqual(grid.getEncodedDirs(range(13), 2), {-1:0x7,0:0x7f,1:0xd})
        self.assertRaises(MambaError,grid.getEncodedDirs,[14],0)
        self.assertEqual(grid.convertFromDir(1, 0), (0,1))
        self.assertEqual(grid.convertFromDir(1, 1), (0,1))
        self.assertEqual(grid.convertFromDir(1, 2), (0,1))
        self.assertEqual(grid.convertFromDir(7, 0), (-1,0))
        self.assertEqual(grid.convertFromDir(7, 1), (-1,3))
        self.assertEqual(grid.convertFromDir(7, 2), (-1,2))
        self.assertEqual(grid.get2DGrid(), HEXAGONAL)
        self.assertEqual(grid.getTranDir(1), 4)
        self.assertEqual(grid.getTranDir(7), 10)
        self.assertEqual(grid.getTranDir(8), 11)
        self.assertEqual(grid.getTranDir(9), 12)
        self.assertEqual(grid.getZExtension(), 1)
        self.assertEqual(grid.getDirections(), range(13))
        self.assertEqual(grid.maxNeighbors(), 12)
        self.assertEqual(grid.getCValue(), core.MB3D_FCC_GRID)
        self.assertEqual(repr(grid), "mamba3D.FACE_CENTER_CUBIC")
        
    def testSetDefaultGrid3D(self):
        """Verifies that modification of the default 3D grid works"""
        self.assertRaises(ValueError, setDefaultGrid3D, 0)
        setDefaultGrid3D(CUBIC)
        grid = DEFAULT_GRID3D
        self.assertTrue(grid==CUBIC)
        self.assertFalse(grid==CENTER_CUBIC)
        self.assertFalse(grid==FACE_CENTER_CUBIC)
        self.assertFalse(grid!=CUBIC)
        self.assertTrue(grid!=CENTER_CUBIC)
        self.assertTrue(grid!=FACE_CENTER_CUBIC)
        self.assertEqual(grid.getShiftDirsList(1,1,1), [(1,1,SQUARE)])
        self.assertEqual(grid.getShiftDirsList(10,1,1), [(1,1,SQUARE)])
        self.assertEqual(grid.getShiftDirsList(19,1,1), [(1,1,SQUARE)])
        self.assertEqual(grid.getEncodedDirs(range(27), 0), {-1:0x1ff,0:0x1ff,1:0x1ff})
        self.assertRaises(MambaError,grid.getEncodedDirs,[27],0)
        for i in range(27):
            if i>=18:
                res = (1,i-18)
            elif i>=9:
                res = (-1,i-9)
            else:
                res = (0,i)
            self.assertEqual(grid.convertFromDir(i, 0), res)
            self.assertEqual(grid.convertFromDir(i, 1), res)
            self.assertEqual(grid.convertFromDir(i, 2), res)
        self.assertEqual(grid.get2DGrid(), SQUARE)
        self.assertEqual(grid.getTranDir(1), 5)
        self.assertEqual(grid.getTranDir(9), 18)
        self.assertEqual(grid.getTranDir(14), 19)
        self.assertEqual(grid.getZExtension(), 1)
        self.assertEqual(grid.getDirections(), range(27))
        self.assertEqual(grid.maxNeighbors(), 26)
        self.assertEqual(grid.getCValue(), core.MB3D_CUBIC_GRID)
        self.assertEqual(repr(grid), "mamba3D.CUBIC")

        setDefaultGrid3D(CENTER_CUBIC)
        self.assertFalse(grid==CUBIC)
        self.assertTrue(grid==CENTER_CUBIC)
        self.assertFalse(grid==FACE_CENTER_CUBIC)
        self.assertTrue(grid!=CUBIC)
        self.assertFalse(grid!=CENTER_CUBIC)
        self.assertTrue(grid!=FACE_CENTER_CUBIC)
        
        setDefaultGrid3D(FACE_CENTER_CUBIC)
        self.assertFalse(grid==CUBIC)
        self.assertFalse(grid==CENTER_CUBIC)
        self.assertTrue(grid==FACE_CENTER_CUBIC)
        self.assertTrue(grid!=CUBIC)
        self.assertTrue(grid!=CENTER_CUBIC)
        self.assertFalse(grid!=FACE_CENTER_CUBIC)
        
    def testGetDirections3D(self):
        """Verifies that the directions are correctly returned"""
        dirs = getDirections3D(CUBIC)
        self.assertEqual(dirs, range(27))
        dirs = getDirections3D(CENTER_CUBIC)
        self.assertEqual(dirs, range(17))
        dirs = getDirections3D(FACE_CENTER_CUBIC)
        self.assertEqual(dirs, range(13))
        dirs = getDirections3D(0)
        self.assertEqual(dirs, [])
        
    def testGridNeighbors3D(self):
        """Verifies that the number of neighbor are correctly returned"""
        nb = gridNeighbors3D(CUBIC)
        self.assertEqual(nb, 26)
        nb = gridNeighbors3D(CENTER_CUBIC)
        self.assertEqual(nb, 16)
        nb = gridNeighbors3D(FACE_CENTER_CUBIC)
        self.assertEqual(nb, 12)
        nb = gridNeighbors3D(0)
        self.assertEqual(nb, 0)
    
    def testTransposeDirection3D(self):
        """Verifies that the direction transposition"""
        d = transposeDirection3D(7)
        self.assertEqual(d, 10)

