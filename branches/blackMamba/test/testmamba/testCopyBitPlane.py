"""
Test cases for the image bit plane copy function.

The function works with 8-bit and binary images. 

Here is the list of legal operations:
     8[plane] -> 1
     1        -> 8[plane]
    
You can either extract a bit plane of a 8-bit image into a binary image or insert
the binary image into the bit plane of an 8-bit image. There is only 8 bit planes
in the 8-bit image, numbered 0(LSB) to 7(MSB).

Python function:
    copyBitPlane
    
C function:
    MB_CopyBitPlane
"""

from mamba import *
import unittest
import random

class TestCopyBitPlane(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
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
        del(self.im8_1)
        del(self.im8_2)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im1s2_1)
        del(self.im8s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, copyBitPlane, self.im1_1, 0, self.im1_2)
        #self.assertRaises(MambaError, copyBitPlane, self.im1_1, 0, self.im8_2)
        self.assertRaises(MambaError, copyBitPlane, self.im1_1, 0, self.im32_2)
        #self.assertRaises(MambaError, copyBitPlane, self.im8_1, 0, self.im1_2)
        self.assertRaises(MambaError, copyBitPlane, self.im8_1, 0, self.im8_2)
        self.assertRaises(MambaError, copyBitPlane, self.im8_1, 0, self.im32_2)
        self.assertRaises(MambaError, copyBitPlane, self.im32_1, 0, self.im1_2)
        self.assertRaises(MambaError, copyBitPlane, self.im32_1, 0, self.im8_2)
        self.assertRaises(MambaError, copyBitPlane, self.im32_1, 0, self.im32_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, copyBitPlane, self.im1s2_1, 0, self.im8_1)
        self.assertRaises(MambaError, copyBitPlane, self.im1_1, 0, self.im8s2_1)
        
    def testParameterRange(self):
        """Verifies that an incorrect parameter raises an exception"""
        for i in range(8,500000):
            self.assertRaises(MambaError, copyBitPlane, self.im1_1, i, self.im8_2)

    def testCopy_1_8(self):
        """Verifies the copy of binary image into 8-bit image bit plane"""
        for p in range(0,8):
            self.im8_1.reset()
            self.im1_1.fill(1)
            copyBitPlane(self.im1_1, p, self.im8_1)
            self.im8_2.fill(1<<p)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_2)
            self.assertLess(x, 0)
            self.im8_1.fill(255)
            self.im1_1.reset()
            copyBitPlane(self.im1_1, p, self.im8_1)
            self.im8_2.fill(255-(1<<p))
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_2)
            self.assertLess(x, 0)

    def testCopy_8_1(self):
        """Verifies the copy of 8-bit image bit plane into binary image"""
        for i in range(256):
            self.im8_1.fill(i)
            for p in range(0,8):
                self.im1_2.fill((i>>p)&1)
                copyBitPlane(self.im8_1, p, self.im1_1)
                (x,y) = compare(self.im1_1, self.im1_2, self.im1_2)
                self.assertLess(x, 0)

