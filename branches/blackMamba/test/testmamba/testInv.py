"""
Test cases for the image negation/inversion function.

The function works on all image depths. The function returns an image where the
pixels are bitwise negated.

Here is the list of legal operations :
     !1 = 1
     !8 = 8
    !32 =32
    
Python function:
    negate
    
C function:
    MB_Inv
"""

from mamba import *
import unittest
import random

class TestInv(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
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
        self.assertRaises(MambaError, negate, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, negate, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, negate, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, negate, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, negate, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, negate, self.im32_1, self.im8_2)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, negate, self.im8s2_1, self.im8_2)
        self.assertRaises(MambaError, negate, self.im8_1, self.im8s2_2)

    def testComputation_1(self):
        """Verifies the inversion of binary images"""
        self.im1_1.fill(1)
        self.im1_3.reset()
        negate(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_3.fill(1)
        negate(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

    def testComputation_8(self):
        """Verifies the inversion of 8-bit images"""
        for i in range(256):
            self.im8_1.fill(i)
            negate(self.im8_1, self.im8_2)
            self.im8_3.fill(255-i)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
            self.assertLess(x, 0)

    def testComputation_32(self):
        """Verifies the inversion of 32-bit images"""
        for i in range(10000):
            vi = random.randint(1,550000)
            self.im32_1.fill(vi)
            negate(self.im32_1, self.im32_2)
            self.im32_3.fill(0xffffffff-vi)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
            self.assertLess(x, 0)

