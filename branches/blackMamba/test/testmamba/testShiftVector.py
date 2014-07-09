"""
Test cases for the image shift by vector function.

The function works on all image depths. All images, both input and output, must
have the same depth.

Here is the list of legal operations :
    shiftVector( 1) = 1
    shiftVector( 8) = 8
    shiftVector(32) =32
    
The result in output is the input image shifted by the given vector. The 
created space is filled with the value given in argument.

Python function:
    shiftVector
    
C functions:
    MB_ShiftVectorb
    MB_ShiftVector8
    MB_ShiftVector32
"""

from mamba import *
import unittest
import random

class TestShiftVector(unittest.TestCase):

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
        
        self.dir = [
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
        #self.assertRaises(MambaError, shiftVector, self.im1_1, self.im1_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im1_1, self.im8_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im1_1, self.im32_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im8_1, self.im1_2,(0,1),1)
        #self.assertRaises(MambaError, shiftVector, self.im8_1, self.im8_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im8_1, self.im32_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im32_1, self.im1_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im32_1, self.im8_2,(0,1),1)
        #self.assertRaises(MambaError, shiftVector, self.im32_1, self.im32_2,(0,1),1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, shiftVector, self.im8s2_1, self.im8_2,(0,1),1)
        self.assertRaises(MambaError, shiftVector, self.im8_1, self.im8s2_2,(0,1),1)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        self.assertRaises(TypeError, shiftVector, self.im1_1, self.im1_2, 5, 0)
            
    def _squarePixelPrediction(self, im, d, x, y, amp, v):
        (w,h) = im.getSize()
    
        xpre = x+amp*self.dirS[d][0]
        ypre = y+amp*self.dirS[d][1]
        
        if xpre<w and xpre>=0 and ypre<h and ypre>=0:
            im.setPixel(v, (xpre,ypre))
        return (xpre,ypre)

    def testShifting_1(self):
        """Verifies shift by vector for binary image"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w//2-1)
            yi = random.randint(0,h//2-1)
            for d in self.dir:
                self.im1_1.reset()
                self.im1_3.reset()
                self.im1_1.setPixel(1, (w//2,h//2))
                self.im1_3.setPixel(1, (w//2+xi*d[0],h//2+yi*d[1]))
                shiftVector(self.im1_1, self.im1_1, (xi*d[0],yi*d[1]), 0)
                (x,y) = compare(self.im1_1, self.im1_3, self.im1_1)
                self.assertLess(x, 0)

    def testShifting_8(self):
        """Verifies shift by vector for greyscale image"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w//2-1)
            yi = random.randint(0,h//2-1)
            vi = random.randint(0,255)
            for d in self.dir:
                self.im8_1.reset()
                self.im8_3.reset()
                self.im8_1.setPixel(vi, (w//2,h//2))
                self.im8_3.setPixel(vi, (w//2+xi*d[0],h//2+yi*d[1]))
                shiftVector(self.im8_1, self.im8_1, (xi*d[0],yi*d[1]), 0)
                (x,y) = compare(self.im8_1, self.im8_3, self.im8_3)
                self.assertLess(x, 0)

    def testShifting_32(self):
        """Verifies shift by vector for 32-bit image"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(100):
            xi = random.randint(0,w//2-1)
            yi = random.randint(0,h//2-1)
            vi = random.randint(0,0xffffffff)
            for d in self.dir:
                self.im32_1.reset()
                self.im32_3.reset()
                self.im32_1.setPixel(vi, (w//2,h//2))
                self.im32_3.setPixel(vi, (w//2+xi*d[0],h//2+yi*d[1]))
                shiftVector(self.im32_1, self.im32_1, (xi*d[0],yi*d[1]), 0)
                (x,y) = compare(self.im32_1, self.im32_3, self.im32_3)
                self.assertLess(x, 0)
                
    def testFillValue_1(self):
        """Verifies the filling of created space due to shift by vector in binary image"""
        (w,h) = self.im1_1.getSize()
        
        created_space_volume = [0, w, h+w-1, h, h+w-1, w, h+w-1, h, h+w-1]
        for i,d in enumerate(self.dir):
            self.im1_1.fill(1)
            self.im1_2.reset()
            shiftVector(self.im1_1, self.im1_2, d, 0)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, w*h-created_space_volume[i])
            self.im1_1.reset()
            self.im1_2.reset()
            shiftVector(self.im1_1, self.im1_2, d, 1)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, created_space_volume[i], "in dir %d,%d : %d/%d" %(d[0],d[1],vol,created_space_volume[i]))
    
    def testFillValue_8(self):
        """Verifies the filling of created space due to shift by vector in 8-bit image"""
        (w,h) = self.im8_1.getSize()
        
        created_space_volume = [0, w, h+w-1, h, h+w-1, w, h+w-1, h, h+w-1]
        for i,d in enumerate(self.dir):
            vi = random.randint(2,255)
            self.im8_1.fill(vi)
            self.im8_2.reset()
            shiftVector(self.im8_1, self.im8_2, d, 0)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol//vi, w*h-created_space_volume[i])
            self.im8_1.reset()
            self.im8_2.reset()
            shiftVector(self.im8_1, self.im8_2, d, vi)
            vol = computeVolume(self.im8_2)
            self.assertEqual(vol//vi, created_space_volume[i], "in dir %d : %d/%d" %(i,vol,created_space_volume[i]))

