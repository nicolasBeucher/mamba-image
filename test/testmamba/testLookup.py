"""
Test cases for the image lookup transformation function

The function works only with 8-bit images.

The function transforms the input 8-bit image according to a given look-up
table (a 256 elements list) and put the result in a 8-bit output image.

Python function:
    lookup
    
C function:
    MB_Lookup
"""

from mamba import *
import unittest
import random

class TestLookup(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        self.im8s2_3 = imageMb(128,128,8)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im8s2_1)
        del(self.im8s2_2)
        del(self.im8s2_3)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        l = 256*[0]
        self.assertRaises(MambaError, lookup, self.im1_1, self.im1_2, l)
        self.assertRaises(MambaError, lookup, self.im1_1, self.im8_2, l)
        self.assertRaises(MambaError, lookup, self.im1_1, self.im32_2, l)
        self.assertRaises(MambaError, lookup, self.im8_1, self.im1_2, l)
        self.assertRaises(MambaError, lookup, self.im8_1, self.im32_2, l)
        self.assertRaises(MambaError, lookup, self.im32_1, self.im1_2, l)
        self.assertRaises(MambaError, lookup, self.im32_1, self.im8_2, l)
        self.assertRaises(MambaError, lookup, self.im32_1, self.im32_2, l)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        l = 256*[0]
        self.assertRaises(MambaError, lookup, self.im8s2_1, self.im8_2, l)
        self.assertRaises(MambaError, lookup, self.im8_1, self.im8s2_2, l)
        
    def testParameterRange(self):
        """Verifies that an incorrect parameter raises an exception"""
        l = 255*[0]
        self.assertRaises(ValueError, lookup, self.im8_1, self.im8_2, l)
        l = 255*(0,)
        self.assertRaises(TypeError, lookup, self.im8_1, self.im8_2, l)

    def testComputation(self):
        """Verifies the lookup table transformation of 8-bit image"""
        (w,h) = self.im8_1.getSize()
        
        for wi in range(w-1):
            for hi in range(h-1):
                self.im8_1.setPixel(wi, (wi,hi))
            
        vi = random.randint(1,255)
        luti = 256*[vi]
        lookup(self.im8_1, self.im8_2, luti)
        self.im8_3.fill(vi)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)
        
        luti = list(range(255,-1,-1))
        lookup(self.im8_1, self.im8_2, luti)
        negate(self.im8_1, self.im8_3)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)

