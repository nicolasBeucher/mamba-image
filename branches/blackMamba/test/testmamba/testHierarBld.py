"""
Test cases for the hierarchical build function.

The function works on greyscale images. All images, both input and output, must
have the same depth.

The function builds an image using the first input image as a mask.

The function result depends on choice over grid.

Python function:
    hierarBuild
    
C functions:
    MB_HierarBld
"""

from mamba import *
import unittest
import random

class TestHierarBld(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
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
        self.im32_4 = imageMb(32)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        self.im8s2_3 = imageMb(128,128,8)
        
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
        del(self.im8s2_1)
        del(self.im8s2_2)
        del(self.im8s2_3)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, hierarBuild, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, hierarBuild, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, hierarBuild, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, hierarBuild, self.im8_1, self.im1_2)
        #self.assertRaises(MambaError, hierarBuild, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, hierarBuild, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, hierarBuild, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, hierarBuild, self.im32_1, self.im8_2)
        #self.assertRaises(MambaError, hierarBuild, self.im32_1, self.im32_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, hierarBuild, self.im8s2_1, self.im8_2)
        self.assertRaises(MambaError, hierarBuild, self.im8_1, self.im8s2_2)
        
    def _drawTestIm(self, imOut, value):

        (w,h) = imOut.getSize()
        drawLine(imOut, (1,1,1,h//3), value)
        drawLine(imOut, (1,h//3,w//3,h//3), value)
        for i in range(1,min(h//4,w//4)):
            drawLine(imOut, (w//3+(i-1),h//3-i,w//3+i,h//3-i),value)
        drawLine(imOut, (w//3+i,h//3-i,w//3+i,(2*h)//3-i), value)
        for j in range(1,min(h//4,w//4)):
            drawLine(imOut, (w//3+i-(j-1),(2*h)//3-i+j,w//3+i-j,(2*h)//3-i+j),value)
        drawLine(imOut, (w//3+i-j,(2*h)//3-i+j,w//3+i-j-w//5,(2*h)//3-i+j),value)
        drawLine(imOut, (w//3+i-j-w//5,(2*h)//3-i+j,w//3+i-j-w//5,(2*h)//3-i+j-h//6),value)

    def testComputation(self):
        """Tests hierarchical build for both grids"""
        self.im8_1.reset()
        self._drawTestIm(self.im8_1, 255)
        
        for i in range(10):
            vi =  random.randint(1,255)
        
            self.im8_4.reset()
            self._drawTestIm(self.im8_4, vi)
        
            self.im8_2.reset()
            self.im8_2.setPixel(vi, (1,1))
            hierarBuild(self.im8_1, self.im8_2, grid=HEXAGONAL)
            (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
            self.im8_2.reset()
            self.im8_2.setPixel(vi, (1,1))
            hierarBuild(self.im8_1, self.im8_2, grid=SQUARE)
            (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
            self.assertLess(x, 0)

    def _drawCross(self, imOut, imExp, x, y, value):
        imOut.setPixel(value, (x,y))
        imOut.setPixel(value, (x-1,y-1))
        imOut.setPixel(value, (x-1,y+1))
        imOut.setPixel(value, (x+1,y-1))
        imOut.setPixel(value, (x+1,y+1))
        if y%2==0:
            imExp.setPixel(value, (x,y))
            imExp.setPixel(value, (x-1,y-1))
            imExp.setPixel(value, (x-1,y+1))
        else:
            imExp.setPixel(value, (x,y))
            imExp.setPixel(value, (x+1,y-1))
            imExp.setPixel(value, (x+1,y+1))
    
    def testGridEffect(self):
        """Verifies that grid is correctly taken into account"""
        self.im8_1.reset()
        self.im8_4.reset()
        self._drawCross(self.im8_1, self.im8_4, 10,10, 255)
        
        self.im8_2.reset()
        self.im8_2.setPixel(255, (10,10))
        hierarBuild(self.im8_1, self.im8_2, grid=HEXAGONAL)
        (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im8_2.reset()
        self.im8_2.setPixel(255, (10,10))
        hierarBuild(self.im8_1, self.im8_2, grid=SQUARE)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testHierarBuild32(self):
        """Tests hierarchical build on 32-bit images for both grids"""
        self.im32_1.reset()
        self._drawTestIm(self.im32_1, 0xffffffff)
        
        for i in range(10):
            vi =  random.randint(1,0x100000)
            
            self.im32_4.reset()
            self._drawTestIm(self.im32_4, vi)
            
            self.im32_2.reset()
            self.im32_2.setPixel(vi, (1,1))
            hierarBuild(self.im32_1, self.im32_2, grid=HEXAGONAL)
            (x,y) = compare(self.im32_4, self.im32_2, self.im32_3)
            self.assertLess(x, 0, "%d, (%d,%d)" % (vi,x,y))
            
            self.im32_2.reset()
            self.im32_2.setPixel(vi, (1,1))
            hierarBuild(self.im32_1, self.im32_2, grid=SQUARE)
            (x,y) = compare(self.im32_4, self.im32_2, self.im32_3)
            self.assertLess(x, 0)


