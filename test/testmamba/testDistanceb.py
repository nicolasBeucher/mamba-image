"""
Test cases for the image set border distance computation function.

The function only works with binary image as input and 32-bit image as output.

For every set of pixels in the input image (pixels set to True that are 
connected), the output image is computed to give its distance to the nearest
border of the set (i.e. distance to the nearest pixel that has a False pixel as
a neighbor).

The result depends on grid and edge configurations.

Python function:
    computeDistance
    
C functions:
    MB_Distanceb
"""

from mamba import *
import unittest
import random

class TestDistanceb(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
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
        del(self.im8_3)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im1s2_1)
        del(self.im32s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, computeDistance, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, computeDistance, self.im1_1, self.im8_2)
        #self.assertRaises(MambaError, computeDistance, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, computeDistance, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, computeDistance, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, computeDistance, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, computeDistance, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, computeDistance, self.im32_1, self.im8_2)
        self.assertRaises(MambaError, computeDistance, self.im32_1, self.im32_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, computeDistance, self.im1s2_1, self.im32_1)
        self.assertRaises(MambaError, computeDistance, self.im1_1, self.im32s2_1)

    def testEmptySet(self):
        """Verifies that an empty set image returns a empty distance image"""
        self.im1_1.reset()
        self.im32_1.reset()
        self.im32_2.reset()
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE, edge=FILLED)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE, edge=EMPTY)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL, edge=FILLED)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL, edge=EMPTY)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
    def _drawExpImFilledSet(self, im, x,y,h,w,v):
    
        for wi in range(w):
            im.fastSetPixel(v, (x+wi,y))
            im.fastSetPixel(v, (x+wi,y+h-1))
        for hi in range(1,h-1):
            im.fastSetPixel(v, (x,y+hi))
            im.fastSetPixel(v, (x+w-1,y+hi))
            
        if h>2 and w>2:
            self._drawExpImFilledSet(im, x+1,y+1,h-2,w-2,v+1)
        
    def testFilledSet(self):
        """Verifies that a filled set image returns a correct distance image"""
        (w,h) = self.im1_1.getSize()
        self.im32_2.reset()
        self._drawExpImFilledSet(self.im32_2,0,0,h,w,1)
        self.im1_1.fill(1)
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE, edge=EMPTY)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL, edge=EMPTY)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
        self.im32_2.reset()
        #self._drawExpImFilledSet(self.im32_2,0,0,h,w,0x00010001)
        self.im1_1.fill(1)
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE, edge=FILLED)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL, edge=FILLED)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
    def _drawSquare(self, im, x,y,values):
        size = int(pow(len(values),0.5))
        for i in range(size):
            for j in range(size):
                im.setPixel(values[i+size*j], (x+i,y+j))
        
    def testEdgeEffect(self):
        """Verifies that edges are correctly taken into account"""
        (w,h) = self.im1_1.getSize()
        self.im1_1.reset()
        self._drawSquare(self.im1_1, 0,0,[1,1,1,1])
        self._drawSquare(self.im1_1, 0,h-2,[1,1,1,1])
        self._drawSquare(self.im1_1, w-2,0,[1,1,1,1])
        self._drawSquare(self.im1_1, w-2,h-2,[1,1,1,1])
        
        self.im32_1.reset()
        self.im32_2.reset()
        self._drawSquare(self.im32_2, 0,0,[2,1,1,1])
        self._drawSquare(self.im32_2, 0,h-2,[1,1,2,1])
        self._drawSquare(self.im32_2, w-2,0,[1,2,1,1])
        self._drawSquare(self.im32_2, w-2,h-2,[1,1,1,2])
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE, edge=FILLED)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))
        self._drawSquare(self.im32_2, 0,0,[1,1,1,1])
        self._drawSquare(self.im32_2, 0,h-2,[1,1,1,1])
        self._drawSquare(self.im32_2, w-2,0,[1,1,1,1])
        self._drawSquare(self.im32_2, w-2,h-2,[1,1,1,1])
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE, edge=EMPTY)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
        self._drawSquare(self.im32_2, 0,0,[2,1,1,1])
        self._drawSquare(self.im32_2, 0,h-2,[1,1,2,1])
        self._drawSquare(self.im32_2, w-2,0,[1,2,1,1])
        self._drawSquare(self.im32_2, w-2,h-2,[1,1,1,2])
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL, edge=FILLED)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        self._drawSquare(self.im32_2, 0,0,[1,1,1,1])
        self._drawSquare(self.im32_2, 0,h-2,[1,1,1,1])
        self._drawSquare(self.im32_2, w-2,0,[1,1,1,1])
        self._drawSquare(self.im32_2, w-2,h-2,[1,1,1,1])
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL, edge=EMPTY)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
    def testComputeHexagonal(self):
        """Verifies the distance computation in hexagonal grid"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self._drawSquare(self.im1_1, 10,11,[1,1,0,1,1,1,1,1,0])
        self._drawSquare(self.im1_1, 20,16,[0,1,1,1,1,1,0,1,1])
        
        self.im32_1.reset()
        self.im32_2.reset()
        self._drawSquare(self.im32_2, 10,11,[1,1,0,1,2,1,1,1,0])
        self._drawSquare(self.im32_2, 20,16,[0,1,1,1,2,1,0,1,1])
        computeDistance(self.im1_1, self.im32_1, grid=HEXAGONAL)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))
        
    def testComputeSquare(self):
        """Verifies the distance computation in square grid"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self._drawSquare(self.im1_1, 10,11,[1,1,1,1,1,1,1,1,1])
        self._drawSquare(self.im1_1, 20,16,[1,1,1,1,1,1,1,1,1])
        
        self.im32_1.reset()
        self.im32_2.reset()
        self._drawSquare(self.im32_2, 10,11,[1,1,1,1,2,1,1,1,1])
        self._drawSquare(self.im32_2, 20,16,[1,1,1,1,2,1,1,1,1])
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))
        
        self.im1_1.reset()
        self._drawSquare(self.im1_1, 10,11,[1,1,0,1,1,1,1,1,0])
        self._drawSquare(self.im1_1, 20,16,[0,1,1,1,1,1,0,1,1])
        
        self.im32_1.reset()
        self.im32_2.reset()
        self._drawSquare(self.im32_2, 10,11,[1,1,0,1,1,1,1,1,0])
        self._drawSquare(self.im32_2, 20,16,[0,1,1,1,1,1,0,1,1])
        computeDistance(self.im1_1, self.im32_1, grid=SQUARE)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0, "%d,%d" %(x,y))

