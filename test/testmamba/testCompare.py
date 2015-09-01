"""
Test cases for the image comparison function.

The function works with all depths. All the images must be of the same depth. The
function will return the position of the first pixel different in the two
input images and put the same pixel in the output image to the value of the 
first image pixel. If the two input images are identical the result is (-1,-1)
    
Python function:
    compare
    
C function:
    MB_Compare
"""

from mamba import *
import unittest
import random

class TestCompare(unittest.TestCase):

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
        
        self.neighbors = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
        
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
        #self.assertRaises(MambaError, compare, self.im1_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im1_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im8_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im32_2, self.im1_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im1_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im8_2, self.im8_1)
        #self.assertRaises(MambaError, compare, self.im8_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im32_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im1_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im8_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im8_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im32_3, self.im8_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im1_3, self.im32_2, self.im32_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im32_2, self.im32_1)
        #self.assertRaises(MambaError, compare, self.im32_3, self.im32_2, self.im32_1)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, compare, self.im8_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im8s2_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im8_3, self.im8s2_2, self.im8s2_1)
        self.assertRaises(MambaError, compare, self.im8s2_3, self.im8_2, self.im8_1)
        self.assertRaises(MambaError, compare, self.im8s2_3, self.im8_2, self.im8s2_1)
        self.assertRaises(MambaError, compare, self.im8s2_3, self.im8s2_2, self.im8_1)

    def testComputation_1(self):
        """Verifies the comparison of two binary images"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(1000):
            wi = random.randint(0,w-1)
            hi = random.randint(0,h-1)
            if i%3==0:
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_1.setPixel(1, (wi,hi))
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            elif i%3==1:
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_2.setPixel(1, (wi,hi))
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            else:
                self.im1_1.reset()
                self.im1_2.reset()
                self.im1_1.setPixel(1, (wi,hi))
                self.im1_2.setPixel(1, (wi,hi))
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertEqual(x, -1)
                self.assertEqual(y, -1)
        
        for i in range(100):
            wi1 = random.randint(0,w-1)
            hi1 = random.randint(0,h-1)
            diri = random.choice(self.neighbors)
            self.im1_1.reset()
            self.im1_2.reset()
            self.im1_1.setPixel(1, (wi1,hi1))
            wi2 = min(w-1, max(0, wi1+diri[0]))
            hi2 = min(h-1, max(0, hi1+diri[1]))
            if wi1!=wi2 or hi1!=hi2:
                self.im1_2.setPixel(1, (wi2,hi2))
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)

    def testComputation_8(self):
        """Verifies the comparison of two 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        for i in range(1200):
            wi = random.randint(0,w-1)
            hi = random.randint(0,h-1)
            vi = random.randint(1,255)
            if i%4==0:
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_1.setPixel(vi, (wi,hi))
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            elif i%4==1:
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_2.setPixel(vi, (wi,hi))
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            elif i%4==2:
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_1.setPixel(vi, (wi,hi))
                vi2 = (vi<255) and vi+1 or vi-1
                self.im8_2.setPixel(vi2, (wi,hi))
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            else:
                self.im8_1.reset()
                self.im8_2.reset()
                self.im8_1.setPixel(vi, (wi,hi))
                self.im8_2.setPixel(vi, (wi,hi))
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertEqual(x, -1)
                self.assertEqual(y, -1)
        
        for i in range(100):
            wi1 = random.randint(0,w-1)
            hi1 = random.randint(0,h-1)
            vi = random.randint(1,255)
            diri = random.choice(self.neighbors)
            self.im8_1.reset()
            self.im8_2.reset()
            self.im8_1.setPixel(vi, (wi1,hi1))
            wi2 = min(w-1, max(0, wi1+diri[0]))
            hi2 = min(h-1, max(0, hi1+diri[1]))
            if wi1!=wi2 or hi1!=hi2:
                self.im8_2.setPixel(vi, (wi2,hi2))
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)

    def testComputation_32(self):
        """Verifies the comparison of two 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        for i in range(1200):
            wi = random.randint(0,w-1)
            hi = random.randint(0,h-1)
            vi = random.randint(1,500005)
            if i%4==0:
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_1.setPixel(vi, (wi,hi))
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            elif i%4==1:
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_2.setPixel(vi, (wi,hi))
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            elif i%4==2:
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_1.setPixel(vi, (wi,hi))
                vi2 = vi+1
                self.im32_2.setPixel(vi2, (wi,hi))
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertEqual(x, wi)
                self.assertEqual(y, hi)
            else:
                self.im32_1.reset()
                self.im32_2.reset()
                self.im32_1.setPixel(vi, (wi,hi))
                self.im32_2.setPixel(vi, (wi,hi))
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertEqual(x, -1)
                self.assertEqual(y, -1)
        
        for i in range(100):
            wi1 = random.randint(0,w-1)
            hi1 = random.randint(0,h-1)
            vi = random.randint(1,500005)
            diri = random.choice(self.neighbors)
            self.im32_1.reset()
            self.im32_2.reset()
            self.im32_1.setPixel(vi, (wi1,hi1))
            wi2 = min(w-1, max(0, wi1+diri[0]))
            hi2 = min(h-1, max(0, hi1+diri[1]))
            if wi1!=wi2 or hi1!=hi2:
                self.im32_2.setPixel(vi, (wi2,hi2))
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)

