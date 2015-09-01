"""
Test cases for the image volume extraction function

The function works with all image depths.

The function returns an integer holding the volume of the image (sum of all the
pixels).

Python function:
    computeVolume
    
C function:
    MB_Volume
"""

from mamba import *
import unittest
import random

class TestVolume(unittest.TestCase):

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
        """Computes the volume of a binary image"""
        (w,h) = self.im1.getSize()
        exp_volume = 0
        for wi in range(w):
            for hi in range(h):
                vi = random.randint(0,1)
                self.im1.setPixel(vi, (wi,hi))
                exp_volume = exp_volume+vi
        obt_volume = computeVolume(self.im1)
        self.assertEqual(obt_volume, exp_volume)

    def testComputation_8(self):
        """Computes the volume of a 8-bit image"""
        (w,h) = self.im8.getSize()
        exp_volume = 0
        for wi in range(w):
            for hi in range(h):
                vi = random.randint(0,255)
                self.im8.setPixel(vi, (wi,hi))
                exp_volume = exp_volume+vi
        obt_volume = computeVolume(self.im8)
        self.assertEqual(obt_volume, exp_volume)

    def testComputation_32(self):
        """Computes the volume of a 32-bit image"""
        (w,h) = self.im32.getSize()
        exp_volume = 0
        for wi in range(w):
            for hi in range(h):
                vi = random.randint(0,0xffffffff)
                self.im32.setPixel(vi, (wi,hi))
                exp_volume = exp_volume+vi
        obt_volume = computeVolume(self.im32)
        self.assertEqual(obt_volume, exp_volume)

