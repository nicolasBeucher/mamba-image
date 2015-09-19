"""
Test cases for the large erosion and dilation functions found in the erodilLarge3D
module of mamba3D package.

Python functions:
    supFarNeighbor3D
    infFarNeighbor3D
    largeLinearDilate3D
    largeLinearErode3D
    largeCubeDilate
    largeCubeErode
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestErodilLarge3D(unittest.TestCase):

    def setUp(self):
        self.im8_1 = image3DMb(64,64,64,8)
        self.im8_2 = image3DMb(64,64,64,8)
        self.im8_3 = image3DMb(64,64,64,8)
        self.im8_4 = image3DMb(64,64,64,8)
        self.im8_5 = image3DMb(64,64,64,8)
        self.im8_6 = image3DMb(128,128,128,8)
        
    def tearDown(self):
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im8_6)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError,supFarNeighbor3D, self.im8_6, self.im8_2, 1,1)
        self.assertRaises(MambaError,infFarNeighbor3D, self.im8_6, self.im8_2, 1,1)
        
    def testSupFarNeighbor3D(self):
        """Verifies the supFarNeighbor3D operator"""
        (w, h, l) = self.im8_1.getSize()
        self.im8_1.reset()
        self.im8_1.setPixel(200, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                for amp in [1, 17, 29]:
                    linearDilate3D(self.im8_1, self.im8_2, d, amp-1, grid3D)
                    linearDilate3D(self.im8_2, self.im8_3, d, 1, grid3D)
                    diff3D(self.im8_3, self.im8_2, self.im8_3)
                    self.im8_2.reset()
                    supFarNeighbor3D(self.im8_1, self.im8_2, d, amp, grid3D)
                    (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_4)
                    self.assertLess(x, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
                # Test of filled edge (size 1 only because edges for other sizes are different)
                linearDilate3D(self.im8_1, self.im8_2, d, 1, grid3D, FILLED)
                diff3D(self.im8_2, self.im8_1, self.im8_2)
                self.im8_3.reset()
                supFarNeighbor3D(self.im8_1, self.im8_3, d, 1, grid3D, FILLED)
                (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_4)
                self.assertLess(x, 0, "grid3D %s, dir %d, filled edge : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
        
    def testInfFarNeighbor3D(self):
        """Verifies the infFarNeighbor3D operator"""   
        (w, h, l) = self.im8_1.getSize()
        self.im8_1.reset()
        self.im8_1.setPixel(200, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                for amp in [1, 17, 29]:
                    linearDilate3D(self.im8_1, self.im8_2, d, amp-1, grid3D)
                    linearDilate3D(self.im8_2, self.im8_3, d, 1, grid3D)
                    diff3D(self.im8_3, self.im8_2, self.im8_3)
                    negate3D(self.im8_3, self.im8_3)
                    negate3D(self.im8_1, self.im8_2)
                    self.im8_4.fill(255)
                    infFarNeighbor3D(self.im8_2, self.im8_4, d, amp, grid3D)
                    (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_5)
                    self.assertLess(x, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
                # Test of empty edge (size 1)
                negate3D(self.im8_1, self.im8_2)
                linearErode3D(self.im8_2, self.im8_3, d, 1, grid3D, EMPTY)
                self.im8_3.setPixel(255, (w//2, h//2, l//2))
                self.im8_4.fill(255)
                infFarNeighbor3D(self.im8_2, self.im8_4, d, 1, grid3D, EMPTY)
                (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_5)
                self.assertLess(x, 0, "grid3D %s, dir %d, empty edge : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
        
        
    def testLargeLinearDilate3D(self):
        """Tests the large linear 3D Dilation"""
        (w, h, l) = self.im8_1.getSize()
        self.im8_1.reset()
        self.im8_1.setPixel(200, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                for amp in [1, 17, 29]:
                    linearDilate3D(self.im8_1, self.im8_2, d, amp, grid3D)
                    largeLinearDilate3D(self.im8_1, self.im8_3, d, amp, grid3D)
                    (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_4)
                    self.assertLess(x, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
    
    def testLargeLinearErode3D(self):
        """Tests the large linear 3D erosion"""
        (w, h, l) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(50, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                for amp in [1, 17, 29]:
                    linearErode3D(self.im8_1, self.im8_2, d, amp, grid3D)
                    largeLinearErode3D(self.im8_1, self.im8_3, d, amp, grid3D)
                    (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_4)
                    self.assertLess(x, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
    
    def testLargeCubeDilate(self):
        """Tests dilations with large cubes"""
        (w, h, l) = self.im8_1.getSize()
        self.im8_1.reset()
        self.im8_1.setPixel(200, (w//2, h//2, l//2))
        for amp in [10, 17, 28]:
            largeCubeDilate(self.im8_1, self.im8_2, amp)
            cube = (w//2 - amp, h//2 -amp, l//2 + amp, w//2 + amp, h//2 + amp, l//2 - amp)
            drawCube(self.im8_3, cube, 200)
            (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_4)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))

    def testLargeCubeErode(self):
        """Tests erosions with large cubes"""
        (w, h, l) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(50, (w//2, h//2, l//2))
        for amp in [10, 17, 27]:
            largeCubeErode(self.im8_1, self.im8_2, amp)
            self.im8_3.fill(255)
            cube = (w//2 - amp, h//2 -amp, l//2 + amp, w//2 + amp, h//2 + amp, l//2 - amp)
            drawCube(self.im8_3, cube, 50)
            (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_4)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))       
 