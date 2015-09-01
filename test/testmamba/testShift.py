"""
Test cases for the image shift function.

The function works on all image depths. All images, both input and output, must
have the same depth.

Here is the list of legal operations :
    shift( 1) = 1
    shift( 8) = 8
    shift(32) =32
    
The result in output is the input image shifted in the given direction. The 
created space is filled with the value given in argument.

The result depends on grid configuration. Allowed values for directions are 
restricted according to grid configuration.

Python function:
    shift
    
C functions:
    MB_Shiftb
    MB_Shift32
"""

from mamba import *
import unittest
import random

class TestShift(unittest.TestCase):

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
        #self.assertRaises(MambaError, shift, self.im1_1, self.im1_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im1_1, self.im8_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im1_1, self.im32_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im8_1, self.im1_2,0,1,1)
        #self.assertRaises(MambaError, shift, self.im8_1, self.im8_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im8_1, self.im32_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im32_1, self.im1_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im32_1, self.im8_2,0,1,1)
        #self.assertRaises(MambaError, shift, self.im32_1, self.im32_2,0,1,1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, shift, self.im8s2_1, self.im8_2,0,1,1)
        self.assertRaises(MambaError, shift, self.im8_1, self.im8s2_2,0,1,1)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        for i in range(7,50):
            self.assertRaises(MambaError, shift, self.im1_1, self.im1_2,i,1,0, grid=HEXAGONAL)
            self.assertRaises(MambaError, shift, self.im8_1, self.im8_2,i,1,0, grid=HEXAGONAL)
            self.assertRaises(MambaError, shift, self.im32_1, self.im32_2,i,1,0, grid=HEXAGONAL)
        for i in range(9,50):
            self.assertRaises(MambaError, shift, self.im1_1, self.im1_2,i,1,0, grid=SQUARE)
            self.assertRaises(MambaError, shift, self.im8_1, self.im8_2,i,1,0, grid=SQUARE)
            self.assertRaises(MambaError, shift, self.im32_1, self.im32_2,i,1,0, grid=SQUARE)
            
    def _squarePixelPrediction(self, im, d, x, y, amp, v):
        (w,h) = im.getSize()
    
        xpre = x+amp*self.dirS[d][0]
        ypre = y+amp*self.dirS[d][1]
        
        if xpre<w and xpre>=0 and ypre<h and ypre>=0:
            im.setPixel(v, (xpre,ypre))
        return (xpre,ypre)

    def testShiftingSquare_1(self):
        """Verifies shift of binary image in square grid"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_3.reset()
                self.im1_1.setPixel(1, (xi,yi))
                self._squarePixelPrediction(self.im1_3, d, xi, yi, ampi, 1)
                shift(self.im1_1, self.im1_2, d, ampi, 0, grid=SQUARE)
                (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
                self.assertLess(x, 0)

    def testShiftingSquare_8(self):
        """Verifies shift of 8-bit image in square grid"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(0,255)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_3.reset()
                self.im8_1.setPixel(vi, (xi,yi))
                self._squarePixelPrediction(self.im8_3, d, xi, yi, ampi, vi)
                shift(self.im8_1, self.im8_2, d, ampi, 0, grid=SQUARE)
                (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
                self.assertLess(x, 0)

    def testShiftingSquare_32(self):
        """Verifies shift of 32-bit image in square grid"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(0,0xffffffff)
            ampi = random.randint(0,100)
            for d in getDirections(SQUARE):
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_3.reset()
                self.im32_1.setPixel(vi, (xi,yi))
                self._squarePixelPrediction(self.im32_3, d, xi, yi, ampi, vi)
                shift(self.im32_1, self.im32_2, d, ampi, 0, grid=SQUARE)
                (x,y) = compare(self.im32_2, self.im32_3, self.im32_3)
                self.assertLess(x, 0)
            
    def _hexagonalPixelPrediction(self, im, d, x, y, amp, v):
        (w,h) = im.getSize()
        xpre = x
        ypre = y
        for i in range(amp):
            xpre = xpre+self.dirH[ypre%2][d][0]
            ypre = ypre+self.dirH[ypre%2][d][1]
        
        if xpre<w and xpre>=0 and ypre<h and ypre>=0:
            im.setPixel(v, (xpre,ypre))
        return (xpre,ypre)

    def testShiftingHexagonal_1(self):
        """Verifies shift of binary image in hexagonal grid"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(1000):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_3.reset()
                self.im1_1.setPixel(1, (xi,yi))
                self._hexagonalPixelPrediction(self.im1_3, d, xi, yi, ampi, 1)
                shift(self.im1_1, self.im1_2, d, ampi, 0, grid=HEXAGONAL)
                (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
                self.assertLess(x, 0)
    
    def testShiftingHexagonal_8(self):
        """Verifies shift of 8-bit image in hexagonal grid"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(0,255)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_3.reset()
                self.im8_1.setPixel(vi, (xi,yi))
                self._hexagonalPixelPrediction(self.im8_3, d, xi, yi, ampi, vi)
                shift(self.im8_1, self.im8_2, d, ampi, 0, grid=HEXAGONAL)
                (x,y) = compare(self.im8_2, self.im8_3, self.im8_3)
                self.assertLess(x, 0)

    def testShiftingHexagonal_32(self):
        """Verifies shift of 32-bit image in hexagonal grid"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(0,0xffffffff)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_3.reset()
                self.im32_1.setPixel(vi, (xi,yi))
                self._hexagonalPixelPrediction(self.im32_3, d, xi, yi, ampi, vi)
                shift(self.im32_1, self.im32_2, d, ampi, 0, grid=HEXAGONAL)
                (x,y) = compare(self.im32_2, self.im32_3, self.im32_3)
                self.assertLess(x, 0)
                
    def testFillValue_1(self):
        """Verifies the filling of created space due to shift in binary image"""
        (w,h) = self.im1_1.getSize()
        
        created_space_volume = [0, w, h+w-1, h, h+w-1, w, h+w-1, h, h+w-1]
        for d in getDirections(SQUARE):
            self.im1_1.fill(1)
            self.im1_2.reset()
            shift(self.im1_1, self.im1_2, d, 1, 0, grid=SQUARE)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, w*h-created_space_volume[d])
            self.im1_1.reset()
            self.im1_2.reset()
            shift(self.im1_1, self.im1_2, d, 1, 1, grid=SQUARE)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, created_space_volume[d], "in dir %d : %d/%d" %(d,vol,created_space_volume[d]))
            
        created_space_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            self.im1_1.fill(1)
            self.im1_2.reset()
            shift(self.im1_1, self.im1_2, d, 1, 0, grid=HEXAGONAL)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, w*h-created_space_volume[d])
            self.im1_1.reset()
            self.im1_2.reset()
            shift(self.im1_1, self.im1_2, d, 1, 1, grid=HEXAGONAL)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, created_space_volume[d])
    
    def testFillValue_8(self):
        """Verifies the filling of created space due to shift in 8-bit image"""
        (w,h) = self.im8_1.getSize()
        
        created_space_volume = [0, w, h+w-1, h, h+w-1, w, h+w-1, h, h+w-1]
        for d in getDirections(SQUARE):
            vi = random.randint(2,255)
            self.im8_1.fill(vi)
            self.im8_2.reset()
            shift(self.im8_1, self.im8_2, d, 1, 0, grid=SQUARE)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol//vi, w*h-created_space_volume[d])
            self.im8_1.reset()
            self.im8_2.reset()
            shift(self.im8_1, self.im8_2, d, 1, vi, grid=SQUARE)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol//vi, created_space_volume[d], "in dir %d : %d/%d" %(d,vol,created_space_volume[d]))
            
        created_space_volume = [0, w+h//2, h, w+h//2-1, w+h//2, h, w+h//2-1]
        for d in getDirections(HEXAGONAL):
            vi = random.randint(2,255)
            self.im8_1.fill(vi)
            self.im8_2.reset()
            shift(self.im8_1, self.im8_2, d, 1, 0, grid=HEXAGONAL)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol//vi, w*h-created_space_volume[d])
            self.im8_1.reset()
            self.im8_2.reset()
            shift(self.im8_1, self.im8_2, d, 1, vi, grid=HEXAGONAL)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol//vi, created_space_volume[d])
    
    def testInoutShifting_1(self):
        """Verifies shift when a binary image is used both as input and output"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_3.reset()
                self.im1_1.setPixel(1, (xi,yi))
                self._hexagonalPixelPrediction(self.im1_3, d, xi, yi, ampi, 1)
                shift(self.im1_1, self.im1_1, d, ampi, 0, grid=HEXAGONAL)
                (x,y) = compare(self.im1_1, self.im1_3, self.im1_2)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_3.reset()
                self.im1_1.setPixel(1, (xi,yi))
                self._squarePixelPrediction(self.im1_3, d, xi, yi, ampi, 1)
                shift(self.im1_1, self.im1_1, d, ampi, 0, grid=SQUARE)
                (x,y) = compare(self.im1_1, self.im1_3, self.im1_2)
                self.assertLess(x, 0)
    
    def testInoutShifting_8(self):
        """Verifies shift when a 8-bit image is used both as input and output"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(0,255)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_3.reset()
                self.im8_1.setPixel(vi, (xi,yi))
                self._hexagonalPixelPrediction(self.im8_3, d, xi, yi, ampi, vi)
                shift(self.im8_1, self.im8_1, d, ampi, 0, grid=HEXAGONAL)
                (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_3.reset()
                self.im8_1.setPixel(vi, (xi,yi))
                self._squarePixelPrediction(self.im8_3, d, xi, yi, ampi, vi)
                shift(self.im8_1, self.im8_1, d, ampi, 0, grid=SQUARE)
                (x,y) = compare(self.im8_1, self.im8_3, self.im8_2)
                self.assertLess(x, 0)

    def testInoutShifting_32(self):
        """Verifies shift when a 32-bit image is used both as input and output"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            vi = random.randint(0,0xffffffff)
            ampi = random.randint(0,100)
            for d in getDirections(HEXAGONAL):
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_3.reset()
                self.im32_1.setPixel(vi, (xi,yi))
                self._hexagonalPixelPrediction(self.im32_3, d, xi, yi, ampi, vi)
                shift(self.im32_1, self.im32_1, d, ampi, 0, grid=HEXAGONAL)
                (x,y) = compare(self.im32_1, self.im32_3, self.im32_2)
                self.assertLess(x, 0)
            for d in getDirections(SQUARE):
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_3.reset()
                self.im32_1.setPixel(vi, (xi,yi))
                self._squarePixelPrediction(self.im32_3, d, xi, yi, ampi, vi)
                shift(self.im32_1, self.im32_1, d, ampi, 0, grid=SQUARE)
                (x,y) = compare(self.im32_1, self.im32_3, self.im32_2)
                self.assertLess(x, 0)

