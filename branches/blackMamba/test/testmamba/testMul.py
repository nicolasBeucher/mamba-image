"""
Test cases for the image multiplication function.

The function works on all image depths. The function returns an image where the
pixels of the two input images have been multiplied. Thus the result image must
at least be as deep as the deepest input image. If not, the function raises an 
error. Other cases are legal (with an exception for the binary images).

Here is the list of legal multiplication operations :
     1 * 1 = 1
     1 * 8 = 8
     8 * 1 = 8
     1 * 8 =32
     8 * 1 =32
     1 *32 =32
    32 * 1 =32
     8 * 8 = 8
     8 * 8 =32
     8 *32 =32
    32 * 8 =32
    32 *32 =32
    
When the result is an 8-bit image or a binary image, the result is saturated so 
that it does not exceed the range (0-255 or 0-1) of possible values.

Python function:
    mul
    
C function:
    MB_Mul
"""

from mamba import *
import unittest
import random

class TestMul(unittest.TestCase):

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
        #self.assertRaises(MambaError, mul, self.im1_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im8_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im32_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im1_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im8_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im32_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im1_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im8_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im32_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, mul, self.im1_3, self.im1_2, self.im8_1)
        #self.assertRaises(MambaError, mul, self.im8_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im32_3, self.im1_2, self.im8_1)
        #self.assertRaises(MambaError, mul, self.im1_3, self.im8_2, self.im8_1)
        #self.assertRaises(MambaError, mul, self.im8_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im32_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im1_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im8_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im32_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im1_3, self.im1_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im8_3, self.im1_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im32_3, self.im1_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im1_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im8_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im32_3, self.im8_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im1_3, self.im32_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im8_3, self.im32_2, self.im32_1)
        #self.assertRaises(MambaError, mul, self.im32_3, self.im32_2, self.im32_1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, mul, self.im8_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, mul, self.im8_3, self.im8s2_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im8_3, self.im8s2_2, self.im8s2_1)
        self.assertRaises(MambaError, mul, self.im8s2_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, mul, self.im8s2_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, mul, self.im8s2_3, self.im8s2_2, self.im8_1)

    def testComputation_1_1_1(self):
        """Tests the multiplication of two binary images into a third one"""
        (w,h) = self.im1_1.getSize()
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        
        drawSquare(self.im1_1,[w//2,0,w-1,h//2-1],1)
        drawSquare(self.im1_1,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_2,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_3,[0,h//2,w//2-1,h-1],1)
        drawSquare(self.im1_2,[w//2,h//2,w-1,h-1],1)
        
        mul(self.im1_2, self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0)

    def testComputation_1_8_8(self):
        """Multiplies a binary image with a 8-bit image into a 8-bit image"""
        self.im1_1.reset()
        self.im8_3.reset()
        for i in range(256):
            self.im8_1.fill(i)
            if i%2==0:
                mul(self.im8_1, self.im1_1, self.im8_2)
            else:
                mul(self.im1_1, self.im8_1, self.im8_2)
            (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
            self.assertLess(x, 0)
        self.im1_1.fill(1)
        for i in range(256):
            self.im8_1.fill(i)
            if i%2==0:
                mul(self.im8_1, self.im1_1, self.im8_2)
            else:
                mul(self.im1_1, self.im8_1, self.im8_2)
            (x,y) = compare(self.im8_1, self.im8_2, self.im8_2)
            self.assertLess(x, 0)


    def testComputation_8_8_8(self):
        """Multiplies two 8-bit images into a 8-bit image"""
        self.im8_3.reset()
        for i in range(1000):
            v1 = random.randint(0,255)
            v2 = random.randint(0,255)
            self.im8_1.fill(v1)
            self.im8_2.fill(v2)
            mul(self.im8_2, self.im8_1, self.im8_3)
            self.assertEqual(self.im8_3.getPixel((0,0)), min(v1*v2,255))
            
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        self.im8_3.fill(255)
        mul(self.im8_2, self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)
            
        self.im8_1.fill(0)
        self.im8_2.fill(255)
        self.im8_3.fill(0)
        mul(self.im8_2, self.im8_1, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_2)
        self.assertLess(x, 0)

    def testComputation_1_8_32(self):
        """Multiplies a binary image with a 8-bit image into a 32-bit image"""
        self.im1_1.reset()
        self.im32_3.reset()
        for i in range(256):
            self.im8_1.fill(i)
            if i%2==0:
                mul(self.im8_1, self.im1_1, self.im32_2)
            else:
                mul(self.im1_1, self.im8_1, self.im32_2)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
        self.im1_1.fill(1)
        for i in range(256):
            self.im8_1.fill(i)
            self.im32_1.fill(i)
            if i%2==0:
                mul(self.im8_1, self.im1_1, self.im32_2)
            else:
                mul(self.im1_1, self.im8_1, self.im32_2)
            (x,y) = compare(self.im32_1, self.im32_2, self.im32_2)
            self.assertLess(x, 0)

    def testComputation_1_32_32(self):
        """Multiplies a binary image with a 32-bit image into a 32-bit image"""
        self.im1_1.reset()
        self.im32_3.reset()
        for i in range(0,20000):
            self.im32_1.fill(i*50)
            if i%2==0:
                mul(self.im32_1, self.im1_1, self.im32_2)
            else:
                mul(self.im1_1, self.im32_1, self.im32_2)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)
        self.im1_1.fill(1)
        for i in range(0,20000):
            self.im32_1.fill(i*50)
            if i%2==0:
                mul(self.im32_1, self.im1_1, self.im32_2)
            else:
                mul(self.im1_1, self.im32_1, self.im32_2)
            (x,y) = compare(self.im32_1, self.im32_2, self.im32_2)
            self.assertLess(x, 0)

    def testComputation_8_8_32(self):
        """Multiplies two 8-bit images into a 32-bit image"""
        self.im32_3.reset()
        for i in range(1000):
            v1 = random.randint(0,255)
            v2 = random.randint(0,255)
            self.im8_1.fill(v1)
            self.im8_2.fill(v2)
            mul(self.im8_2, self.im8_1, self.im32_3)
            self.assertEqual(self.im32_3.getPixel((0,0)), v1*v2)
            
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        self.im32_3.fill(65025)
        mul(self.im8_2, self.im8_1, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)
            
        self.im8_1.fill(0)
        self.im8_2.fill(255)
        self.im32_3.fill(0)
        mul(self.im8_2, self.im8_1, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
        self.assertLess(x, 0)

    def testComputation_8_32_32(self):
        """Multiplies a 8-bit image with a 32-bit image into a 32-bit image"""
        self.im32_3.reset()
        for i in range(0,20000):
            v1 = random.randint(0,255)
            self.im8_1.fill(v1)
            self.im32_1.fill(i*50)
            self.im32_3.fill(i*50*v1)
            if i%2==0:
                mul(self.im32_1, self.im8_1, self.im32_2)
            else:
                mul(self.im8_1, self.im32_1, self.im32_2)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)

    def testComputation_32_32_32(self):
        """Multiplies two 32-bit images into a 32-bit image"""
        self.im32_3.reset()
        for i in range(0,2000):
            v1 = random.randint(0,100000)
            self.im32_2.fill(v1)
            self.im32_1.fill(i*5)
            self.im32_3.fill(i*5*v1)
            mul(self.im32_2, self.im32_1, self.im32_2)
            (x,y) = compare(self.im32_3, self.im32_2, self.im32_2)
            self.assertLess(x, 0)

