"""
Test cases for the filtering operators found in the filter3D
module of mamba3D package. 

Python functions:
    alternateFilter3D
    fullAlternateFilter3D
    linearAlternateFilter3D
    autoMedian3D
    simpleLevelling3D
    strongLevelling3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestFilter3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(64,64,64,1)
        self.im1_2 = image3DMb(64,64,64,1)
        self.im1_3 = image3DMb(64,64,64,1)
        self.im1_4 = image3DMb(64,64,64,1)
        self.im1_5 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(64,64,32,8)
        self.im8_2 = image3DMb(64,64,32,8)
        self.im8_3 = image3DMb(64,64,32,8)
        self.im8_4 = image3DMb(64,64,32,8)
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
        
    def _drawBox3D(self, im, size, value):
        (w,h,l) = im.getSize()
        (x1,y1,z1,x2,y2,z2) = size
        
        drawSquare(im[z1], (x1,y1,x2,y2), value)
        drawSquare(im[z2], (x1,y1,x2,y2), value)
        for i in range(z1+1,z2):
            drawBox(im[i], (x1,y1,x2,y2), value)
        
    def _drawAlternated3D(self, imOut):
        (w,h,l) = imOut.getSize()
        
        imOut.reset()
        drawCube(imOut, (0,h//2,l//2,w-1,h-1,l-1), 255)
        imOut.setPixel(255, (w//4,h//4,l//4))
        imOut.setPixel(0, (w//4,3*h//4,3*l//4))
        drawCube(imOut, (w//2-1,h//4-1,l//4-1,w//2+1,h//4+1,l//4+1), 255)
        drawCube(imOut, (w//2-1,3*h//4-1,3*l//4-1,w//2+1,3*h//4+1,3*l//4+1), 0)
        self._drawBox3D(imOut, (3*w//4-1,h//4-1,l//4-1,3*w//4+2,h//4+2,l//4+2), 255)
        self._drawBox3D(imOut, (3*w//4-2,h//4-2,l//4-2,3*w//4+3,h//4+3,l//4+3), 255)
        self._drawBox3D(imOut, (3*w//4-1,3*h//4-1,3*l//4-1,3*w//4+2,3*h//4+2,3*l//4+2), 0)
        self._drawBox3D(imOut, (3*w//4-2,3*h//4-2,3*l//4-2,3*w//4+3,3*h//4+3,3*l//4+3), 0)
        
    def testAlternateFilter3D(self):
        """Verifies the alternate filter 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self._drawAlternated3D(self.im8_1)
        alternateFilter3D(self.im8_1, self.im8_2, 1, True, CUBE3X3X3)
        self.im8_3.reset()
        drawCube(self.im8_3, (0,h//2,l//2,w-1,h-1,l-1), 255)
        drawCube(self.im8_3, (w//2-1,h//4-1,l//4-1,w//2+1,h//4+1,l//4+1), 255)
        drawCube(self.im8_3, (w//2-1,3*h//4-1,3*l//4-1,w//2+1,3*h//4+1,3*l//4+1), 0)
        drawCube(self.im8_3, (3*w//4-2,3*h//4-2,3*l//4-2,3*w//4+3,3*h//4+3,3*l//4+3), 0)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        alternateFilter3D(self.im8_1, self.im8_2, 1, False, CUBE3X3X3)
        self.im8_3.reset()
        drawCube(self.im8_3, (0,h//2,l//2,w-1,h-1,l-1), 255)
        drawCube(self.im8_3, (w//2-1,h//4-1,l//4-1,w//2+1,h//4+1,l//4+1), 255)
        drawCube(self.im8_3, (w//2-1,3*h//4-1,3*l//4-1,w//2+1,3*h//4+1,3*l//4+1), 0)
        drawCube(self.im8_3, (3*w//4-2,h//4-2,l//4-2,3*w//4+3,h//4+3,l//4+3), 255)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testFullAlternateFilter3D(self):
        """Verifies the full alternate filter 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self._drawAlternated3D(self.im8_1)
        fullAlternateFilter3D(self.im8_1, self.im8_2, 2, True, CUBE3X3X3)
        self.im8_3.reset()
        drawCube(self.im8_3, (0,h//2,l//2,w-1,h-1,l-1), 255)
        drawCube(self.im8_3, (3*w//4-2,3*h//4-2,3*l//4-2,3*w//4+3,3*h//4+3,3*l//4+3), 0)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        fullAlternateFilter3D(self.im8_1, self.im8_2, 2, False, CUBE3X3X3)
        self.im8_3.reset()
        drawCube(self.im8_3, (0,h//2,l//2,w-1,h-1,l-1), 255)
        drawCube(self.im8_3, (3*w//4-2,h//4-2,l//4-2,3*w//4+3,h//4+3,l//4+3), 255)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def _drawAlternatedSeg3D(self, imOut):
        (w,h,l) = imOut.getSize()
        imOut.reset()
        drawCube(imOut, (0,h//2,l//2,w-1,h-1,l-1), 255)
        
        drawLine3D(imOut, (w//4,h//4-1,l//4-1,w//4,h//4+1,l//4+1), 255)
        drawLine3D(imOut, (w//4,3*h//4-1,3*l//4-1,w//4,3*h//4+1,3*l//4+1), 0)
        
        drawLine3D(imOut, (3*w//4-1,h//4-3,l//4-3,3*w//4-1,h//4+2,l//4+2), 255)
        drawLine3D(imOut, (3*w//4,h//4-3,l//4-3,3*w//4,h//4+2,l//4+2), 255)
        drawLine3D(imOut, (3*w//4,h//4-1,l//4-1,3*w//4,h//4,l//4), 0)
        drawLine3D(imOut, (3*w//4+1,h//4-3,l//4-3,3*w//4+1,h//4+2,l//4+2), 255)
        
        drawLine3D(imOut, (3*w//4-1,3*h//4-3,3*l//4-3,3*w//4-1,3*h//4+2,3*l//4+2), 0)
        drawLine3D(imOut, (3*w//4,3*h//4-3,3*l//4-3,3*w//4,3*h//4+2,3*l//4+2), 0)
        drawLine3D(imOut, (3*w//4,3*h//4-1,3*l//4-1,3*w//4,3*h//4,3*l//4), 255)
        drawLine3D(imOut, (3*w//4+1,3*h//4-3,3*l//4-3,3*w//4+1,3*h//4+2,3*l//4+2), 0)
        
    def testLinearAlternateFilter3D(self):
        """Verifies the linear alternate filter operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self._drawAlternatedSeg3D(self.im8_1)
        linearAlternateFilter3D(self.im8_1, self.im8_2, 4, True, CUBIC)
        self.im8_3.reset()
        drawCube(self.im8_3, (0,h//2,l//2,w-1,h-1,l-1), 255)
        drawLine3D(self.im8_3, (3*w//4-1,h//4-3,l//4-3,3*w//4-1,h//4+2,l//4+2), 255)
        drawLine3D(self.im8_3, (3*w//4+1,h//4-3,l//4-3,3*w//4+1,h//4+2,l//4+2), 255)
        drawLine3D(self.im8_3, (3*w//4-1,3*h//4-3,3*l//4-3,3*w//4-1,3*h//4+2,3*l//4+2), 0)
        drawLine3D(self.im8_3, (3*w//4+1,3*h//4-3,3*l//4-3,3*w//4+1,3*h//4+2,3*l//4+2), 0)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "%d,%d,%d" % (x,y,z))
        linearAlternateFilter3D(self.im8_1, self.im8_2, 4, False, CUBIC)
        self.im8_3.reset()
        drawCube(self.im8_3, (0,h//2,l//2,w-1,h-1,l-1), 255)
        drawLine3D(self.im8_3, (3*w//4-1,h//4-3,l//4-3,3*w//4-1,h//4+2,l//4+2), 255)
        drawLine3D(self.im8_3, (3*w//4+1,h//4-3,l//4-3,3*w//4+1,h//4+2,l//4+2), 255)
        drawLine3D(self.im8_3, (3*w//4-1,3*h//4-3,3*l//4-3,3*w//4-1,3*h//4+2,3*l//4+2), 0)
        drawLine3D(self.im8_3, (3*w//4+1,3*h//4-3,3*l//4-3,3*w//4+1,3*h//4+2,3*l//4+2), 0)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
    def testAutoMedian3D(self):
        """Tests the auto median filter 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        for n in range(1,6):
            value = n%2==1 and 255 or 0
            self.im8_1.fill(value)
            drawCube(self.im8_1, (w//2-n,h//2-n,l//2-n,w//2+n,h//2+n,l//2+n), 100)
            for i in range(n+1):
                autoMedian3D(self.im8_1, self.im8_2, i, se=CUBE3X3X3)
                (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
                self.assertLess(x, 0)
            self.im8_3.fill(value)
            autoMedian3D(self.im8_1, self.im8_2, n+1, se=CUBE3X3X3)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)
            
    def testSimpleLevelling3D(self):
        """Verifies the simple levelling 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(21):
            drawLine3D(self.im8_1, (w//2-10+i, h//2-10, l//2-10, w//2-10+i, h//2+10, l//2+10), 101+i)
        
        for i in range(22):
            self.im8_4.reset()
            drawCube(self.im8_4, (w//2-10, h//2-10, l//2-10, w//2+10, h//2+10, l//2+10), 100+i)
            self.im8_3.reset()
            for j in range(21):
                drawLine3D(self.im8_3, (w//2-10+j, h//2-10, l//2-10, w//2-10+j, h//2+10, l//2+10), min(101+j,100+i))
            
            simpleLevelling3D(self.im8_1, self.im8_4, self.im8_2, CUBIC)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "%d" % (i))
            
    def testStrongLevelling3D(self):
        """Verifies the strong levelling 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(21):
            drawSquare(self.im8_1[l//2-10+i], (w//2-10, h//2-10, w//2+10, h//2+10), 101+i)
        
        for i in range(12):
            self.im8_3.reset()
            if i<11:
                for j in range(21-2*i):
                    drawSquare(self.im8_3[l//2-10+j], (w//2-10, h//2-10, w//2+10, h//2+10), 101+j)
                for j in range(21-2*i, 21):
                    drawSquare(self.im8_3[l//2-10+j], (w//2-10, h//2-10, w//2+10, h//2+10), 121-2*i)
            
            strongLevelling3D(self.im8_1, self.im8_2, i, (i%2==1), CUBIC)
            (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" % (i,x,y,z))

