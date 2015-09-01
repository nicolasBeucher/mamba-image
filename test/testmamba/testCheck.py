"""
Test cases for the image emptiness checking function.

The function returns True if the image is empty (all pixels set to 0). It works
with all depths.
    
Python function:
    checkEmptiness
    
C function:
    MB_Check
"""

from mamba import *
import unittest
import random

class TestCheck(unittest.TestCase):

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

    def testEmptyness_1(self):
        """Tests the correct emptiness checking for binary images"""
        (w,h) = self.im1_1.getSize()
        for i in range(1000):
            self.im1_1.reset()
            self.assertTrue(checkEmptiness(self.im1_1))
            wi = random.randint(0,w-1)
            hi = random.randint(0,h-1)
            self.im1_1.setPixel(1, (wi,hi))
            self.assertTrue(not checkEmptiness(self.im1_1))

    def testEmptyness_8(self):
        """Tests the correct emptiness checking for 8-bit images"""
        (w,h) = self.im8_1.getSize()
        for i in range(1000):
            self.im8_1.reset()
            self.assertTrue(checkEmptiness(self.im8_1))
            wi = random.randint(0,w-1)
            hi = random.randint(0,h-1)
            vi = random.randint(1,255)
            self.im8_1.setPixel(vi, (wi,hi))
            self.assertTrue(not checkEmptiness(self.im8_1))

    def testEmptyness_32(self):
        """Tests the correct emptiness checking for 32-bit images"""
        (w,h) = self.im32_1.getSize()
        for i in range(1000):
            self.im32_1.reset()
            self.assertTrue(checkEmptiness(self.im32_1))
            wi = random.randint(0,w-1)
            hi = random.randint(0,h-1)
            vi = random.randint(1,100000)
            self.im32_1.setPixel(vi, (wi,hi))
            self.assertTrue(not checkEmptiness(self.im32_1))

