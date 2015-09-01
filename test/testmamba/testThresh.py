"""
Test cases for the image threshold function.

The function works with all 8-bit and 32-bit images as input and puts the output 
in a binary image.

Here is the list of legal operations :
    threshold(8) = 1
    threshold(32) =1
    
The result in output is a binary image where pixels are set to True if the 
corresponding pixel in the input image is inside the range given in parameter.
The pixel is set to False otherwise.

Python function:
    threshold
    
C function:
    MB_Thresh
"""

from mamba import *
import unittest
import random

class TestThresh(unittest.TestCase):

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
        self.im8s2_1 = imageMb(128,128,8)
        
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
        del(self.im8s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, threshold, self.im1_1, self.im1_2, 0, 0)
        self.assertRaises(MambaError, threshold, self.im1_1, self.im8_2, 0, 0)
        self.assertRaises(MambaError, threshold, self.im1_1, self.im32_2, 0, 0)
        #self.assertRaises(MambaError, threshold, self.im8_1, self.im1_2, 0, 0)
        self.assertRaises(MambaError, threshold, self.im8_1, self.im8_2, 0, 0)
        self.assertRaises(MambaError, threshold, self.im8_1, self.im32_2, 0, 0)
        #self.assertRaises(MambaError, threshold, self.im32_1, self.im1_2, 0, 0)
        self.assertRaises(MambaError, threshold, self.im32_1, self.im8_2, 0, 0)
        self.assertRaises(MambaError, threshold, self.im32_1, self.im32_2, 0, 0)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, threshold, self.im8s2_1, self.im1_1, 0, 0)
        self.assertRaises(MambaError, threshold, self.im8_1, self.im1s2_1, 0, 0)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        self.assertRaises(MambaError, threshold, self.im8_1, self.im1_2, 255, 0)
        self.assertRaises(MambaError, threshold, self.im32_1, self.im1_2, 2000, 0)

    def testComputation_8_1(self):
        """Thresholding 8-bit image into binary image"""
        (w,h) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for wi in range(w):
            for hi in range(h):
                self.im8_1.setPixel(wi, (wi,hi))
                
        for i in range(256):
            for hi in range(h):
                self.im1_1.setPixel(1, (i,hi))
                self.im1_2.setPixel(1, (w-1-i,hi))
            threshold(self.im8_1, self.im1_3, 0, i)
            (x,y) = compare(self.im1_1, self.im1_3, self.im1_3)
            self.assertLess(x, 0)
            threshold(self.im8_1, self.im1_3, 255-i, 255)
            (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
            self.assertLess(x, 0)
            

    def testComputation_32_1(self):
        """Thresholding 32-bit image into binary image"""
        (w,h) = self.im32_1.getSize()
        
        vi = random.randint(0,200000)
        
        self.im32_1.reset()
        for wi in range(w):
            for hi in range(h):
                self.im32_1.setPixel(vi+wi, (wi,hi))
                
        for i in range(256):
            for hi in range(h):
                self.im1_1.setPixel(1, (i,hi))
                self.im1_2.setPixel(1, (w-1-i,hi))
            threshold(self.im32_1, self.im1_3, vi, vi+i)
            (x,y) = compare(self.im1_1, self.im1_3, self.im1_3)
            self.assertLess(x, 0)
            threshold(self.im32_1, self.im1_3, vi+255-i, vi+255)
            (x,y) = compare(self.im1_2, self.im1_3, self.im1_3)
            self.assertLess(x, 0)

