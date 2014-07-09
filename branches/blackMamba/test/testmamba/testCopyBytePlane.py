"""
Test cases for the image bit plane copy function.

The function works with 8-bit and 32-bit images. 

Here is the list of legal operations:
     32[plane] -> 8
     8         -> 32[plane]
    
You can either extract a byte plane of a 32-bit image into an 8-bit image or insert
the 8-bit image into the byte plane of an 32-bit image. There is only 4 byte planes
in a 32-bit image, numbered 0(LSByte) to 3(MSByte).

Python function:
    copyBytePlane
    
C function:
    MB_CopyBytePlane
"""

from mamba import *
import unittest
import random

class TestCopyBytePlane(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im32s2_1 = imageMb(128,128,32)
        self.im8s2_1 = imageMb(128,128,8)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32s2_1)
        del(self.im8s2_1)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, copyBytePlane, self.im1_1, 0, self.im1_2)
        self.assertRaises(MambaError, copyBytePlane, self.im1_1, 0, self.im8_2)
        self.assertRaises(MambaError, copyBytePlane, self.im1_1, 0, self.im32_2)
        self.assertRaises(MambaError, copyBytePlane, self.im8_1, 0, self.im1_2)
        self.assertRaises(MambaError, copyBytePlane, self.im8_1, 0, self.im8_2)
        #self.assertRaises(MambaError, copyBytePlane, self.im8_1, 0, self.im32_2)
        self.assertRaises(MambaError, copyBytePlane, self.im32_1, 0, self.im1_2)
        #self.assertRaises(MambaError, copyBytePlane, self.im32_1, 0, self.im8_2)
        self.assertRaises(MambaError, copyBytePlane, self.im32_1, 0, self.im32_2)
        
    def testParameterRange(self):
        """Verifies that an incorrect parameter raises an exception"""
        for i in range(4,500000):
            self.assertRaises(MambaError, copyBytePlane, self.im32_1, i, self.im8_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, copyBitPlane, self.im32s2_1, 0, self.im8_1)
        self.assertRaises(MambaError, copyBitPlane, self.im32_1, 0, self.im8s2_1)

    def testCopy_8_32(self):
        """Verifies the copy of 8-bit image into 32-bit image byte plane"""
        for i in range(256):
            for p in range(0,4):
                self.im8_1.fill(i)
                self.im32_1.reset()
                copyBytePlane(self.im8_1, p, self.im32_1)
                v = i<<(8*p)
                self.im32_2.fill(v)
                (x,y) = compare(self.im32_1, self.im32_2, self.im32_2)
                self.assertLess(x, 0)

    def testCopy_32_8(self):
        """Verifies the copy of 32-bit image byte plane into 8-bit image"""
        for i in range(256):
            for p in range(0,4):
                self.im8_1.reset()
                v = i<<(8*p)
                self.im32_1.fill(v)
                copyBytePlane(self.im32_1, p, self.im8_1)
                self.im8_2.fill(i)
                (x,y) = compare(self.im8_1, self.im8_2, self.im8_2)
                self.assertLess(x, 0)

