"""
Test cases for the extremum operators found in the extrema3D
module of mamba3D package. 

Python functions:
    minima3D
    maxima3D
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
        if ext=="min":
            imOut.fill(255)
        else:
            imOut.reset()
            
        (w,h,l) = imOut.getSize()
        for xi in range(0,w-3,3):
            vi = random.randint(1,255)
            hi = vi-random.randint(0,vi)
            yi = random.randint(1,h-2)
            zi = random.randint(1,l-2)
            if ext=="min":
                imOut.setPixel(255-vi+hi, (xi+1,yi,zi))
                imOut.setPixel(255-vi, (xi,yi,zi))
            else:
                imOut.setPixel(vi-hi, (xi+1,yi,zi))
                imOut.setPixel(vi, (xi,yi,zi))
            if hi<lh and vi-hi>0:
                imRes.setPixel(1, (xi+1,yi,zi))
            imRes.setPixel(1, (xi,yi,zi))
        
    def testMinima3D(self):
        """Verifies the minima extraction 3D operator"""
        for i in range(1, 2):
            self._drawRandomExtrema(self.im8_1, self.im1_1, lh=i, ext="min")
            minima3D(self.im8_1, self.im1_2, i)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testMaxima3D(self):
        """Verifies the maxima extraction 3D operator"""
        for i in range(1, 2):
            self._drawRandomExtrema(self.im8_1, self.im1_1, lh=i, ext="max")
            maxima3D(self.im8_1, self.im1_2, i)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
            
