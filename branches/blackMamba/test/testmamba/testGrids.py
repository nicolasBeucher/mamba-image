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
        self.assertEqual(repr(DEFAULT_GRID), "DEFAULT_GRID")
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
