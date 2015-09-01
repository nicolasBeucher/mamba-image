"""
Test cases for the segmentation (watershed based) functions found in the segment
module of mamba package.

Python functions and classes:
    markerControlledWatershed
    valuedWatershed
    fastSKIZ
    geodesicSKIZ
    mosaic
    mosaicGradient
"""

from mamba import *
import unittest
import random

class TestSegment(unittest.TestCase):

    def setUp(self):
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im1_4 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im8_4 = imageMb(8)
        self.im8_5 = imageMb(8)
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
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
            
    def _drawWells(self, imOut, wall=[1,2,3,4]):
        (w,h) = imOut.getSize()
        
        imOut.reset()
        if wall.count(1)>0:
            drawLine(imOut, (w//2,0,w//2,h//2), 20)
        if wall.count(2)>0:
            drawLine(imOut, (0,h//2,w//2,h//2), 40)
        if wall.count(3)>0:
            drawLine(imOut, (w//2,h//2+1,w//2,h-1), 60)
        if wall.count(4)>0:
            drawLine(imOut, (w//2+1,h//2,w-1,h//2), 80)
        imOut.setPixel(255, (w//2,h//2))
        
    def testMarkerControlledWatershed(self):
        """Verifies the marker controlled valued watershed computation"""
        (w,h) = self.im8_1.getSize()
        
        self._drawWells(self.im8_1)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self._drawWells(self.im8_3, wall=[1,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[3,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[2,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[3,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[3,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[2,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[1,3,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[2,3,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[1,2,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self._drawWells(self.im8_3, wall=[2,3,4])
        markerControlledWatershed(self.im8_1, self.im1_1, self.im8_2, SQUARE)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testValuedWatershed(self):
        """Verifies the minima controlled valued watershed computation"""
        (w,h) = self.im8_1.getSize()
        
        self._drawWells(self.im8_1)
        
        valuedWatershed(self.im8_1,self.im8_2, SQUARE)
        (x,y) = compare(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testFastSKIZ(self):
        """Verifies the fast SKIZ operator based on watershed"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self.im1_3.fill(1)
        drawLine(self.im1_3, (w//2,0,w//2,h-1), 0)
        drawLine(self.im1_3, (0,h//2,w-1,h//2), 0)
        fastSKIZ(self.im1_1, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def testGeodesicSKIZ(self):
        """Verifies the geodesic SKIZ operator based on watershed"""
        (w,h) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_1.setPixel(1, (3*w//4,h//4))
        self.im1_1.setPixel(1, (w//4,h//4))
        self.im1_1.setPixel(1, (w//4,3*h//4))
        self.im1_1.setPixel(1, (3*w//4,3*h//4))
        self.im1_4.reset()
        drawSquare(self.im1_4, (5,5,w-6,h//2-6), 1)
        drawSquare(self.im1_4, (5,h//2+5,w-6,h-6), 1)
        drawSquare(self.im1_4, (w//2+5,5,w-6,h-6), 1)
        copy(self.im1_4, self.im1_3)
        drawLine(self.im1_3, (w//2,0,w//2,h-1), 0)
        drawLine(self.im1_3, (0,h//2,w-1,h//2), 0)
        geodesicSKIZ(self.im1_1, self.im1_4, self.im1_2, SQUARE)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
    def _drawSquares(self, imOut):
        (w,h) = imOut.getSize()
        
        for i in range(w//4):
            drawSquare(imOut, (i,i,w-1-i,h-1-i), i+1)
        for i in range(w//4):
            drawSquare(imOut, (i+w//4,i+w//4,w-1-i-w//4,h-1-i-w//4), w//2+i*2)
        
    def testMosaic(self):
        """Verifies the computation of mosaic image using watershed segment"""
        (w,h) = self.im8_1.getSize()
        
        self._drawSquares(self.im8_1)
        mosaic(self.im8_1, self.im8_2, self.im8_3, SQUARE)
            
        self.im8_5.fill(1)
        drawSquare(self.im8_5, (w//4,w//4+1,w-2-w//4,h-1-w//4), w-2)
        (x,y) = compare(self.im8_2, self.im8_5, self.im8_5)
        self.assertLess(x, 0)
        self.im8_5.reset()
        drawBox(self.im8_5, (w//4,w//4,w-1-w//4,h-1-w//4), 255)
        (x,y) = compare(self.im8_3, self.im8_5, self.im8_5)
        self.assertLess(x, 0)
        
        mosaic(self.im8_1, self.im8_1, self.im8_3, SQUARE)
            
        self.im8_5.fill(1)
        drawSquare(self.im8_5, (w//4,w//4+1,w-2-w//4,h-1-w//4), w-2)
        (x,y) = compare(self.im8_1, self.im8_5, self.im8_5)
        self.assertLess(x, 0)
        
    def testMosaicGradient(self):
        """Verifies the computation of mosaic gradient using watershed segment"""
        (w,h) = self.im8_1.getSize()
        
        self._drawSquares(self.im8_1)
        mosaicGradient(self.im8_1, self.im8_2, SQUARE)
            
        self.im8_5.reset()
        drawBox(self.im8_5, (w//4,w//4,w-1-w//4,h-1-w//4), w-3)
        (x,y) = compare(self.im8_2, self.im8_5, self.im8_5)
        self.assertLess(x, 0)
        
        mosaicGradient(self.im8_1, self.im8_1, SQUARE)
            
        self.im8_5.reset()
        drawBox(self.im8_5, (w//4,w//4,w-1-w//4,h-1-w//4), w-3)
        (x,y) = compare(self.im8_1, self.im8_5, self.im8_5)
        self.assertLess(x, 0)
        
        # Doesn't test anything just here to enter the mosaicGradient while
        # loop and make sure everything is ok inside
        for i in range(w):
            for j in range(h):
                self.im8_1.fastSetPixel(random.randint(0,255), (i,j))
        mosaicGradient(self.im8_1, self.im8_1)

