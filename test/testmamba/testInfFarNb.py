"""
Test cases for the image infimum by far neighbor function.

The function works on all images depths. All images, both input and output, must
have the same depth.

Here is the list of legal operations :
    infFarNeighbor( 1, 1) = 1
    infFarNeighbor( 8, 8) = 8
    infFarNeighbor(32,32) =32
    
The result in output is the infimum value (see testInf for a definition). In
this case however, the pixels inside the second input image (which is also the 
output image) are compared with their neighbors (specified to the function) 
at a given distance inside the first image.

The result depends on grid and edge configurations. Allowed values for neighbor
are restricted according to grid configuration.

Python function:
    infFarNeighbor
    
C functions:
    MB_InfFarNbb
    MB_InfFarNb8
    MB_InfFarNb32
"""

from mamba import *
import unittest
import random

class TestInfFarNb(unittest.TestCase):

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
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        self.im8s2_3 = imageMb(128,128,8)
        
        self.dirS = [
            (0,0),
            (0,-1),
            (1,-1),
            (1,0),
            (1,1),
            (0,1),
            (-1,1),
            (-1,0),
            (-1,-1)
        ]
        
        dirHE = [
            (0,0),
            (0,-1),
            (1,0),
            (0,1),
            (-1,1),
            (-1,0),
            (-1,-1)
        ]
        
        dirHO = [
            (0,0),
            (1,-1),
            (1,0),
            (1,1),
            (0,1),
            (-1,0),
            (0,-1)
        ]
        
        self.dirH = [dirHE, dirHO]
        
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
        del(self.im8s2_1)
        del(self.im8s2_2)
        del(self.im8s2_3)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        #self.assertRaises(MambaError, infFarNeighbor, self.im1_1, self.im1_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im1_1, self.im8_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im1_1, self.im32_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im8_1, self.im1_2,0,1)
        #self.assertRaises(MambaError, infFarNeighbor, self.im8_1, self.im8_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im8_1, self.im32_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im32_1, self.im1_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im32_1, self.im8_2,0,1)
        #self.assertRaises(MambaError, infFarNeighbor, self.im32_1, self.im32_2,0,1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, infFarNeighbor, self.im8s2_1, self.im8_2,0,1)
        self.assertRaises(MambaError, infFarNeighbor, self.im8_1, self.im8s2_2,0,1)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        for i in range(7,50):
            self.assertRaises(MambaError, infFarNeighbor, self.im1_1, self.im1_2,i,1, grid=HEXAGONAL)
            self.assertRaises(MambaError, infFarNeighbor, self.im8_1, self.im8_2,i,1, grid=HEXAGONAL)
            self.assertRaises(MambaError, infFarNeighbor, self.im32_1, self.im32_2,i,1, grid=HEXAGONAL)
        for i in range(9,50):
            self.assertRaises(MambaError, infFarNeighbor, self.im1_1, self.im1_2,i,1, grid=SQUARE)
            self.assertRaises(MambaError, infFarNeighbor, self.im8_1, self.im8_2,i,1, grid=SQUARE)
            self.assertRaises(MambaError, infFarNeighbor, self.im32_1, self.im32_2,i,1, grid=SQUARE)
            
    def _squarePixelPrediction(self, im, d, x, y, amp, v):
        (w,h) = im.getSize()
    
        xpre = x-amp*self.dirS[d][0]
        ypre = y-amp*self.dirS[d][1]
        
        if xpre<w and xpre>=0 and ypre<h and ypre>=0:
            im.setPixel(v, (xpre,ypre))
        return (xpre,ypre)

    def testComputationSquare_1(self):
        """Tests infimum by far neighbor computations in square grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im1_1.fill(1)
                self.im1_2.fill(1)
                self.im1_3.fill(1)
                self.im1_1.setPixel(0, (xi,yi))
                self._squarePixelPrediction(self.im1_3, d, xi, yi, ampi, 0)
                infFarNeighbor(self.im1_1, self.im1_2, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
                self.assertLess(x, 0, "in dir %d, (%d,%d)-%d : (%d,%d)" % (d,xi,yi,ampi,x,y))

    def testComputationSquare_8(self):
        """Tests infimum by far neighbor computations in square grid on greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(1,255)
            wi = random.randint(0,vi-1)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im8_1.fill(vi)
                self.im8_2.fill(vi)
                self.im8_3.fill(vi)
                self.im8_1.setPixel(wi, (xi,yi))
                self._squarePixelPrediction(self.im8_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im8_1, self.im8_2, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
                self.assertLess(x, 0)

    def testComputationSquare_32(self):
        """Tests infimum by far neighbor computations in square grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(1,0xffffffff)
            wi = random.randint(0,vi-1)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im32_1.fill(vi)
                self.im32_2.fill(vi)
                self.im32_3.fill(vi)
                self.im32_1.setPixel(wi, (xi,yi))
                self._squarePixelPrediction(self.im32_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im32_1, self.im32_2, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im32_2, self.im32_3, self.im32_3)
                self.assertLess(x, 0, "in dir %d [vi=%d], (%d,%d)-%d : (%d,%d)" % (d,vi,xi,yi,ampi,x,y))
            
    def _hexagonalPixelPrediction(self, im, d, x, y, amp, v):
        (w,h) = im.getSize()
        xpre = x
        ypre = y
        for i in range(amp):
            xpre = xpre-self.dirH[(ypre+1)%2][d][0]
            ypre = ypre-self.dirH[(ypre+1)%2][d][1]
        
        if xpre<w and xpre>=0 and ypre<h and ypre>=0:
            im.setPixel(v, (xpre,ypre))
        return (xpre,ypre)

    def testComputationHexagonal_1(self):
        """Tests infimum by far neighbor computations in hexagonal grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(1000):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im1_1.fill(1)
                self.im1_2.fill(1)
                self.im1_3.fill(1)
                self.im1_1.setPixel(0, (xi,yi))
                self._hexagonalPixelPrediction(self.im1_3, d, xi, yi, ampi, 0)
                infFarNeighbor(self.im1_1, self.im1_2, d, ampi, grid=HEXAGONAL)
                (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
                self.assertLess(x, 0, "in dir %d, (%d,%d)-%d : (%d,%d)" % (d,xi,yi,ampi,x,y))
    
    def testComputationHexagonal_8(self):
        """Tests infimum by far neighbor computations in hexagonal grid on greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(1,255)
            wi = random.randint(0,vi-1)
            ampi = random.randint(0,100)
            for d in range(2,3): #getDirections(HEXAGONAL):
                self.im8_1.fill(vi)
                self.im8_2.fill(vi)
                self.im8_3.fill(vi)
                self.im8_1.setPixel(wi, (xi,yi))
                self._hexagonalPixelPrediction(self.im8_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im8_1, self.im8_2, d, ampi, grid=HEXAGONAL)
                (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
                self.assertLess(x, 0, "at (%d,%d) : (%d,%d) %d - %d" % (x,y,xi,yi,d,ampi))

    def testComputationHexagonal_32(self):
        """Tests infimum by far neighbor computations in hexagonal grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(1,0xffffffff)
            wi = random.randint(0,vi-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im32_1.fill(vi)
                self.im32_2.fill(vi)
                self.im32_3.fill(vi)
                self.im32_1.setPixel(wi, (xi,yi))
                self._hexagonalPixelPrediction(self.im32_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im32_1, self.im32_2, d, ampi, grid=HEXAGONAL)
                (x,y) = compare(self.im32_2, self.im32_3, self.im32_3)
                self.assertLess(x, 0, "in dir %d [vi=%d, wi=%d], (%d,%d)-%d : (%d,%d)" % (d,vi,wi,xi,yi,ampi,x,y))
                
    def testEdgeEffect_1(self):
        """Verifies that edge value is correctly taken into account on binary image"""
        (w,h) = self.im1_1.getSize()
        
        created_space_volume = [0, w, h+w-1, h, h+w-1, w, h+w-1, h, h+w-1]
        for d in getDirections(SQUARE):
            self.im1_1.fill(1)
            infFarNeighbor(self.im1_1, self.im1_1, d, 1, edge=FILLED, grid=SQUARE)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
            self.im1_1.fill(1)
            infFarNeighbor(self.im1_1, self.im1_1, d, 1, edge=EMPTY, grid=SQUARE)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, (w*h-created_space_volume[d]))
            
        created_space_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            self.im1_1.fill(1)
            infFarNeighbor(self.im1_1, self.im1_1, d, 1, edge=FILLED, grid=HEXAGONAL)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h)
            self.im1_1.fill(1)
            infFarNeighbor(self.im1_1, self.im1_1, d, 1, edge=EMPTY, grid=HEXAGONAL)
            vol = computeVolume(self.im1_1)
            self.assertEqual(vol, w*h-created_space_volume[d], "%d : %d!=%d [%d]"%(d,vol,w*h-created_space_volume[d],created_space_volume[d]))
    
    def testEdgeEffect_8(self):
        """Verifies that edge value is correctly taken into account on greyscale image"""
        (w,h) = self.im8_1.getSize()
        
        created_space_volume = [0, w, h+w-1, h, h+w-1, w, h+w-1, h, h+w-1]
        for d in getDirections(SQUARE):
            vi = random.randint(2,255)
            self.im8_1.fill(vi)
            infFarNeighbor(self.im8_1, self.im8_1, d, 1, edge=FILLED, grid=SQUARE)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, vi*w*h)
            self.im8_1.fill(vi)
            infFarNeighbor(self.im8_1, self.im8_1, d, 1, edge=EMPTY, grid=SQUARE)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, vi*(w*h-created_space_volume[d]))
            
        created_space_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            vi = random.randint(2,255)
            self.im8_1.fill(vi)
            infFarNeighbor(self.im8_1, self.im8_1, d, 1, edge=FILLED, grid=HEXAGONAL)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, vi*w*h)
            self.im8_1.fill(vi)
            infFarNeighbor(self.im8_1, self.im8_1, d, 1, edge=EMPTY, grid=HEXAGONAL)
            vol = computeVolume(self.im8_1)
            self.assertEqual(vol, vi*(w*h-created_space_volume[d]), "%d : %d!=%d [%d, %d]"%(d,vol,vi*(w*h-created_space_volume[d]),vi,created_space_volume[d]))
    
    def testInoutComputation_1(self):
        """Verifies computation when a binary image is used as both input and output"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im1_1.fill(1)
                self.im1_3.fill(1)
                self.im1_1.setPixel(0, (xi,yi))
                self.im1_3.setPixel(0, (xi,yi))
                self._hexagonalPixelPrediction(self.im1_3, d, xi, yi, ampi, 0)
                infFarNeighbor(self.im1_1, self.im1_1, d, ampi, grid=HEXAGONAL)
                (x,y) = compare(self.im1_1, self.im1_3, self.im1_2)
                self.assertLess(x, 0, "hex in dir %d, (%d,%d)-%d : (%d,%d)" % (d,xi,yi,ampi,x,y))
            for d in getDirections(SQUARE):
                self.im1_1.fill(1)
                self.im1_3.fill(1)
                self.im1_1.setPixel(0, (xi,yi))
                self.im1_3.setPixel(0, (xi,yi))
                self._squarePixelPrediction(self.im1_3, d, xi, yi, ampi, 0)
                infFarNeighbor(self.im1_1, self.im1_1, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im1_1, self.im1_3, self.im1_2)
                self.assertLess(x, 0, "sqr in dir %d, (%d,%d)-%d : (%d,%d)" % (d,xi,yi,ampi,x,y))
    
    def testInoutComputation_8(self):
        """Verifies computation when a 8-bit image is used as both input and output"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(1,255)
            wi = random.randint(0,vi-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im8_1.fill(vi)
                self.im8_3.fill(vi)
                self.im8_1.setPixel(wi, (xi,yi))
                self.im8_3.setPixel(wi, (xi,yi))
                self._hexagonalPixelPrediction(self.im8_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im8_1, self.im8_1, d, ampi, grid=HEXAGONAL)
                (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im8_1.fill(vi)
                self.im8_2.fill(vi)
                self.im8_3.fill(vi)
                self.im8_1.setPixel(wi, (xi,yi))
                self.im8_3.setPixel(wi, (xi,yi))
                self._squarePixelPrediction(self.im8_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im8_1, self.im8_1, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
                self.assertLess(x, 0)

    def testInoutComputation_32(self):
        """Verifies computation when a 32-bit image is used as both input and output"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(1,0xffffffff)
            wi = random.randint(0,vi-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im32_1.fill(vi)
                self.im32_3.fill(vi)
                self.im32_1.setPixel(wi, (xi,yi))
                self.im32_3.setPixel(wi, (xi,yi))
                self._hexagonalPixelPrediction(self.im32_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im32_1, self.im32_1, d, ampi, grid=HEXAGONAL)
                (x,y) = compare(self.im32_1, self.im32_3, self.im32_2)
                self.assertLess(x, 0, "hex in dir %d [vi=%d], (%d,%d)-%d : (%d,%d)" % (d,vi,xi,yi,ampi,x,y))
            for d in getDirections(SQUARE):
                self.im32_1.fill(vi)
                self.im32_3.fill(vi)
                self.im32_1.setPixel(wi, (xi,yi))
                self.im32_3.setPixel(wi, (xi,yi))
                self._squarePixelPrediction(self.im32_3, d, xi, yi, ampi, wi)
                infFarNeighbor(self.im32_1, self.im32_1, d, ampi, grid=SQUARE)
                (x,y) = compare(self.im32_1, self.im32_3, self.im32_2)
                self.assertLess(x, 0, "sqr in dir %d [vi=%d], (%d,%d)-%d : (%d,%d)" % (d,vi,xi,yi,ampi,x,y))

