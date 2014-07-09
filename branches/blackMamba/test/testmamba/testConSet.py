"""
Test cases for the image constant filling function.

The function fills the binary, 8-bit and 32-bit images with the given value.

Python function:
    imageMb.fill
    
C function:
    MB_ConSet
"""

from mamba import *
import unittest
import random

class TestConSet(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
        # for this test the image size is restricted
        self.im1 = imageMb(128,32,1)
        self.im8 = imageMb(128,32,8)
        self.im32 = imageMb(128,32,32)
        
    def tearDown(self):
        del(self.im1)
        del(self.im8)
        del(self.im32)

    def testSetting_1(self):
        """Verifies that binary images are correctly filled"""
        (w,h) = self.im1.getSize()
        
        self.im1.fill(1)
        for wi in range(w):
            for hi in range(h):
                v = self.im1.getPixel((wi,hi))
                self.assertEqual(v, 1)
        
        self.im1.fill(0)
        for wi in range(w):
            for hi in range(h):
                v = self.im1.getPixel((wi,hi))
                self.assertEqual(v, 0)

    def testSetting_8(self):
        """Verifies that 8-bit images are correctly filled"""
        (w,h) = self.im8.getSize()
        
        for i in range(100):
            vi = random.randint(0,255)
        
            self.im8.fill(vi)
            for wi in range(w):
                for hi in range(h):
                    v = self.im8.getPixel((wi,hi))
                    self.assertEqual(v, vi)

    def testSetting_32(self):
        """Verifies that 32-bit images are correctly filled"""
        (w,h) = self.im32.getSize()
        
        for i in range(100):
            vi = random.randint(1,0xffffffff)
        
            self.im32.fill(vi)
            for wi in range(w):
                for hi in range(h):
                    v = self.im32.getPixel((wi,hi))
                    self.assertEqual(v, vi)
        
        vi = 0xfedcba98
    
        self.im32.fill(vi)
        for wi in range(w):
            for hi in range(h):
                v = self.im32.getPixel((wi,hi))
                self.assertEqual(v, vi)

