"""
Test cases for the image constant multiplication function.

The function works with 8-bit and 32-bit images. The function returns an image where 
the pixels of the input image have been multiplied by a given constant positive
value.

Here is the list of legal addition operations (where c is the constant):
     8 * c = 8
    32 * c =32
    
On 8-bit images, the result is saturated so that it does not exceed 255.

Python function:
    mulConst
    
C function:
    MB_ConMul
"""

from mamba import *
import unittest
import random

class TestConMul(unittest.TestCase):

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

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, mulConst, self.im1_2, 1, self.im1_1)
        self.assertRaises(MambaError, mulConst, self.im1_2, 1, self.im8_1)
        self.assertRaises(MambaError, mulConst, self.im1_2, 1, self.im32_1)
        self.assertRaises(MambaError, mulConst, self.im8_2, 1, self.im1_1)
        #self.assertRaises(MambaError, mulConst, self.im8_2, 1, self.im8_1)
        self.assertRaises(MambaError, mulConst, self.im8_2, 1, self.im32_1)
        self.assertRaises(MambaError, mulConst, self.im32_2, 1, self.im1_1)
        self.assertRaises(MambaError, mulConst, self.im32_2, 1, self.im8_1)
        #self.assertRaises(MambaError, mulConst, self.im32_2, 1, self.im32_1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, mulConst, self.im8s2_2, 1, self.im8_1)
        self.assertRaises(MambaError, mulConst, self.im8_2, 1, self.im8s2_1)

    def testComputation_8_8(self):
        """Multiplies a 8-bit image by a constant and puts the result in a 8-bit image"""
        for i in range(1000):
            vf = random.randint(0,255)
            vd = random.randint(0,255)
            self.im8_1.fill(vf)
            mulConst(self.im8_1, vd, self.im8_2)
            self.assertEqual(self.im8_2.getPixel((0,0)), min(vf*vd,255))
            
        self.im8_1.fill(127)
        self.im8_3.fill(254)
        mulConst(self.im8_1, 2, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
            
        self.im8_1.fill(1)
        self.im8_3.fill(2)
        mulConst(self.im8_1, 2, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testComputation_32_32(self):
        """Multiplies a 32-bit image by a constant and puts the result in a 32-bit image"""
        for i in range(1000):
            vf = random.randint(1,50000)
            vd = random.randint(0,60000)
            self.im32_1.fill(vf)
            mulConst(self.im32_1, vd, self.im32_2)
            if ((vf*vd)<0):
                v1 = hex(0xffffffff+vf*vd+1)
            else:
                v1 = hex(vf*vd)
            if (self.im32_2.getPixel((0,0))<0):
                v2 = hex(0xffffffff+self.im32_2.getPixel((0,0))+1)
            else:
                v2 = hex(self.im32_2.getPixel((0,0)))
            self.assertEqual(v2, v1, "[%d]x[%d] = [%s/%s]" %(vf,vd,v2,v1))
            
        self.im32_1.fill(0x3fffffff)
        self.im32_3.fill(0x7ffffffe)
        mulConst(self.im32_1, 2, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

