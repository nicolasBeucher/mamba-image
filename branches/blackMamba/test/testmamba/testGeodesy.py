"""
Test cases for the functions implementing geodesic operators found in the 
geodesy module of mamba package.

Python functions:
    geodesicDilate
    geodesicErode
    build
    dualBuild
    closeHoles
    removeEdgeParticles
    geodesicDistance
    lowerGeodesicDilate
    lowerGeodesicErode
    upperGeodesicDilate
    upperGeodesicErode
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

    def testBuild(self):
        """Tests the build operation for both grids"""
        self.im8_1.reset()
        self._drawTestIm(self.im8_1, 255)
        
        for i in range(10):
            vi =  random.randint(1,255)
        
            self.im8_4.reset()
            self._drawTestIm(self.im8_4, vi)
        
            self.im8_2.reset()
            self.im8_2.setPixel(vi, (1,1))
            build(self.im8_1, self.im8_2, grid=HEXAGONAL)
            (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
            self.im8_2.reset()
            self.im8_2.setPixel(vi, (1,1))
            build(self.im8_1, self.im8_2, grid=SQUARE)
            (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
            self.assertLess(x, 0)

    def testDualBuild(self):
        """Tests the dual build operation for both grids"""
        self.im8_1.fill(255)
        self._drawTestIm(self.im8_1, 0)
        
        for i in range(10):
            vi =  random.randint(0,254)
        
            self.im8_4.fill(255)
            self._drawTestIm(self.im8_4, vi)
        
            self.im8_2.fill(255)
            self.im8_2.setPixel(vi, (1,1))
            dualBuild(self.im8_1, self.im8_2, grid=HEXAGONAL)
            (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
            self.im8_2.fill(255)
            self.im8_2.setPixel(vi, (1,1))
            dualBuild(self.im8_1, self.im8_2, grid=SQUARE)
            (x,y) = compare(self.im8_4, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testLowerGeodesicDilate_1(self):
        """Verifies the lower geodesic dilation operation for binary images"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        
        drawSquare(self.im1_2, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        self.im1_1.setPixel(1, (w//2,h//2-2))
        self.im1_1.setPixel(1, (w//2,h//2-3))
        drawSquare(self.im1_4, (w//2-1,h//2-2,w//2+1,h//2-1), 1)
        lowerGeodesicDilate(self.im1_1, self.im1_2, self.im1_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        geodesicDilate(self.im1_1, self.im1_2, self.im1_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicDilate_1(self):
        """Verifies the upper geodesic dilation operation for binary images"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        
        drawSquare(self.im1_2, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        self.im1_1.setPixel(1, (w//2,h//2-2))
        self.im1_1.setPixel(1, (w//2,h//2-3))
        drawSquare(self.im1_4, (w//2-1,h//2-4,w//2+1,h//2-3), 1)
        drawSquare(self.im1_4, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        upperGeodesicDilate(self.im1_1, self.im1_2, self.im1_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicDilate_8(self):
        """Verifies the upper geodesic dilation operation for greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(w,256)):
            drawLine(self.im8_1, (i,0,i,h-1), 255-i)
        self.im8_2.fill(128)
        self.im8_4.fill(128)
        for i in range(129):
            drawLine(self.im8_4, (i,0,i,h-1), min(256-i,255))
        upperGeodesicDilate(self.im8_1, self.im8_2, self.im8_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testLowerGeodesicDilate_8(self):
        """Verifies the lower geodesic dilation operation for greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(w,256)):
            drawLine(self.im8_1, (i,0,i,h-1), 255-i)
        self.im8_2.fill(128)
        
        self.im8_4.reset()
        for i in range(129):
            drawLine(self.im8_4, (i,0,i,h-1), 128)
        for i in range(129,min(w,256)):
            drawLine(self.im8_4, (i,0,i,h-1), 256-i)
        lowerGeodesicDilate(self.im8_1, self.im8_2, self.im8_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        geodesicDilate(self.im8_1, self.im8_2, self.im8_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testLowerGeodesicErode_1(self):
        """Verifies the lower geodesic erosion operation for binary images"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        drawSquare(self.im1_2, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        self.im1_4.setPixel(1, (w//2,h//2-2))
        drawSquare(self.im1_1, (w//2-1,h//2-3,w//2+1,h//2-1), 1)
        lowerGeodesicErode(self.im1_1, self.im1_2, self.im1_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        geodesicErode(self.im1_1, self.im1_2, self.im1_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicErode_1(self):
        """Verifies the upper geodesic erosion operation for binary images"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        drawSquare(self.im1_2, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        self.im1_4.setPixel(1, (w//2,h//2-3))
        drawSquare(self.im1_4, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        drawSquare(self.im1_1, (w//2-1,h//2-4,w//2+1,h//2-1), 1)
        upperGeodesicErode(self.im1_1, self.im1_2, self.im1_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicErode_8(self):
        """Verifies the upper geodesic erosion operation for greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(w,256)):
            drawLine(self.im8_1, (i,0,i,h-1), 255-i)
        self.im8_2.fill(128)
        self.im8_4.fill(128)
        for i in range(127):
            drawLine(self.im8_4, (i,0,i,h-1), 254-i)
        upperGeodesicErode(self.im8_1, self.im8_2, self.im8_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        geodesicErode(self.im8_1, self.im8_2, self.im8_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testLowerGeodesicErode_8(self):
        """Verifies the lower geodesic erosion operation for greyscale images"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(w,256)):
            drawLine(self.im8_1, (i,0,i,h-1), 255-i)
        self.im8_2.fill(128)
        
        self.im8_4.reset()
        for i in range(127):
            drawLine(self.im8_4, (i,0,i,h-1), 128)
        for i in range(127,min(w,256)-1):
            drawLine(self.im8_4, (i,0,i,h-1), 254-i)
        lowerGeodesicErode(self.im8_1, self.im8_2, self.im8_3, 1, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testCloseHoles(self):
        """Verifies the closing holes operator"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(1,10):
            self.im1_1.reset()
            drawBox(self.im1_1, (w//2-i,h//2-i,w//2+i,h//2+i), 1)
            self.im1_2.reset()
            drawSquare(self.im1_2, (w//2-i,h//2-i,w//2+i,h//2+i), 1)
            closeHoles(self.im1_1, self.im1_3)
            (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d" %(i))
            
    def testRemoveEdgeParticles(self):
        """Tests the operator removing the particles connected to the edge"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        y=1
        i=0
        while (y+i)<h:
            drawSquare(self.im1_1, (0,y,i,y+i), 1)
            drawSquare(self.im1_1, (w//2,y,w//2+i,y+i), 1)
            drawSquare(self.im1_2, (w//2,y,w//2+i,y+i), 1)
            y += i+2
            i += 1
        removeEdgeParticles(self.im1_1, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "%d" %(i))
        
    def testGeodesicDistanceDepthAcceptation(self):
        """Verifies that geodesicDistance function raises an error for non binary images"""
        self.assertRaises(MambaError, geodesicDistance, self.im8_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, geodesicDistance, self.im32_3, self.im1_2, self.im1_1)
        
    def testGeodesicDistance(self):
        """Verifies the geodesic distance operation"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im8_3.reset()
        self.im8_4.reset()
        drawSquare(self.im1_2, (w//2-2,h//2-2,w//2+2,h//2+2), 1)
        drawSquare(self.im8_4, (w//2-1,h//2-2,w//2+1,h//2-1), 1)
        self.im8_4.setPixel(2, (w//2,h//2-2))
        drawSquare(self.im1_1, (w//2-1,h//2-2,w//2+1,h//2-1), 1)
        geodesicDistance(self.im1_1, self.im1_2, self.im8_3, se=SQUARE3X3)
        (x,y) = compare(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)

