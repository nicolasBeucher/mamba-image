"""
Test cases for the image division function.

The function works on greyscale and 32-bit depths. The function returns an
image where the pixels first are divided by the pixels of the second. Thus
the result image must at least be as deep as the first input image.
If not, the function raises an error.

Here is the list of legal division operations :
     8 / 8 = 8
     8 / 8 =32
    32 / 8 =32
    32 /32 =32

Python function:
    div
    
C function:
    MB_Div
"""

from mamba import *
import unittest
import random

class TestDiv(unittest.TestCase):

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
        self.assertRaises(MambaError, div, self.im1_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im8_2, self.im8_1)
        #self.assertRaises(MambaError, div, self.im8_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, div, self.im32_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, div, self.im8_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, div, self.im32_3, self.im8_2, self.im32_1)
        self.assertRaises(MambaError, div, self.im1_3, self.im32_2, self.im32_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im32_2, self.im32_1)
        #self.assertRaises(MambaError, div, self.im32_3, self.im32_2, self.im32_1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, div, self.im8_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im8s2_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im8_3, self.im8s2_2, self.im8s2_1)
        self.assertRaises(MambaError, div, self.im8s2_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, div, self.im8s2_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, div, self.im8s2_3, self.im8s2_2, self.im8_1)

    def testComputation_8_8_8(self):
        """Divides two 8-bit images into a 8-bit image"""
        self.im8_3.reset()
        for i in range(1000):
            v1 = random.randint(0,255)
            v2 = random.randint(1,255)
            self.im8_1.fill(v1)
            self.im8_2.fill(v2)
            div(self.im8_1, self.im8_2, self.im8_3)
            self.assertEqual(self.im8_3.getPixel((0,0)), v1//v2)
            
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        self.im8_3.fill(1)
        div(self.im8_1, self.im8_2, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)
            
        self.im8_1.fill(0)
        self.im8_2.fill(0)
        self.im8_3.fill(255)
        div(self.im8_1, self.im8_2, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)

    def testComputation_8_8_32(self):
        """Divides two 8-bit images into a 32-bit image"""
        self.im32_3.reset()
        for i in range(1000):
            v1 = random.randint(0,255)
            v2 = random.randint(1,255)
            self.im8_1.fill(v1)
            self.im8_2.fill(v2)
            div(self.im8_1, self.im8_2, self.im32_3)
            r = self.im32_3.getPixel((0,0))
            self.assertEqual(r, v1//v2, "%d %d (%d,%d)" % (r,v1//v2,v1,v2))
            
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        self.im32_3.fill(1)
        div(self.im8_1, self.im8_2, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)
            
        self.im8_1.fill(0)
        self.im8_2.fill(0)
        self.im32_3.fill(0xffffffff)
        div(self.im8_1, self.im8_2, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)

    def testComputation_32_8_32(self):
        """Divides a 32-bit image with a 8-bit image into a 32-bit image"""
        self.im32_3.reset()
        for i in range(0,2000):
            v1 = random.randint(1,255)
            self.im8_1.fill(v1)
            self.im32_1.fill(i*50)
            self.im32_3.fill((i*50)//v1)
            div(self.im32_1, self.im8_1, self.im32_2)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)

    def testComputation_32_32_32(self):
        """Divides two 32-bit images into a 32-bit image"""
        self.im32_3.reset()
        for i in range(0,2000):
            v1 = random.randint(1,100000)
            self.im32_2.fill(v1)
            self.im32_1.fill(i*5)
            self.im32_3.fill((i*5)//v1)
            div(self.im32_1, self.im32_2, self.im32_2)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)

