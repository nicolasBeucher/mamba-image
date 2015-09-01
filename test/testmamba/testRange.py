"""
Test cases for the image pixel range functions.

The functions return the actual pixel value range (minimum value to maximum) or
the allowed range given the image depth.

The functions works with all depths.

Python functions:
    computeRange
    computeMaxRange
    
C functions:
    MB_Range
    MB_depthRange
"""

from mamba import *
import unittest
import random

class TestRange(unittest.TestCase):

    def setUp(self):
        # Creating images 
        self.im1 = imageMb(1)
        self.im8 = imageMb(8)
        self.im32 = imageMb(32)
        
    def tearDown(self):
        del(self.im1)
        del(self.im8)
        del(self.im32)

    def testComputation_1(self):
        """Computes the actual pixel range of a binary image"""
        (w,h) = self.im1.getSize()
        self.im1.reset()
        mi, ma = computeRange(self.im1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 0)
        self.im1.fill(1)
        mi, ma = computeRange(self.im1)
        self.assertEqual(mi, 1)
        self.assertEqual(ma, 1)
        self.im1.setPixel(0, (0,0))
        mi, ma = computeRange(self.im1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 1)
        self.im1.reset()
        self.im1.setPixel(1, (w-1,h-1))
        mi, ma = computeRange(self.im1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 1)
        
    def testMaxRange_1(self):
        """Verifies the correctness of allowed range for binary images"""
        mi, ma = computeMaxRange(self.im1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 1)

    def testComputation_8(self):
        """Computes the actual pixel range of a 8-bit image"""
        (w,h) = self.im8.getSize()
        for i in range(100):
            vrange = random.randint(0,255)
            self.im8.fill(vrange)
            exp_ma = vrange
            for hi in range(h):
                vi = random.randint(vrange,255)
                self.im8.setPixel(vi, (0,hi))
                exp_ma = max(exp_ma, vi)
            mi, ma = computeRange(self.im8)
            self.assertEqual(mi, vrange)
            self.assertEqual(ma, exp_ma)
            vrange = random.randint(0,255)
            self.im8.fill(vrange)
            exp_mi = vrange
            for wi in range(w):
                vi = random.randint(0,vrange)
                self.im8.setPixel(vi, (wi,0))
                exp_mi = min(exp_mi, vi)
            mi, ma = computeRange(self.im8)
            self.assertEqual(ma, vrange)
            self.assertEqual(mi, exp_mi)
        
    def testMaxRange_8(self):
        """Verifies the correctness of allowed range for 8-bit images"""
        mi, ma = computeMaxRange(self.im8)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 255)

    def testComputation_32(self):
        """Computes the actual pixel range of a 32-bit image"""
        (w,h) = self.im32.getSize()
        for i in range(100):
            vrange = random.randint(0,0xffffffff)
            self.im32.fill(vrange)
            mi, ma = computeRange(self.im32)
            self.assertEqual(mi, vrange, "mi=%d, vrange=%d" % (mi, vrange))
            self.assertEqual(ma, vrange, "ma=%d, vrange=%d" % (ma, vrange))
            exp_ma = vrange
            for hi in range(h):
                vi = random.randint(vrange,0xffffffff)
                self.im32.setPixel(vi, (0,hi))
                exp_ma = max(exp_ma, vi)
            mi, ma = computeRange(self.im32)
            self.assertEqual(mi, vrange)
            self.assertEqual(ma, exp_ma)
            vrange = random.randint(0,0xffffffff)
            self.im32.fill(vrange)
            exp_mi = vrange
            for wi in range(w):
                vi = random.randint(0,vrange)
                self.im32.setPixel(vi, (wi,0))
                exp_mi = min(exp_mi, vi)
            mi, ma = computeRange(self.im32)
            self.assertEqual(ma, vrange)
            self.assertEqual(mi, exp_mi)
        
    def testMaxRange_32(self):
        """Verifies the correctness of allowed range for 32-bit images"""
        mi, ma = computeMaxRange(self.im32)
        self.assertEqual(mi, 0, "allowed min is %d" % (mi))
        self.assertEqual(ma, 0xffffffff, "allowed max is %x" % (ma))

