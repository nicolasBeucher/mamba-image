"""
Test cases for the binary image depth conversion by mask function.

The function works with binary images and converts them into 32-bit or 8-bit
images.

Here is the list of legal operations:
     1 -> 8
     1 ->32
    
When converting from binary, the pixels set to True are converted to a given 
value in the output image and the pixels set to False to another given value.

Python function:
    convertByMask
    
C function:
    MB_Mask
"""

from mamba import *
import unittest
import random

class TestMask(unittest.TestCase):

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
        self.im8s2_1 = imageMb(128,128,8)
        
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
        del(self.im8s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, convertByMask, self.im1_1, self.im1_2, 0, 0)
        #self.assertRaises(MambaError, convertByMask, self.im1_1, self.im8_2, 0, 0)
        #self.assertRaises(MambaError, convertByMask, self.im1_1, self.im32_2, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im8_1, self.im1_2, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im8_1, self.im8_2, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im8_1, self.im32_2, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im32_1, self.im1_2, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im32_1, self.im8_2, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im32_1, self.im32_2, 0, 0)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, convertByMask, self.im1_1, self.im8s2_1, 0, 0)
        self.assertRaises(MambaError, convertByMask, self.im1s2_1, self.im8_1, 0, 0)

    def testComputation_1_8(self):
        """Using binary image as mask to create 8-bit image"""
        (w,h) = self.im1_1.getSize()
        vi = random.randint(1,255)
        
        self.im1_1.fill(1)
        self.im8_2.fill(vi)
        convertByMask(self.im1_1, self.im8_1, 0, vi)
        (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        
        vi = random.randint(1,255)
        
        self.im1_1.reset()
        self.im8_2.fill(vi)
        convertByMask(self.im1_1, self.im8_1, vi, 0)
        (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
        
        vi = random.randint(10,250)
        self.im1_1.reset()
        self.im8_2.reset()
        for wi in range(w):
            for hi in range(h):
                if wi%2==0:
                    self.im1_1.setPixel(1, (wi,hi))
                    self.im8_2.setPixel(vi+1, (wi,hi))
                else:
                    self.im1_1.setPixel(0, (wi,hi))
                    self.im8_2.setPixel(vi, (wi,hi))
        convertByMask(self.im1_1, self.im8_1, vi, vi+1)
        (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
        self.assertLess(x, 0)
            

    def testComputation_1_32(self):
        """Using binary image as mask to create 32-bit image"""
        (w,h) = self.im1_1.getSize()
        
        vi = random.randint(0,0xffffffff)
        if vi==0:
            vi = 1
        self.im1_1.fill(1)
        self.im32_2.fill(vi)
        convertByMask(self.im1_1, self.im32_1, 0, vi)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
        vi = random.randint(0,0xffffffff)
        if vi==0:
            vi = 2
        self.im1_1.reset()
        self.im32_2.fill(vi)
        convertByMask(self.im1_1, self.im32_1, vi, 0)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)
        
        vi = random.randint(0,0xffffffff)
        if vi==0:
            vi = 15
        self.im1_1.reset()
        self.im32_2.reset()
        for wi in range(w):
            for hi in range(h):
                if wi%2==0:
                    self.im1_1.setPixel(1, (wi,hi))
                    self.im32_2.setPixel(vi+1, (wi,hi))
                else:
                    self.im1_1.setPixel(0, (wi,hi))
                    self.im32_2.setPixel(vi, (wi,hi))
        convertByMask(self.im1_1, self.im32_1, vi, vi+1)
        (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
        self.assertLess(x, 0)

