"""
Test cases for the large erosion and dilation functions found in the erodilLarge
module of mamba package. Some functions of erodil module are also tested
here.

Python functions and classes:
    largeLinearErode
    largeLinearDilate
    largeHexagonalErode
    largeHexagonalDilate
    largeSquareErode
    largeSquareDilate
    largeDodecagonalErode
    largeDodecagonalDilate
    largeOctogonalErode
    largeOctogonalDilate
"""

from mamba import *
import unittest
import random

class TestErodilLarge(unittest.TestCase):

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
        
    def testLargeLinearErode(self):
        """Verifies the large linear erosion"""
        (w,h) = self.im8_1.getSize()
        for d in getDirections():
            for n in range(1, 150, 10):
                self.im8_1.fill(255)
                self.im8_1.setPixel(0, (w//2,h//2))
                self.im8_2.fill(255)
                self.im8_2.setPixel(0, (w//2,h//2))
                linearErode(self.im8_1, self.im8_1, d, n)
                largeLinearErode(self.im8_2, self.im8_2, d, n)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
                self.im8_1.fill(255)
                self.im8_1.setPixel(0, (w//2,h//2))
                self.im8_2.fill(255)
                self.im8_2.setPixel(0, (w//2,h//2))
                linearErode(self.im8_1, self.im8_1, d, n, edge=EMPTY)
                largeLinearErode(self.im8_2, self.im8_2, d, n, edge=EMPTY)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
        
    def testLargeLinearDilate(self):
        """Verifies the large linear dilation"""
        (w,h) = self.im8_1.getSize()
        for d in getDirections():
            for n in range(1, 150, 10):
                self.im8_1.reset()
                self.im8_1.setPixel(255, (w//2,h//2))
                self.im8_2.reset()
                self.im8_2.setPixel(255, (w//2,h//2))
                linearDilate(self.im8_1, self.im8_1, d, n)
                largeLinearDilate(self.im8_2, self.im8_2, d, n)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
                self.im8_1.reset()
                self.im8_1.setPixel(255, (w//2,h//2))
                self.im8_2.reset()
                self.im8_2.setPixel(255, (w//2,h//2))
                linearDilate(self.im8_1, self.im8_1, d, n, edge=FILLED)
                largeLinearDilate(self.im8_2, self.im8_2, d, n, edge=FILLED)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            
    def testLargeHexagonalErode(self):
        """Verifies the large hexagonal erosion"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n, se=HEXAGON)
            largeHexagonalErode(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n, se=HEXAGON, edge=EMPTY)
            largeHexagonalErode(self.im8_2, self.im8_2, n, edge=EMPTY)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testLargeHexagonalDilate(self):
        """Verifies the large hexagonal dilation"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            dilate(self.im8_1, self.im8_1, n, se=HEXAGON)
            largeHexagonalDilate(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            dilate(self.im8_1, self.im8_1, n, se=HEXAGON, edge=FILLED)
            largeHexagonalDilate(self.im8_2, self.im8_2, n, edge=FILLED)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testLargeSquareErode(self):
        """Verifies the large square erosion"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n, se=SQUARE3X3)
            largeSquareErode(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            erode(self.im8_1, self.im8_1, n, se=SQUARE3X3, edge=EMPTY)
            largeSquareErode(self.im8_2, self.im8_2, n, edge=EMPTY)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testLargeSquareDilate(self):
        """Verifies the large square dilation"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            dilate(self.im8_1, self.im8_1, n, se=SQUARE3X3)
            largeSquareDilate(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            dilate(self.im8_1, self.im8_1, n, se=SQUARE3X3, edge=FILLED)
            largeSquareDilate(self.im8_2, self.im8_2, n, edge=FILLED)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testLargeDodecagonalErode(self):
        """Verifies the large dodecagonal erosion"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            dodecagonalErode(self.im8_1, self.im8_1, n)
            largeDodecagonalErode(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            dodecagonalErode(self.im8_1, self.im8_1, n, edge=EMPTY)
            largeDodecagonalErode(self.im8_2, self.im8_2, n, edge=EMPTY)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testLargeDodecagonalDilate(self):
        """Verifies the large dodecagonal dilation"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            dodecagonalDilate(self.im8_1, self.im8_1, n)
            largeDodecagonalDilate(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            dodecagonalDilate(self.im8_1, self.im8_1, n, edge=FILLED)
            largeDodecagonalDilate(self.im8_2, self.im8_2, n, edge=FILLED)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testLargeOctogonalErode(self):
        """Verifies the large octocagonal erosion"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            octogonalErode(self.im8_1, self.im8_1, n)
            largeOctogonalErode(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2))
            self.im8_2.fill(255)
            self.im8_2.setPixel(0, (w//2,h//2))
            octogonalErode(self.im8_1, self.im8_1, n, edge=EMPTY)
            largeOctogonalErode(self.im8_2, self.im8_2, n, edge=EMPTY)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testLargeOctogonalDilate(self):
        """Verifies the large octogonal dilation"""
        (w,h) = self.im8_1.getSize()
        for n in range(1, 150, 10):
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            octogonalDilate(self.im8_1, self.im8_1, n)
            largeOctogonalDilate(self.im8_2, self.im8_2, n)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2))
            self.im8_2.reset()
            self.im8_2.setPixel(255, (w//2,h//2))
            octogonalDilate(self.im8_1, self.im8_1, n, edge=FILLED)
            largeOctogonalDilate(self.im8_2, self.im8_2, n, edge=FILLED)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
            self.assertLess(x, 0)

