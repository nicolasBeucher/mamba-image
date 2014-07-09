"""
Test cases for the image addition function.

The function works on all images depth. The function returns an image where the
pixels of the two input images have been added. Thus the result image must at
least be as deep as the deepest input image. If not, the function raises an error.
Other cases are legal (with an exception for the binary images).

Here is the list of legal addition operations :
     1 + 1 = 1
     1 + 8 = 8
     8 + 1 = 8
     1 + 8 =32
     8 + 1 =32
     1 +32 =32
    32 + 1 =32
     8 + 8 = 8
     8 + 8 =32
     8 +32 =32
    32 + 8 =32
    32 +32 =32
    
When the result is an 8-bit image or a binary image, the result is saturated so 
that it does not exceed the range (0-255 or 0-1) of possible values.

Python function:
    add
    
C function:
    MB_Add
"""

from mamba import *
import unittest
import random

class TestAdd(unittest.TestCase):

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
        """Tests incorrect depth raise an exception"""
        self.assertRaises(MambaError, add, self.im8_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im32_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im1_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im8_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im32_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im1_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im8_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im32_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, add, self.im1_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im32_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im32_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im1_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im8_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im32_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im1_3, self.im1_2, self.im32_1)

    def testSizeCheck(self):
        """Tests different size raise an exception"""
        self.assertRaises(MambaError, add, self.im8_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, add, self.im8_3, self.im8s2_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im8_3, self.im8s2_2, self.im8s2_1)
        self.assertRaises(MambaError, add, self.im8s2_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, add, self.im8s2_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, add, self.im8s2_3, self.im8s2_2, self.im8_1)

    def testComputation_1_1_1(self):
        """Tests the result of two binary images added into a third"""
        self.im1_1.fill(1)
        self.im1_2.reset()
        add(self.im1_2, self.im1_1, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0, "1+0!=1 in (%d,%d)" % (x,y))
        self.im1_2.fill(1)
        self.im1_1.reset()
        add(self.im1_2, self.im1_1, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "0+1!=1 in (%d,%d)" % (x,y))
        self.im1_2.fill(1)
        self.im1_1.fill(1)
        add(self.im1_2, self.im1_1, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0, "1+1!=1 in (%d,%d)" % (x,y))
        self.im1_2.reset()
        self.im1_1.reset()
        add(self.im1_2, self.im1_1, self.im1_3)
        (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
        self.assertLess(x, 0, "0+0!=0 in (%d,%d)" % (x,y))

    def testComputation_1_8_8(self):
        """Tests the result of accumulation of binary images into 8bit images"""
        v = random.randint(0,255)
        self.im8_3.fill(255)
        self.im1_1.reset()
        self.im8_2.fill(v)
        
        add(self.im8_2, self.im1_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), v, 
                     "v[%d in 8] + 0[in 1] !=v / =%d in (0,0)" % (v,self.im8_2.getPixel((0,0))))
        
        self.im8_2.reset()
        self.im1_1.fill(1)
        for i in range(255):
            if i%2==0:
                add(self.im8_2, self.im1_1, self.im8_2)
            else:
                add(self.im1_1, self.im8_2, self.im8_2)
            self.assertEqual(self.im8_2.getPixel((0,0)), i+1,
                         "v[%d in 8] + 1[in 1] !=v+1[%d in 8] / =%d in (0,0)" % (i,i+1,self.im8_2.getPixel((0,0))))
        
        add(self.im8_2, self.im1_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 255)
        add(self.im8_2, self.im1_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 255)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testComputation_1_8_32(self):
        """Adds binary image into 8bit image and result in a 32bit image"""
        self.im1_1.fill(1)
        self.im8_2.reset()
        self.im32_3.reset()
        self.im32_2.fill(256)
        for i in range(255):
            self.im8_2.fill(i)
            if i%2==0:
                add(self.im8_2, self.im1_1, self.im32_3)
            else:
                add(self.im1_1, self.im8_2, self.im32_3)
            self.assertEqual(self.im32_3.getPixel((0,0)), i+1)
        
        self.im8_2.fill(255)
        add(self.im8_2, self.im1_1, self.im32_3)
        self.assertEqual(self.im32_3.getPixel((0,0)), 256)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

    def testComputation_8_8_8(self):
        """Adds greyscale images into 8bit image and checks saturation"""
        self.im8_1.fill(1)
        self.im8_2.reset()
        self.im8_3.fill(255)
        for i in range(255):
            add(self.im8_2, self.im8_1, self.im8_2)
            self.assertEqual(self.im8_2.getPixel((0,0)), i+1)
        
        add(self.im8_2, self.im8_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 255)
        add(self.im8_2, self.im8_1, self.im8_2)
        self.assertEqual(self.im8_2.getPixel((0,0)), 255)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

    def testComputation_8_8_32(self):
        """Adds greyscale images into 32bit image"""
        v = random.randint(0,255)
        self.im8_1.fill(v)
        self.im32_3.reset()
        self.im32_2.fill(v+255)
        for i in range(255):
            self.im8_2.fill(i+1)
            add(self.im8_2, self.im8_1, self.im32_3)
            self.assertEqual(self.im32_3.getPixel((0,0)), v+i+1)
            
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)

    def testComputation_1_32_32(self):
        """Tests the result of accumulation of binary images into 32bit images"""
        v = random.randint(1,500000)
        self.im1_1.fill(1)
        self.im32_3.reset()
        self.im32_2.fill(v)
        for i in range(1000):
            if i%2==0:
                add(self.im32_2, self.im1_1, self.im32_2)
            else:
                add(self.im1_1, self.im32_2, self.im32_2)
            self.assertEqual(self.im32_2.getPixel((0,0)), v+i+1)

    def testComputation_8_32_32(self):
        """Tests the result of accumulation of 8bit images into 32bit images"""
        (w,h) = self.im8_1.getSize()
        v1 = random.randint(1,200000)
        v2 = random.randint(1,4)
        self.im8_1.fill(v2)
        self.im32_3.reset()
        self.im32_2.fill(v1)
        for i in range(600):
            if i%2==0:
                add(self.im32_2, self.im8_1, self.im32_2)
            else:
                add(self.im8_1, self.im32_2, self.im32_2)
            v = v1+(i+1)*v2
            self.assertEqual(self.im32_2.getPixel((0,0)), v)
            vol = computeVolume(self.im32_2)
            self.assertEqual(vol, w*h*v, "[%d,%d] : %d : %d!=%d" %(w,h,v,vol,w*h*v))

    def testComputation_32_32_32(self):
        """Adds 32bit images into a 32bit image"""
        self.im32_3.reset()
        for i in range(100):
            v1 = random.randint(1,200000)
            v2 = random.randint(1,400000)
            self.im32_1.fill(v1)
            self.im32_2.fill(v2)
            add(self.im32_2, self.im32_1, self.im32_3)
            self.assertEqual(self.im32_3.getPixel((0,0)), v1+v2)

