"""
Test cases for the image subtraction function.

The function works on all image depths. The function returns an image where the
pixels of the two input images have been subtracted. Thus the result image 
must at least be as deep as the deepest input image. If not, the function raises 
an error. Other cases are legal (with an exception for the binary images).

Here is the list of legal subtraction operations :
     1 - 1 = 1
     8 - 1 = 8
     8 - 8 = 8
     8 - 8 =32
    32 - 8 =32
     8 -32 =32
    32 -32 =32
    
When the result is an 8-bit image or a binary image, the result is saturated so 
that it does not exceed the range (0-255 or 0-1) of possible values.

Python function:
    sub
    
C function:
    MB_Sub
"""

from mamba import *
import unittest
import random

class TestSub(unittest.TestCase):

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
        #self.assertRaises(MambaError, sub, self.im1_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im1_2, self.im8_1)
        #self.assertRaises(MambaError, sub, self.im8_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im8_2, self.im8_1)
        #self.assertRaises(MambaError, sub, self.im8_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, sub, self.im32_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, sub, self.im8_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, sub, self.im32_3, self.im8_2, self.im32_1)
        self.assertRaises(MambaError, sub, self.im1_3, self.im32_2, self.im32_1)
        #self.assertRaises(MambaError, sub, self.im8_3, self.im32_2, self.im32_1)
        #self.assertRaises(MambaError, sub, self.im32_3, self.im32_2, self.im32_1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, sub, self.im8_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im8s2_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im8_3, self.im8s2_2, self.im8s2_1)
        self.assertRaises(MambaError, sub, self.im8s2_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, sub, self.im8s2_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, sub, self.im8s2_3, self.im8s2_2, self.im8_1)

    def testComputation_1_1_1(self):
        """Tests the subtraction with two binary images into a third one"""
        self.im1_1.reset()
        self.im1_2.reset()
        sub(self.im1_1, self.im1_2, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_1.reset()
        self.im1_2.fill(1)
        sub(self.im1_1, self.im1_2, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_1.fill(1)
        self.im1_2.reset()
        sub(self.im1_1, self.im1_2, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0)
        
        self.im1_1.fill(1)
        self.im1_2.fill(1)
        sub(self.im1_1, self.im1_2, self.im1_3)
        self.im1_1.reset()
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0)

    def testComputation_1_8_8(self):
        """Subtracts binary image out of 8-bit image into 8-bit image"""
        v = random.randint(0,255)
        self.im8_3.reset()
        self.im1_1.reset()
        self.im8_2.fill(v)
        
        sub(self.im8_2, self.im1_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), v)
        
        self.im8_2.fill(255)
        self.im1_1.fill(1)
        for i in range(255):
            sub(self.im8_2, self.im1_1, self.im8_2)
            self.assertEqual(self.im8_2.getPixel((0,0)), 255-(i+1))
        
        sub(self.im8_2, self.im1_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 0)
        sub(self.im8_2, self.im1_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 0)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testComputation_8_8_8(self):
        """Subtracts an 8-bit image out of an 8-bit image and into a 8-bit image"""
        self.im8_1.fill(1)
        self.im8_2.fill(255)
        for i in range(255):
            sub(self.im8_2, self.im8_1, self.im8_2)
            self.assertEqual(self.im8_2.getPixel((0,0)), 255-(i+1))
        
        sub(self.im8_2, self.im8_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 0)
        sub(self.im8_2, self.im8_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 0)
        
        self.im8_1.fill(255)
        self.im8_2.fill(50)
        self.im8_3.fill(0)
        sub(self.im8_2, self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im8_1.fill(0)
        self.im8_2.fill(50)
        self.im8_3.fill(50)
        sub(self.im8_2, self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testComputation_8_8_32(self):
        """Subtracts an 8-bit image out of an 8-bit image and into a 32-bit image"""
        self.im8_2.fill(255)
        for i in range(256):
            self.im8_1.fill(i)
            sub(self.im8_2, self.im8_1, self.im32_3)
            self.assertEqual(self.im32_3.getPixel((0,0)), 255-i)
        
        self.im8_1.fill(255)
        self.im8_2.fill(50)
        self.im32_3.fill(0xffffffff + 1 + (50 - 255))
        sub(self.im8_2, self.im8_1, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)
        
        self.im8_1.fill(0)
        self.im8_2.fill(50)
        self.im32_3.fill(50)
        sub(self.im8_2, self.im8_1, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

    def testComputation_8_32_32(self):
        """Subtracts an 8-bit image out of a 32-bit image and into a 32-bit image"""
        (w,h) = self.im8_1.getSize()
        v1 = random.randint(0,200000)
        v2 = random.randint(0,255)
        self.im8_1.fill(v2)
        self.im32_3.reset()
        self.im32_2.fill(v1)
        v = v1
        for i in range(100):
            sub(self.im32_2, self.im8_1, self.im32_2)
            v = v-v2
            if v<0:
                v = 0xffffffff + 1 + v
            self.assertEqual(self.im32_2.getPixel((0,0)), v)
            vol = computeVolume(self.im32_2)
            self.assertEqual(vol, (w*h*v), "[%d,%d] : %d : %d!=%d" %(w,h,v,vol,w*h*v))

    def testComputation_32_8_32(self):
        """Subtracts a 32-bit image out of a 8-bit image and into a 32-bit image"""
        (w,h) = self.im8_1.getSize()
        v1 = random.randint(0,200000)
        v2 = random.randint(0,255)
        self.im8_1.fill(v2)
        self.im32_3.reset()
        self.im32_2.fill(v1)
        v = v1
        for i in range(100):
            sub(self.im8_1, self.im32_2, self.im32_2)
            v = v2-v
            if v<0:
                v = 0xffffffff + 1 + v
            self.assertEqual(self.im32_2.getPixel((0,0)), v, "%d : %d %d %d %d" % (i,self.im32_2.getPixel((0,0)),v,v1,v2))
            vol = computeVolume(self.im32_2)
            self.assertEqual(vol, (w*h*v), "[%d,%d] : %d : %d!=%d" %(w,h,v,vol,w*h*v))

    def testComputation_32_32_32(self):
        """Subtracts 32-bit images into a 32-bit image"""
        self.im32_3.reset()
        for i in range(100):
            v1 = random.randint(0,200000)
            v2 = random.randint(0,200000)
            self.im32_1.fill(v1)
            self.im32_2.fill(v2)
            sub(self.im32_2, self.im32_1, self.im32_3)
            v = v2-v1
            if v<0:
                v = 0xffffffff + 1 + v
            self.assertEqual(self.im32_3.getPixel((0,0)), v)

