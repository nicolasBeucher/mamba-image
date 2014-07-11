"""
Test cases for the image Hit-or-Miss transformation function

The function works only with binary images.

The Hit-or-Miss transformation fonction is a rather complex operation involving
pixel neighbors and patterns.

Python function:
    hitOrMiss
    
C function:
    MB_BinHitOrMiss
"""

from mamba import *
import unittest
import random

class TesthitOrMiss(unittest.TestCase):

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
        self.im1s2_2 = imageMb(128,128,1)
        
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
        del(self.im1s2_2)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        dse = doubleStructuringElement([0],[1],SQUARE)
        #self.assertRaises(MambaError, hitOrMiss, self.im1_1, self.im1_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im1_1, self.im8_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im1_1, self.im32_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im8_1, self.im1_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im8_1, self.im8_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im8_1, self.im32_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im32_1, self.im1_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im32_1, self.im8_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im32_1, self.im32_2, dse)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        dse = doubleStructuringElement([0],[1],SQUARE)
        self.assertRaises(MambaError, hitOrMiss, self.im1s2_1, self.im1_2, dse)
        self.assertRaises(MambaError, hitOrMiss, self.im1_1, self.im1s2_2, dse)

    def testParameterCheck(self):
        """Tests that using same image for input and output raises an exception"""
        dse = doubleStructuringElement([0],[1],SQUARE)
        self.assertRaises(MambaError, hitOrMiss, self.im1_1, self.im1_1, dse)
        
    def _draw3ptsLineS(self,im,imexp,x,y):
        for i in range(x,x+3):
            im.setPixel(1, (i,y))
        imexp.setPixel(1, (x+1,y+1))
        
    def _draw3ptsSquareS(self,im,imexp,x,y,h):
        for j in range(h):
            for i in range(x,x+3):
                im.setPixel(1, (i,y+j))
        imexp.setPixel(1, (x+1,y+h))

    def testComputationSquare(self):
        """Tests binary Hit-or-Miss in square grid"""
        (w,h) = self.im1_1.getSize()
        
        for wi in range(w):
            for hi in range(h):
                vi = random.randint(0,1)
                self.im1_1.setPixel(vi, (wi,hi))
        
        self.im1_2.reset()
        dse = doubleStructuringElement([],[0],SQUARE)
        hitOrMiss(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        
        negate(self.im1_1, self.im1_3)
        self.im1_2.reset()
        dse = doubleStructuringElement([0],[],SQUARE)
        hitOrMiss(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self._draw3ptsLineS(self.im1_1,self.im1_3, 10,5)
        self._draw3ptsLineS(self.im1_1,self.im1_3, 15,5)
        self._draw3ptsSquareS(self.im1_1,self.im1_3, 10,7,4)
        self._draw3ptsLineS(self.im1_1,self.im1_3, 15,10)
        dse = doubleStructuringElement([0,3,7],[1,2,8],SQUARE)
        hitOrMiss(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
    def _draw3ptsLineH(self,im,imexp,x,y):
        for i in range(x,x+3):
            im.setPixel(1, (i,y))
        imexp.setPixel(1, (x+1,y+1))
        if (y+1)%2==0:
            imexp.setPixel(1, (x+2,y+1))
        else:
            imexp.setPixel(1, (x,y+1))
        
    def _draw3ptsSquareH(self,im,imexp,x,y,h):
        for j in range(h):
            for i in range(x,x+3):
                im.setPixel(1, (i,y+j))
        imexp.setPixel(1, (x+1,y+h))
        if (y+h)%2==0:
            imexp.setPixel(1, (x+2,y+h))
        else:
            imexp.setPixel(1, (x,y+h))

    def testComputationHexagonal(self):
        """Tests binary Hit-or-Miss in hexagonal grid"""
        (w,h) = self.im1_1.getSize()
        
        for wi in range(w):
            for hi in range(h):
                vi = random.randint(0,1)
                self.im1_1.setPixel(vi, (wi,hi))
        
        self.im1_2.reset()
        dse = doubleStructuringElement([],[0],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        
        negate(self.im1_1, self.im1_3)
        self.im1_2.reset()
        dse = doubleStructuringElement([0],[],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self._draw3ptsLineH(self.im1_1,self.im1_3, 10,5)
        self._draw3ptsLineH(self.im1_1,self.im1_3, 15,5)
        self._draw3ptsSquareH(self.im1_1,self.im1_3, 10,7,4)
        self._draw3ptsLineH(self.im1_1,self.im1_3, 15,10)
        dse = doubleStructuringElement([0,2,5],[1,6],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
    def testEmptyEdge(self):
        """Verifies the correct empty edge effect in the binary Hit-or-Miss"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (0,h//2))
        
        self.im1_2.reset()
        self.im1_3.reset()
        dse = doubleStructuringElement([],[0,5],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse, edge=EMPTY)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        self.im1_3.setPixel(1, (0,h//2))
        dse = doubleStructuringElement([5],[0],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse, edge=EMPTY)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
    def testFilledEdge(self):
        """Verifies the correct filled edge effect in the binary Hit-or-Miss"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (0,h//2))
        
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_3.setPixel(1, (0,h//2))
        dse = doubleStructuringElement([],[0,5],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse, edge=FILLED)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_3.reset()
        dse = doubleStructuringElement([5],[0],HEXAGONAL)
        hitOrMiss(self.im1_1, self.im1_2, dse, edge=FILLED)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
        self.assertLess(x, 0)

