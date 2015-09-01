"""
Test cases for the extremum operators found in the extrema3D
module of mamba3D package. 

Python functions:
    minima3D
    maxima3D
    minDynamics3D
    maxDynamics3D
    deepMinima3D
    highMaxima3D
    maxPartialBuild3D
    minPartialBuild3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestGeodesy3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(64,64,64,1)
        self.im1_2 = image3DMb(64,64,64,1)
        self.im1_3 = image3DMb(64,64,64,1)
        self.im1_4 = image3DMb(64,64,64,1)
        self.im1_5 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(64,64,64,8)
        self.im8_2 = image3DMb(64,64,64,8)
        self.im8_3 = image3DMb(64,64,64,8)
        self.im8_4 = image3DMb(64,64,64,8)
        self.im8_5 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(64,64,64,32)
        self.im32_2 = image3DMb(64,64,64,32)
        self.im32_3 = image3DMb(64,64,64,32)
        self.im32_4 = image3DMb(64,64,64,32)
        self.im32_5 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im1_5)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        del(self.im32_5)
        
    def _drawRandomExtrema(self,imOut, imRes, lh=1, ext="min"):
        imRes.reset()
        (rd,ru) = computeMaxRange3D(imOut)
        if ext=="min":
            imOut.fill(ru)
        else:
            imOut.reset()
            
        (w,h,l) = imOut.getSize()
        for xi in range(0,w-3,3):
            vi = random.randint(1,ru)
            hi = vi-random.randint(0,vi)
            yi = random.randint(1,h-2)
            zi = random.randint(1,l-2)
            if ext=="min":
                imOut.setPixel(ru-vi+hi, (xi+1,yi,zi))
                imOut.setPixel(ru-vi, (xi,yi,zi))
            else:
                imOut.setPixel(vi-hi, (xi+1,yi,zi))
                imOut.setPixel(vi, (xi,yi,zi))
            if hi<lh and vi-hi>0:
                imRes.setPixel(1, (xi+1,yi,zi))
            imRes.setPixel(1, (xi,yi,zi))
        
    def testMinima3D_8(self):
        """Verifies the minima extraction 3D operator on 8-bit image"""
        for i in range(1, 2):
            self._drawRandomExtrema(self.im8_1, self.im1_1, lh=i, ext="min")
            minima3D(self.im8_1, self.im1_2, i)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testMaxima3D_8(self):
        """Verifies the maxima extraction 3D operator on 8-bit image"""
        for i in range(1, 2):
            self._drawRandomExtrema(self.im8_1, self.im1_1, lh=i, ext="max")
            maxima3D(self.im8_1, self.im1_2, i)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testMinima3D_32(self):
        """Verifies the minima extraction 3D operator on 32-bit image"""
        for i in range(1, 2):
            self._drawRandomExtrema(self.im32_1, self.im1_1, lh=i, ext="min")
            minima3D(self.im32_1, self.im1_2, i)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testMaxima3D_32(self):
        """Verifies the maxima extraction 3D operator on 32-bit image"""
        for i in range(1, 2):
            self._drawRandomExtrema(self.im32_1, self.im1_1, lh=i, ext="max")
            maxima3D(self.im32_1, self.im1_2, i)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
            
    def _drawBaseImage(self, imOut):
        (w,h,l) = imOut.getSize()
        for i in range(l//4):
            imOut[i].fill(50)
        for i in range(l//4,l//4+10):
            imOut[i].fill(100)
        for i in range(l//4+10,3*l//4):
            imOut[i].fill(70)
        for i in range(3*l//4,3*l//4+10):
            imOut[i].fill(110)
        for i in range(3*l//4+10,l):
            imOut[i].fill(50)
        return (w,h,l)
        
    def testMinDynamics3D_8(self):
        """Verifies the dynamic minima function on greyscale image"""
        (w,h,l) = self._drawBaseImage(self.im8_1)
        negate3D(self.im8_1, self.im8_1)
        minDynamics3D(self.im8_1, self.im1_1, 30, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        minDynamics3D(self.im8_1, self.im1_1, 40, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMinDynamics3D_32(self):
        """Verifies the dynamic minima function on 32-bit image"""
        (w,h,l) = self._drawBaseImage(self.im32_1)
        negate3D(self.im32_1, self.im32_1)
        minDynamics3D(self.im32_1, self.im1_1, 30, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        minDynamics3D(self.im32_1, self.im1_1, 40, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMaxDynamics3D_8(self):
        """Verifies the dynamic maxima function on greyscale image"""
        (w,h,l) = self._drawBaseImage(self.im8_1)
        maxDynamics3D(self.im8_1, self.im1_1, 30, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        maxDynamics3D(self.im8_1, self.im1_1, 40, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMaxDynamics3D_32(self):
        """Verifies the dynamic maxima function on 32-bit image"""
        (w,h,l) = self._drawBaseImage(self.im32_1)
        maxDynamics3D(self.im32_1, self.im1_1, 30, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        maxDynamics3D(self.im32_1, self.im1_1, 40, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testDeepMinima3D_8(self):
        """Verifies the deep minima function on greyscale image"""
        (w,h,l) = self._drawBaseImage(self.im8_1)
        negate3D(self.im8_1, self.im8_1)
        deepMinima3D(self.im8_1, self.im1_1, 29, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        deepMinima3D(self.im8_1, self.im1_1, 30, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testDeepMinima3D_32(self):
        """Verifies the deep minima function on 32-bit image"""
        (w,h,l) = self._drawBaseImage(self.im32_1)
        negate3D(self.im32_1, self.im32_1)
        deepMinima3D(self.im32_1, self.im1_1, 29, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        deepMinima3D(self.im32_1, self.im1_1, 30, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testHighMaxima3D_8(self):
        """Verifies the high maxima function on greyscale image"""
        (w,h,l) = self._drawBaseImage(self.im8_1)
        highMaxima3D(self.im8_1, self.im1_1, 29, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        highMaxima3D(self.im8_1, self.im1_1, 30, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testHighMaxima3D_32(self):
        """Verifies the high maxima function on 32-bit image"""
        (w,h,l) = self._drawBaseImage(self.im32_1)
        highMaxima3D(self.im32_1, self.im1_1, 29, CUBIC)
        self.im1_2.reset()
        for i in range(l//4,l//4+10):
            self.im1_2[i].fill(1)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        self.im1_2.reset()
        highMaxima3D(self.im32_1, self.im1_1, 30, CUBIC)
        for i in range(3*l//4,3*l//4+10):
            self.im1_2[i].fill(1)
        (x,y,z) = compare3D(self.im1_1,self.im1_2,self.im1_3)
        self.assertLess(x, 0)
        
    def testMaxPartialBuild3D(self):
        """Verifies the maxima partial build operator"""
        (w,h,l) = self._drawBaseImage(self.im8_1)
        self.im1_1.reset()
        for i in range(l//2,l):
            self.im1_1[i].fill(1)
        maxPartialBuild3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        for i in range(l//4):
            self.im8_3[i].fill(50)
        for i in range(l//4,l//4+10):
            self.im8_3[i].fill(70)
        for i in range(l//4+10,3*l//4):
            self.im8_3[i].fill(70)
        for i in range(3*l//4,3*l//4+10):
            self.im8_3[i].fill(110)
        for i in range(3*l//4+10,l):
            self.im8_3[i].fill(50)
        (x,y,z) = compare3D(self.im8_3,self.im8_2,self.im8_3)
        self.assertLess(x, 0)
        
    def testMinPartialBuild3D(self):
        """Verifies the minima partial build operator"""
        (w,h,l) = self._drawBaseImage(self.im8_1)
        negate3D(self.im8_1, self.im8_1)
        self.im1_1.reset()
        for i in range(l//2,l):
            self.im1_1[i].fill(1)
        minPartialBuild3D(self.im8_1, self.im1_1, self.im8_2, CUBIC)
        for i in range(l//4):
            self.im8_3[i].fill(50)
        for i in range(l//4,l//4+10):
            self.im8_3[i].fill(70)
        for i in range(l//4+10,3*l//4):
            self.im8_3[i].fill(70)
        for i in range(3*l//4,3*l//4+10):
            self.im8_3[i].fill(110)
        for i in range(3*l//4+10,l):
            self.im8_3[i].fill(50)
        negate3D(self.im8_3, self.im8_3)
        (x,y,z) = compare3D(self.im8_3,self.im8_2,self.im8_3)
        self.assertLess(x, 0)
