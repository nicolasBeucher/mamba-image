"""
Test cases for the grid functions found in mamba.

These tests cover all the functions that are not performing any computations.
    
Python function:
    getDirections
    gridNeighbors
    setDefaultGrid
    rotateDirection
    transposeDirection
"""

from mamba import *
import unittest
import random
from PIL import Image

class TestVarious(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
            
    def testGridAndEdgeRepr(self):
        """Verifies that the representation of the grid and edge value is correct"""
        self.assertEqual(repr(EMPTY), "EMPTY")
        self.assertEqual(repr(FILLED), "FILLED")
        self.assertEqual(repr(HEXAGONAL), "HEXAGONAL")
        self.assertEqual(repr(SQUARE), "SQUARE")
        self.assertEqual(repr(DEFAULT_GRID), "HEXAGONAL")
        DEFAULT_GRID.id = 40
        DEFAULT_GRID.default = False
        self.assertEqual(repr(DEFAULT_GRID), "")
        DEFAULT_GRID.default = True
        setDefaultGrid(HEXAGONAL)
        id = EMPTY.id
        EMPTY.id = 40
        self.assertEqual(repr(EMPTY), "")
        EMPTY.id = id
        
    def testSetDefaultGrid(self):
        """Tests that modifying the default grid is correctly taken into account"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(255, (w//2,h//2))
        setDefaultGrid(SQUARE)
        supNeighbor(self.im8_1, self.im8_1, 1<<2)
        v = self.im8_1.getPixel((w//2-1,h//2+1))
        self.assertEqual(v, 255)
        v = self.im8_1.getPixel((w//2-1,h//2))
        self.assertEqual(v, 0)
        self.im8_1.reset()
        self.im8_1.setPixel(255, (w//2,h//2))
        setDefaultGrid(HEXAGONAL)
        supNeighbor(self.im8_1, self.im8_1, 1<<2)
        v = self.im8_1.getPixel((w//2-1,h//2+1))
        self.assertEqual(v, 0)
        v = self.im8_1.getPixel((w//2-1,h//2))
        self.assertEqual(v, 255)
        DEFAULT_GRID.id = 40
        self.assertRaises(ValueError, setDefaultGrid, DEFAULT_GRID)
        self.assertEqual(getDirections(), [])
        self.assertEqual(gridNeighbors(), 0)
        setDefaultGrid(HEXAGONAL)
        
    def testGridNeighbors(self):
        """Verifies that the number of neighbor are correctly returned"""
        nb = gridNeighbors(SQUARE)
        self.assertEqual(nb, 8)
        nb = gridNeighbors(HEXAGONAL)
        self.assertEqual(nb, 6)
        
    def testRotateDirection(self):
        """Verifies the direction rotation function"""
        self.assertEqual(rotateDirection(0, grid=SQUARE), 0)
        self.assertEqual(rotateDirection(1, grid=SQUARE), 2)
        self.assertEqual(rotateDirection(2, grid=SQUARE), 3)
        self.assertEqual(rotateDirection(3, grid=SQUARE), 4)
        self.assertEqual(rotateDirection(4, grid=SQUARE), 5)
        self.assertEqual(rotateDirection(5, grid=SQUARE), 6)
        self.assertEqual(rotateDirection(6, grid=SQUARE), 7)
        self.assertEqual(rotateDirection(7, grid=SQUARE), 8)
        self.assertEqual(rotateDirection(8, grid=SQUARE), 1)
        self.assertEqual(rotateDirection(0, grid=HEXAGONAL), 0)
        self.assertEqual(rotateDirection(1, grid=HEXAGONAL), 2)
        self.assertEqual(rotateDirection(2, grid=HEXAGONAL), 3)
        self.assertEqual(rotateDirection(3, grid=HEXAGONAL), 4)
        self.assertEqual(rotateDirection(4, grid=HEXAGONAL), 5)
        self.assertEqual(rotateDirection(5, grid=HEXAGONAL), 6)
        self.assertEqual(rotateDirection(6, grid=HEXAGONAL), 1)
    
    def testTransposeDirection(self):
        """Verifies that the direction transposition"""
        self.assertEqual(transposeDirection(0, grid=SQUARE), 0)
        self.assertEqual(transposeDirection(1, grid=SQUARE), 5)
        self.assertEqual(transposeDirection(2, grid=SQUARE), 6)
        self.assertEqual(transposeDirection(3, grid=SQUARE), 7)
        self.assertEqual(transposeDirection(4, grid=SQUARE), 8)
        self.assertEqual(transposeDirection(5, grid=SQUARE), 1)
        self.assertEqual(transposeDirection(6, grid=SQUARE), 2)
        self.assertEqual(transposeDirection(7, grid=SQUARE), 3)
        self.assertEqual(transposeDirection(8, grid=SQUARE), 4)
        self.assertEqual(transposeDirection(0, grid=HEXAGONAL), 0)
        self.assertEqual(transposeDirection(1, grid=HEXAGONAL), 4)
        self.assertEqual(transposeDirection(2, grid=HEXAGONAL), 5)
        self.assertEqual(transposeDirection(3, grid=HEXAGONAL), 6)
        self.assertEqual(transposeDirection(4, grid=HEXAGONAL), 1)
        self.assertEqual(transposeDirection(5, grid=HEXAGONAL), 2)
        self.assertEqual(transposeDirection(6, grid=HEXAGONAL), 3)
        
