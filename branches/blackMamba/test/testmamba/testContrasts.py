"""
Test cases for the gradient and tophat functions found in the contrasts module of 
mamba package.

Python functions and classes:
    gradient
    halfGradient
    whiteTopHat
    blackTopHat
    supWhiteTopHat
    supBlackTopHat
    regularisedGradient
"""

from mamba import *
import unittest
import random

class TestContrasts(unittest.TestCase):

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

    def testGradient(self):
        """Verifies the gradient operation"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//2-1, h//2-1, w//2+1, h//2+1), 255)
        self.im8_2.reset()
        drawBox(self.im8_2, (w//2-1, h//2-1, w//2+1, h//2+1), 255)
        drawBox(self.im8_2, (w//2-2, h//2-2, w//2+2, h//2+2), 255)
        gradient(self.im8_1, self.im8_1, se=SQUARE3X3)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testHalfGradient(self):
        """Verifies the half-gradient operation"""
        (w,h) = self.im8_1.getSize()
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//2-1, h//2-1, w//2+1, h//2+1), 255)
        self.im8_2.reset()
        drawBox(self.im8_2, (w//2-1, h//2-1, w//2+1, h//2+1), 255)
        halfGradient(self.im8_1, self.im8_1, type="intern", se=SQUARE3X3)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        self.im8_1.reset()
        drawSquare(self.im8_1, (w//2-1, h//2-1, w//2+1, h//2+1), 255)
        self.im8_2.reset()
        drawBox(self.im8_2, (w//2-2, h//2-2, w//2+2, h//2+2), 255)
        halfGradient(self.im8_1, self.im8_1, type="extern", se=SQUARE3X3)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def _growingSpot(self, imOut, n=None, se=DEFAULT_SE, inv=False):
        (w,h) = imOut.getSize()
        imOut.reset()
        prov = imageMb(imOut)
        if n==None:
            n = w
        x = 10
        size = 0
        while((x+size)<w and size<n):
            prov.reset()
            prov.setPixel(255, (x, h//2))
            dilate(prov, prov, size, se)
            logic(imOut, prov, imOut, "sup")
            x += 10+2*size
            size += 1
        if inv:
            negate(imOut, imOut)
        return size
        
    def testWhiteTopHat(self):
        """Tests the white top hat operation"""
        size = self._growingSpot(self.im8_1, se=HEXAGON)
        for i in range(size+1):
            whiteTopHat(self.im8_1, self.im8_2, i, se=HEXAGON)
            self._growingSpot(self.im8_3, i, se=HEXAGON)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        size = self._growingSpot(self.im8_1, se=SQUARE3X3)
        for i in range(size+1):
            whiteTopHat(self.im8_1, self.im8_2, i, se=SQUARE3X3)
            self._growingSpot(self.im8_3, i, se=SQUARE3X3)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testBlackTopHat(self):
        """Tests the black top hat operation"""
        size = self._growingSpot(self.im8_1, se=HEXAGON, inv=True)
        for i in range(size+1):
            blackTopHat(self.im8_1, self.im8_2, i, se=HEXAGON)
            self._growingSpot(self.im8_3, i, se=HEXAGON)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        size = self._growingSpot(self.im8_1, se=SQUARE3X3, inv=True)
        for i in range(size+1):
            blackTopHat(self.im8_1, self.im8_2, i, se=SQUARE3X3)
            self._growingSpot(self.im8_3, i, se=SQUARE3X3)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def _growingLineSpot(self, imOut, n=None, inv=False):
        (w,h) = imOut.getSize()
        imOut.reset()
        prov = imageMb(imOut)
        if n==None:
            n = w
        x = 10
        size = 0
        dir = 1
        while((x+size)<w and size<n):
            prov.reset()
            prov.setPixel(255, (x, h//2))
            linearDilate(prov, prov, dir, size, HEXAGONAL)
            logic(imOut, prov, imOut, "sup")
            x += 10+2*size
            size += 1
            dir = rotateDirection(dir, grid=HEXAGONAL)
        if inv:
            negate(imOut, imOut)
        return size
        
    def testSupWhiteTopHat(self):
        """Tests the sup white top hat operation"""
        size = self._growingLineSpot(self.im8_1)
        for i in range(size+1):
            supWhiteTopHat(self.im8_1, self.im8_2, i, grid=HEXAGONAL)
            self._growingLineSpot(self.im8_3, i)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def testSupBlackTopHat(self):
        """Tests the sup black top hat operation"""
        size = self._growingLineSpot(self.im8_1, inv=True)
        for i in range(size+1):
            supBlackTopHat(self.im8_1, self.im8_2, i, grid=HEXAGONAL)
            self._growingLineSpot(self.im8_3, i)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
        
    def _drawSlope(self, imOut, imRes, size):
        w,h = imOut.getSize()
        imOut.reset()
        for i in range(50,50+size):
            drawLine(imOut, (i,0,i,h-1), i-50)
        drawSquare(imOut, (i+1, 0, w-1, h-1), i-50)
        imRes.reset()
        for i in range(2-size%2):
            drawLine(imRes, (49+size//2+size%2+i,0,49+size//2+size%2+i,h-1), 1)
            
    def testRegularisedGradient(self):
        """Verifies the correct computation of a regularised gradient"""
        for i in range(10):
            m = random.randint(30,60)
            self._drawSlope(self.im8_1, self.im8_3, m)
            for n in range(20):
                regularisedGradient(self.im8_1, self.im8_2, n, SQUARE)
                vol = computeVolume(self.im8_2)
                if m<(4*n+1):
                    self.assertNotEqual(vol, 0, "m=%d : n=%d (vol %d)" % (m,n,vol))
                    (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
                    self.assertLess(x, 0)
                else:
                    self.assertEqual(vol, 0, "m=%d : n=%d (vol %d)" % (m,n,vol))

