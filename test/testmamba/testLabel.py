"""
Test cases for the image labelling function.

The function only works with 32-bit image as output.

For every set of pixels in the input image (pixels set to a the same non zero
value that are connected), the output image is computed to give the entire
pixels set a value (its label) that is unique inside the image.

The result depends on grid and edge configurations.

Python function:
    label
    
C functions:
    MB_Label
"""

from mamba import *
import unittest
import random

class TestLabel(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im1s2_1 = imageMb(128,128,1)
        self.im32s2_1 = imageMb(128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im1s2_1)
        del(self.im32s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, label, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, label, self.im1_1, self.im8_2)
        #self.assertRaises(MambaError, label, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, label, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, label, self.im8_1, self.im8_2)
        #self.assertRaises(MambaError, label, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, label, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, label, self.im32_1, self.im8_2)
        #self.assertRaises(MambaError, label, self.im32_1, self.im32_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, label, self.im1s2_1, self.im32_1)
        self.assertRaises(MambaError, label, self.im1_1, self.im32s2_1)
        
    def testParameterRange(self):
        """Verifies that an incorrect parameter raises an exception"""
        for i in range(257, 1000):
            self.assertRaises(MambaError, label, self.im1_1, self.im32_2, 0, i)
        self.assertRaises(MambaError, label, self.im1_1, self.im32_2, 255, 254)

    def testComputationUniqueLabel1(self):
        """Labelling only one complex object"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im32_2.reset()
        
        for x in range(1,w-3,4):
            for hi in range(1,h-1):
                self.im1_1.setPixel(1, (x, hi))
                self.im32_2.setPixel(1, (x, hi))
            self.im1_1.setPixel(1, (x+1, hi))
            self.im32_2.setPixel(1, (x+1, hi))
            for hi in range(h-2,0,-1):
                self.im1_1.setPixel(1, (x+2, hi))
                self.im32_2.setPixel(1, (x+2, hi))
            self.im1_1.setPixel(1, (x+3, 1))
            self.im32_2.setPixel(1, (x+3, hi))
        
        n = label(self.im1_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 1)
        (x,y) = compare(self.im32_1, self.im32_2, self.im32_3)
        self.assertLess(x, 0)
        
        n = label(self.im1_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, 1)

    def testComputationUniqueLabel8(self):
        """Labelling only one complex object"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        
        vi = random.randint(1,255)
        for x in range(1,w-3,4):
            for hi in range(1,h-1):
                self.im8_1.setPixel(vi, (x, hi))
            self.im8_1.setPixel(vi, (x+1, hi))
            for hi in range(h-2,0,-1):
                self.im8_1.setPixel(vi, (x+2, hi))
            self.im8_1.setPixel(vi, (x+3, 1))
        
        n = label(self.im8_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 1)
        
        n = label(self.im8_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, 1)

    def testComputationUniqueLabel32(self):
        """Labelling only one complex object"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.reset()
        
        vi = random.randint(1,0xffffffff)
        for x in range(1,w-3,4):
            for hi in range(1,h-1):
                self.im32_1.setPixel(vi, (x, hi))
            self.im32_1.setPixel(vi, (x+1, hi))
            for hi in range(h-2,0,-1):
                self.im32_1.setPixel(vi, (x+2, hi))
            self.im32_1.setPixel(vi, (x+3, 1))
        
        n = label(self.im32_1, self.im32_2, grid=SQUARE)
        self.assertEqual(n, 1)
        
        n = label(self.im32_1, self.im32_2, grid=HEXAGONAL)
        self.assertEqual(n, 1)

    def testComputationMultipleLabel1(self):
        """Labelling numerous simple binary objects"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        
        n_exp = 0
        vol_exp = 0
        for wi in range(0,w-2,2):
            for hi in range(0,h-2,2):
                self.im1_1.setPixel(1, (wi,hi))
                n_exp += 1
                vol_exp += n_exp
        
        n = label(self.im1_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_1)
        self.assertEqual(vol, vol_exp)
        
        n = label(self.im1_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_1)
        self.assertEqual(vol, vol_exp)

    def testComputationMultipleLabel8(self):
        """Labelling numerous simple greyscale objects"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        
        n_exp = 0
        vol_exp = 0
        vi = random.randint(1,255)
        for wi in range(0,w-2,2):
            for hi in range(0,h-2,2):
                self.im8_1.setPixel(vi, (wi,hi))
                n_exp += 1
                vol_exp += n_exp
        
        n = label(self.im8_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_1)
        self.assertEqual(vol, vol_exp)
        
        n = label(self.im8_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_1)
        self.assertEqual(vol, vol_exp)
        
        self.im8_1.fill(5)
        
        n_exp = 1
        vol_exp = w*h
        vi = random.randint(6,255)
        for wi in range(1,w-2,2):
            for hi in range(1,h-2,2):
                self.im8_1.setPixel(vi, (wi,hi))
                n_exp += 1
                vol_exp += (n_exp-1)
        
        n = label(self.im8_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_1)
        self.assertEqual(vol, vol_exp)
        
        n = label(self.im8_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_1)
        self.assertEqual(vol, vol_exp)

    def testComputationMultipleLabel32(self):
        """Labelling numerous simple 32-bit objects"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.reset()
        
        n_exp = 0
        vol_exp = 0
        vi = random.randint(1,0xffffffff)
        for wi in range(0,w-2,2):
            for hi in range(0,h-2,2):
                self.im32_1.setPixel(vi, (wi,hi))
                n_exp += 1
                vol_exp += n_exp
        
        n = label(self.im32_1, self.im32_2, grid=SQUARE)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_2)
        self.assertEqual(vol, vol_exp)
        
        n = label(self.im32_1, self.im32_2, grid=HEXAGONAL)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_2)
        self.assertEqual(vol, vol_exp)
        
        self.im32_1.fill(137)
        
        n_exp = 1
        vol_exp = w*h
        vi = random.randint(256,0xffffffff)
        for wi in range(1,w-2,2):
            for hi in range(1,h-2,2):
                self.im32_1.setPixel(vi, (wi,hi))
                n_exp += 1
                vol_exp += n_exp-1
        
        n = label(self.im32_1, self.im32_2, grid=SQUARE)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_2)
        self.assertEqual(vol, vol_exp)
        
        n = label(self.im32_1, self.im32_2, grid=HEXAGONAL)
        self.assertEqual(n, n_exp)
        vol = computeVolume(self.im32_2)
        self.assertEqual(vol, vol_exp)

    def testComputationGridEffect1(self):
        """Verifies grid configuration on labelling"""
        self.im1_1.reset()
        
        # first 'object'
        self.im1_1.setPixel(1, (6,3))
        self.im1_1.setPixel(1, (5,4))
        self.im1_1.setPixel(1, (6,5))
        
        # second 'object'
        self.im1_1.setPixel(1, (4,8))
        self.im1_1.setPixel(1, (5,9))
        self.im1_1.setPixel(1, (4,10))
        
        n = label(self.im1_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 2)
        
        n = label(self.im1_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, 6)

        self.im1_1.reset()
        
        # object
        self.im1_1.setPixel(1, (3,5))
        self.im1_1.setPixel(1, (4,6))
        self.im1_1.setPixel(1, (5,5))
        
        n = label(self.im1_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 1)

    def testComputationGridEffect8(self):
        """Verifies grid configuration on labelling"""
        self.im8_1.reset()
        
        # first 'object'
        self.im8_1.setPixel(2, (6,3))
        self.im8_1.setPixel(2, (5,4))
        self.im8_1.setPixel(2, (6,5))
        
        # second 'object'
        self.im8_1.setPixel(127, (4,8))
        self.im8_1.setPixel(127, (5,9))
        self.im8_1.setPixel(127, (4,10))
        
        n = label(self.im8_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 2)
        
        n = label(self.im8_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, 6)

        self.im8_1.reset()
        
        # object
        self.im8_1.setPixel(1, (3,5))
        self.im8_1.setPixel(1, (4,6))
        self.im8_1.setPixel(1, (5,5))
        
        n = label(self.im8_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 1)

    def testComputationGridEffect32(self):
        """Verifies grid configuration on labelling"""
        self.im32_1.reset()
        
        # first 'object'
        self.im32_1.setPixel(2, (6,3))
        self.im32_1.setPixel(2, (5,4))
        self.im32_1.setPixel(2, (6,5))
        
        # second 'object'
        self.im32_1.setPixel(127, (4,8))
        self.im32_1.setPixel(127, (5,9))
        self.im32_1.setPixel(127, (4,10))
        
        n = label(self.im32_1, self.im32_2, grid=SQUARE)
        self.assertEqual(n, 2)
        
        n = label(self.im32_1, self.im32_2, grid=HEXAGONAL)
        self.assertEqual(n, 6)

        self.im32_1.reset()
        
        # object
        self.im32_1.setPixel(1, (3,5))
        self.im32_1.setPixel(1, (4,6))
        self.im32_1.setPixel(1, (5,5))
        
        n = label(self.im32_1, self.im32_2, grid=SQUARE)
        self.assertEqual(n, 1)

    def testComputationEdge1(self):
        """Verifies that objects touching the edge are correctly labelled"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        
        self.im1_1.setPixel(1, (0,0))
        self.im1_1.setPixel(1, (w-1,0))
        self.im1_1.setPixel(1, (0,h-1))
        self.im1_1.setPixel(1, (w-1,h-1))
        
        n = label(self.im1_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 4, "%d"%(n))
        
        n = label(self.im1_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, 4, "%d"%(n))

    def testComputationEdge8(self):
        """Verifies that objects touching the edge are correctly labelled"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        
        self.im8_1.setPixel(255, (0,0))
        self.im8_1.setPixel(255, (w-1,0))
        self.im8_1.setPixel(255, (0,h-1))
        self.im8_1.setPixel(255, (w-1,h-1))
        
        n = label(self.im8_1, self.im32_1, grid=SQUARE)
        self.assertEqual(n, 4, "%d"%(n))
        
        n = label(self.im8_1, self.im32_1, grid=HEXAGONAL)
        self.assertEqual(n, 4, "%d"%(n))

    def testComputationEdge32(self):
        """Verifies that objects touching the edge are correctly labelled"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.reset()
        
        self.im32_1.setPixel(5255, (0,0))
        self.im32_1.setPixel(5255, (w-1,0))
        self.im32_1.setPixel(5255, (0,h-1))
        self.im32_1.setPixel(5255, (w-1,h-1))
        
        n = label(self.im32_1, self.im32_2, grid=SQUARE)
        self.assertEqual(n, 4, "%d"%(n))
        
        n = label(self.im32_1, self.im32_2, grid=HEXAGONAL)
        self.assertEqual(n, 4, "%d"%(n))

    def testComputationRange1(self):
        """Labelling in the lower byte according to range specified"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        
        for wi in range(0,w-2,2):
            for hi in range(0,h-2,2):
                self.im1_1.setPixel(1, (wi,hi))
        
        n = label(self.im1_1, self.im32_1, 10, 230, grid=SQUARE)
        copyBytePlane(self.im32_1, 0, self.im8_1)
        l = list(range(256))
        l[0] = 10
        lookup(self.im8_1, self.im8_1, l)
        mi, ma = computeRange(self.im8_1)
        self.assertEqual(mi, 10)
        self.assertEqual(ma, 229)
        
        n = label(self.im1_1, self.im32_1, 10, 230, grid=HEXAGONAL)
        copyBytePlane(self.im32_1, 0, self.im8_1)
        l = list(range(256))
        l[0] = 10
        lookup(self.im8_1, self.im8_1, l)
        mi, ma = computeRange(self.im8_1)
        self.assertEqual(mi, 10)
        self.assertEqual(ma, 229)

    def testComputationRange8(self):
        """Labelling in the lower byte according to range specified"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        
        vi = random.randint(1,255)
        for wi in range(0,w-2,2):
            for hi in range(0,h-2,2):
                self.im8_1.setPixel(vi, (wi,hi))
        
        n = label(self.im8_1, self.im32_1, 10, 230, grid=SQUARE)
        copyBytePlane(self.im32_1, 0, self.im8_2)
        l = list(range(256))
        l[0] = 10
        lookup(self.im8_2, self.im8_2, l)
        mi, ma = computeRange(self.im8_2)
        self.assertEqual(mi, 10)
        self.assertEqual(ma, 229)
        
        n = label(self.im8_1, self.im32_1, 10, 230, grid=HEXAGONAL)
        copyBytePlane(self.im32_1, 0, self.im8_2)
        l = list(range(256))
        l[0] = 10
        lookup(self.im8_2, self.im8_2, l)
        mi, ma = computeRange(self.im8_2)
        self.assertEqual(mi, 10)
        self.assertEqual(ma, 229)

    def testComputationRange32(self):
        """Labelling in the lower byte according to range specified"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.reset()
        
        vi = random.randint(1,0xffffffff)
        for wi in range(0,w-2,2):
            for hi in range(0,h-2,2):
                self.im32_1.setPixel(vi, (wi,hi))
        
        n = label(self.im32_1, self.im32_2, 10, 230, grid=SQUARE)
        copyBytePlane(self.im32_2, 0, self.im8_2)
        l = list(range(256))
        l[0] = 10
        lookup(self.im8_2, self.im8_2, l)
        mi, ma = computeRange(self.im8_2)
        self.assertEqual(mi, 10)
        self.assertEqual(ma, 229)
        
        n = label(self.im32_1, self.im32_2, 10, 230, grid=HEXAGONAL)
        copyBytePlane(self.im32_2, 0, self.im8_2)
        l = list(range(256))
        l[0] = 10
        lookup(self.im8_2, self.im8_2, l)
        mi, ma = computeRange(self.im8_2)
        self.assertEqual(mi, 10)
        self.assertEqual(ma, 229)

