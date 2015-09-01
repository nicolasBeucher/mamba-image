"""
Test cases for the functions implementing geodesic operators found in the 
geodesy module of mamba package.

Python functions and classes:
    minima
    maxima
    minDynamics
    maxDynamics
    deepMinima
    highMaxima
    maxPartialBuild
    minPartialBuild
"""

from mamba import *
import unittest
import random

class TestGeodesy(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im32_4 = imageMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        
    def _drawRandomExtrema(self,imOut, imRes, lh=1, ext="min"):
        imRes.reset()
        mv = computeMaxRange(imOut)[1]
        if ext=="min":
            imOut.fill(mv)
        else:
            imOut.reset()
            
        (w,h) = imOut.getSize()
        for xi in range(0,w-3,3):
            vi = random.randint(1,mv)
            hi = vi-random.randint(0,vi)
            yi = random.randint(1,h-2)
            if ext=="min":
                imOut.setPixel(mv-vi+hi, (xi+1,yi))
                imOut.setPixel(mv-vi, (xi,yi))
            else:
                imOut.setPixel(vi-hi, (xi+1,yi))
                imOut.setPixel(vi, (xi,yi))
            if hi<lh and vi-hi>0:
                imRes.setPixel(1, (xi+1,yi))
            imRes.setPixel(1, (xi,yi))
        
    def testMinima8(self):
        """Verifies the minima extraction operator on greyscale image"""
        for i in range(1, 10):
            self._drawRandomExtrema(self.im8_1, self.im1_1, lh=i, ext="min")
            minima(self.im8_1, self.im1_2, i)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d" %(i,x,y))
        
    def testMinima32(self):
        """Verifies the minima extraction operator on 32-bit image"""
        for i in range(1, 10):
            self._drawRandomExtrema(self.im32_1, self.im1_1, lh=i, ext="min")
            minima(self.im32_1, self.im1_2, i)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d" %(i,x,y))
        
    def testMaxima8(self):
        """Verifies the maxima extraction operator on greyscale image"""
        for i in range(1, 10):
            self._drawRandomExtrema(self.im8_1, self.im1_1, lh=i, ext="max")
            maxima(self.im8_1, self.im1_2, i)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d" %(i))
        
    def testMaxima32(self):
        """Verifies the maxima extraction operator on 32-bit image"""
        for i in range(1, 10):
            self._drawRandomExtrema(self.im32_1, self.im1_1, lh=i, ext="max")
            maxima(self.im32_1, self.im1_2, i)
            (x,y) = compare(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d" %(i))
            
    def _drawBaseImage(self, imOut):
        (w,h) = imOut.getSize()
        drawSquare(imOut, (0,0,w//4,h-1), 50)
        drawSquare(imOut, (w//4+1,0,w//4+20,h-1),100)
        drawSquare(imOut, (w//4+21,0,3*w//4,h-1), 70)
        drawSquare(imOut, (3*w//4+1,0,3*w//4+20,h-1),110)
        drawSquare(imOut, (3*w//4+21,0,255,h-1),50)
        return (w,h)
        
    def testMinDynamics8(self):
        """Verifies the dynamic minima function on greyscale image"""
        (w,h) = self._drawBaseImage(self.im8_1)
        negate(self.im8_1, self.im8_1)
        minDynamics(self.im8_1, self.im1_1, 30, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        minDynamics(self.im8_1, self.im1_1, 40, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMinDynamics32(self):
        """Verifies the dynamic minima function on 32-bit image"""
        (w,h) = self._drawBaseImage(self.im32_1)
        negate(self.im32_1, self.im32_1)
        minDynamics(self.im32_1, self.im1_1, 30, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        minDynamics(self.im32_1, self.im1_1, 40, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMaxDynamics8(self):
        """Verifies the dynamic maxima function on greyscale image"""
        (w,h) = self._drawBaseImage(self.im8_1)
        maxDynamics(self.im8_1, self.im1_1, 30, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        maxDynamics(self.im8_1, self.im1_1, 40, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMaxDynamics32(self):
        """Verifies the dynamic maxima function on 32-bit image"""
        (w,h) = self._drawBaseImage(self.im32_1)
        maxDynamics(self.im32_1, self.im1_1, 30, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        maxDynamics(self.im32_1, self.im1_1, 40, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testDeepMinima8(self):
        """Verifies the deep minima function on greyscale image"""
        (w,h) = self._drawBaseImage(self.im8_1)
        negate(self.im8_1, self.im8_1)
        deepMinima(self.im8_1, self.im1_1, 29, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        deepMinima(self.im8_1, self.im1_1, 30, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testDeepMinima32(self):
        """Verifies the deep minima function on 32-bit image"""
        (w,h) = self._drawBaseImage(self.im32_1)
        negate(self.im32_1, self.im32_1)
        deepMinima(self.im32_1, self.im1_1, 29, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        deepMinima(self.im32_1, self.im1_1, 30, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testHighMaxima8(self):
        """Verifies the high maxima function on greyscale image"""
        (w,h) = self._drawBaseImage(self.im8_1)
        highMaxima(self.im8_1, self.im1_1, 29, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        highMaxima(self.im8_1, self.im1_1, 30, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testHighMaxima32(self):
        """Verifies the high maxima function on 32-bit image"""
        (w,h) = self._drawBaseImage(self.im32_1)
        highMaxima(self.im32_1, self.im1_1, 29, SQUARE)
        self.im1_2.reset()
        drawSquare(self.im1_2, (w//4+1,0,w//4+20,h-1),1)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        highMaxima(self.im32_1, self.im1_1, 30, SQUARE)
        drawSquare(self.im1_2, (3*w//4+1,0,3*w//4+20,h-1),1)
        (x,y) = compare(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMaxPartialBuild(self):
        """Verifies the maxima partial build operator"""
        (w,h) = self._drawBaseImage(self.im8_1)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2,0,w-1,h-1), 1)
        maxPartialBuild(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        drawSquare(self.im8_3, (0,0,w//4,h-1), 50)
        drawSquare(self.im8_3, (w//4+1,0,w//4+20,h-1),70)
        drawSquare(self.im8_3, (w//4+21,0,3*w//4,h-1), 70)
        drawSquare(self.im8_3, (3*w//4+1,0,3*w//4+20,h-1),110)
        drawSquare(self.im8_3, (3*w//4+21,0,255,h-1),50)
        (x,y) = compare(self.im8_3,self.im8_2,self.im8_3)
        self.assertLess(x, 0)
        
    def testMinPartialBuild(self):
        """Verifies the minima partial build operator"""
        (w,h) = self._drawBaseImage(self.im8_1)
        negate(self.im8_1, self.im8_1)
        self.im1_1.reset()
        drawSquare(self.im1_1, (w//2,0,w-1,h-1), 1)
        minPartialBuild(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        drawSquare(self.im8_3, (0,0,w//4,h-1), 50)
        drawSquare(self.im8_3, (w//4+1,0,w//4+20,h-1),70)
        drawSquare(self.im8_3, (w//4+21,0,3*w//4,h-1), 70)
        drawSquare(self.im8_3, (3*w//4+1,0,3*w//4+20,h-1),110)
        drawSquare(self.im8_3, (3*w//4+21,0,255,h-1),50)
        negate(self.im8_3, self.im8_3)
        (x,y) = compare(self.im8_3,self.im8_2,self.im8_3)
        self.assertLess(x, 0)

