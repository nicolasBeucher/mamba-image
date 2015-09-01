"""
Test cases for the filtering functions found in the filter module of 
mamba package.

Python functions:
    alternateFilter
    fullAlternateFilter
    linearAlternateFilter
    autoMedian
    simpleLevelling
    strongLevelling
    largeHexagonalAlternateFilter
    largeDodecagonalAlternateFilter
    largeSquareAlternateFilter
    largeOctogonalAlternateFilter
"""

from mamba import *
import unittest
import random

class TestFilter(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
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
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        
    def _drawAlternated(self, imOut):
        (w,h) = imOut.getSize()
        imOut.reset()
        drawSquare(imOut, (0,h//2,w-1,h-1), 255)
        imOut.setPixel(255, (w//4,h//4))
        imOut.setPixel(0, (w//4,3*h//4))
        drawSquare(imOut, (w//2-1,h//4-1,w//2+1,h//4+1), 255)
        drawSquare(imOut, (w//2-1,3*h//4-1,w//2+1,3*h//4+1), 0)
        drawBox(imOut, (3*w//4-1,h//4-1,3*w//4+2,h//4+2), 255)
        drawBox(imOut, (3*w//4-2,h//4-2,3*w//4+3,h//4+3), 255)
        drawBox(imOut, (3*w//4-1,3*h//4-1,3*w//4+2,3*h//4+2), 0)
        drawBox(imOut, (3*w//4-2,3*h//4-2,3*w//4+3,3*h//4+3), 0)
        
    def testAlternateFilter(self):
        """Verifies the alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self._drawAlternated(self.im8_1)
        alternateFilter(self.im8_1, self.im8_2, 1, True, SQUARE3X3)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawSquare(self.im8_3, (w//2-1,h//4-1,w//2+1,h//4+1), 255)
        drawSquare(self.im8_3, (w//2-1,3*h//4-1,w//2+1,3*h//4+1), 0)
        drawSquare(self.im8_3, (3*w//4-2,3*h//4-2,3*w//4+3,3*h//4+3), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        alternateFilter(self.im8_1, self.im8_2, 1, False, SQUARE3X3)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawSquare(self.im8_3, (w//2-1,h//4-1,w//2+1,h//4+1), 255)
        drawSquare(self.im8_3, (w//2-1,3*h//4-1,w//2+1,3*h//4+1), 0)
        drawSquare(self.im8_3, (3*w//4-2,h//4-2,3*w//4+3,h//4+3), 255)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testFullAlternateFilter(self):
        """Verifies the full alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self._drawAlternated(self.im8_1)
        fullAlternateFilter(self.im8_1, self.im8_2, 2, True, SQUARE3X3)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawSquare(self.im8_3, (3*w//4-2,3*h//4-2,3*w//4+3,3*h//4+3), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        fullAlternateFilter(self.im8_1, self.im8_2, 2, False, SQUARE3X3)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawSquare(self.im8_3, (3*w//4-2,h//4-2,3*w//4+3,h//4+3), 255)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testLargeSquareAlternateFilter(self):
        """Verifies the large square full alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self._drawAlternated(self.im8_1)
        largeSquareAlternateFilter(self.im8_1, self.im8_2, 0, 3, 1, True)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawSquare(self.im8_3, (3*w//4-2,3*h//4-2,3*w//4+3,3*h//4+3), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        largeSquareAlternateFilter(self.im8_1, self.im8_2, 0, 3, 1, False)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawSquare(self.im8_3, (3*w//4-2,h//4-2,3*w//4+3,h//4+3), 255)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testLargeHexagonalAlternateFilter(self):
        """Verifies the large hexagonal full alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.setPixel(255, (w//2,h//2))
        largeHexagonalDilate(self.im8_1, self.im8_2, 14)
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        largeHexagonalErode(self.im8_1, self.im8_1, 4)
        logic(self.im8_2, self.im8_1, self.im8_2, "inf")
        largeHexagonalAlternateFilter(self.im8_2, self.im8_1, 1, 6, 1, True)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 0)
        largeHexagonalAlternateFilter(self.im8_2, self.im8_1, 1, 6, 1, False)
        self.im8_3.setPixel(255, (w//2,h//2))
        largeHexagonalDilate(self.im8_3, self.im8_3, 14)
        (x,y) = compare(self.im8_3, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        
    def testLargeDodecagonalAlternateFilter(self):
        """Verifies the large dodecagonal full alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.setPixel(255, (w//2,h//2))
        largeDodecagonalDilate(self.im8_1, self.im8_2, 14)
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        largeDodecagonalErode(self.im8_1, self.im8_1, 4)
        logic(self.im8_2, self.im8_1, self.im8_2, "inf")
        largeDodecagonalAlternateFilter(self.im8_2, self.im8_1, 1, 6, 1, True)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 0)
        largeDodecagonalAlternateFilter(self.im8_2, self.im8_1, 1, 6, 1, False)
        v = computeVolume(self.im8_1)
        self.assertNotEqual(v, 0)
        
    def testLargeOctogonalAlternateFilter(self):
        """Verifies the large octogonal full alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.setPixel(255, (w//2,h//2))
        largeOctogonalDilate(self.im8_1, self.im8_2, 14)
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2))
        largeOctogonalErode(self.im8_1, self.im8_1, 4)
        logic(self.im8_2, self.im8_1, self.im8_2, "inf")
        largeOctogonalAlternateFilter(self.im8_2, self.im8_1, 1, 6, 1, True)
        v = computeVolume(self.im8_1)
        self.assertEqual(v, 0)
        largeOctogonalAlternateFilter(self.im8_2, self.im8_1, 1, 6, 1, False)
        self.im8_3.setPixel(255, (w//2,h//2))
        largeOctogonalDilate(self.im8_3, self.im8_3, 14)
        (x,y) = compare(self.im8_3, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        
    def _drawAlternatedSeg(self, imOut):
        (w,h) = imOut.getSize()
        imOut.reset()
        drawSquare(imOut, (0,h//2,w-1,h-1), 255)
        
        drawLine(imOut, (w//4,h//4-1,w//4,h//4+1), 255)
        drawLine(imOut, (w//4,3*h//4-1,w//4,3*h//4+1), 0)
        
        drawLine(imOut, (3*w//4-1,h//4-3,3*w//4-1,h//4+2), 255)
        drawLine(imOut, (3*w//4,h//4-3,3*w//4,h//4+2), 255)
        drawLine(imOut, (3*w//4,h//4-1,3*w//4,h//4  ), 0)
        drawLine(imOut, (3*w//4+1,h//4-3,3*w//4+1,h//4+2), 255)
        
        drawLine(imOut, (3*w//4-1,3*h//4-3,3*w//4-1,3*h//4+2), 0)
        drawLine(imOut, (3*w//4,3*h//4-3,3*w//4,3*h//4+2), 0)
        drawLine(imOut, (3*w//4,3*h//4-1,3*w//4,3*h//4  ), 255)
        drawLine(imOut, (3*w//4+1,3*h//4-3,3*w//4+1,3*h//4+2), 0)
        
    def testLinearAlternateFilter(self):
        """Verifies the linear alternate filter operator"""
        (w,h) = self.im8_1.getSize()
        
        self._drawAlternatedSeg(self.im8_1)
        linearAlternateFilter(self.im8_1, self.im8_2, 3, True, SQUARE)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawLine(self.im8_3, (3*w//4-1,h//4-3,3*w//4-1,h//4+2), 255)
        drawLine(self.im8_3, (3*w//4,h//4-2,3*w//4,h//4+1), 255)
        drawLine(self.im8_3, (3*w//4+1,h//4-3,3*w//4+1,h//4+2), 255)
        drawLine(self.im8_3, (3*w//4-1,3*h//4-3,3*w//4-1,3*h//4+2), 0)
        drawLine(self.im8_3, (3*w//4,3*h//4-3,3*w//4,3*h//4+2), 0)
        drawLine(self.im8_3, (3*w//4+1,3*h//4-3,3*w//4+1,3*h//4+2), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        linearAlternateFilter(self.im8_1, self.im8_2, 3, False, SQUARE)
        self.im8_3.reset()
        drawSquare(self.im8_3, (0,h//2,w-1,h-1), 255)
        drawLine(self.im8_3, (3*w//4-1,h//4-3,3*w//4-1,h//4+2), 255)
        drawLine(self.im8_3, (3*w//4,h//4-3,3*w//4,h//4+2), 255)
        drawLine(self.im8_3, (3*w//4+1,h//4-3,3*w//4+1,h//4+2), 255)
        drawLine(self.im8_3, (3*w//4-1,3*h//4-3,3*w//4-1,3*h//4+2), 0)
        drawLine(self.im8_3, (3*w//4,3*h//4-2,3*w//4,3*h//4+1), 0)
        drawLine(self.im8_3, (3*w//4+1,3*h//4-3,3*w//4+1,3*h//4+2), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testAutoMedian(self):
        """Tests the auto median filter operator"""
        (w,h) = self.im8_1.getSize()
        
        for n in range(1,6):
            value = n%2==1 and 255 or 0
            self.im8_1.fill(value)
            drawSquare(self.im8_1, (w//2-n,h//2-n,w//2+n,h//2+n), 100)
            for i in range(n+1):
                autoMedian(self.im8_1, self.im8_2, i, se=SQUARE3X3)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            self.im8_3.fill(value)
            autoMedian(self.im8_1, self.im8_2, n+1, se=SQUARE3X3)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testSimpleLevelling(self):
        """Verifies the simple levelling operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(21):
            drawLine(self.im8_1, (w//2-10+i, h//2-10, w//2-10+i, h//2+10), 101+i)
        
        for i in range(22):
            self.im8_4.reset()
            drawSquare(self.im8_4, (w//2-10, h//2-10, w//2+10, h//2+10), 100+i)
            self.im8_3.reset()
            for j in range(21):
                drawLine(self.im8_3, (w//2-10+j, h//2-10, w//2-10+j, h//2+10), min(101+j,100+i))
            
            simpleLevelling(self.im8_1, self.im8_4, self.im8_2, SQUARE)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "%d" % (i))
            
    def testStrongLevelling(self):
        """Verifies the strong levelling operator"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(21):
            drawLine(self.im8_1, (w//2-10+i, h//2-10, w//2-10+i, h//2+10), 101+i)
        
        for i in range(12):
            self.im8_3.reset()
            if i<11:
                for j in range(21-2*i):
                    drawLine(self.im8_3, (w//2-10+j, h//2-10, w//2-10+j, h//2+10), 101+j)
                for j in range(21-2*i, 21):
                    drawLine(self.im8_3, (w//2-10+j, h//2-10, w//2-10+j, h//2+10), 121-2*i)
            
            strongLevelling(self.im8_1, self.im8_2, i, (i%2==1), SQUARE)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "%d" % (i))

