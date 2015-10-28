"""
Test cases for the measure operators found in the measure3D
module of mamba3D package.

Python functions:
    computeVolume3D
    computeRange3D
    computeMaxRange3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestMiscellaneous3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(1)
        self.im1_2 = image3DMb(1)
        self.im1_3 = image3DMb(1)
        self.im8_1 = image3DMb(8)
        self.im8_2 = image3DMb(8)
        self.im8_3 = image3DMb(8)
        self.im8_4 = image3DMb(128,128,128,8)
        self.im8_5 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(32)
        self.im32_2 = image3DMb(32)
        self.im32_3 = image3DMb(32)
        self.im32_4 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        
    def _drawValueByPlane(self, im):
        im.reset()
        for i,im2D in enumerate(im):
            im2D.fill(i)
        
    def testComputeVolume3D(self):
        """Verifies the computation of the volume on 3D images"""
        (w,h,l) = self.im8_1.getSize()
        self._drawValueByPlane(self.im8_1)
        vol = computeVolume3D(self.im8_1)
        exp_vol = 0
        for i in range(256):
            exp_vol += i*w*h
        self.assertEqual(vol, exp_vol)
        
    def testComputeRange3D(self):
        """Verifies the computation of the range on 3D images"""
        self.im8_1.fill(128)
        self.im8_1.setPixel(23, (128,128,0))
        self.im8_1.setPixel(198, (128,128,255))
        (mi,ma) = computeRange3D(self.im8_1)
        self.assertEqual(mi, 23)
        self.assertEqual(ma, 198)
        
    def testComputeMaxRange3D(self):
        """Verifies the computation of the maximum range on 3D images"""
        (mi,ma) = computeMaxRange3D(self.im1_1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 1)
        (mi,ma) = computeMaxRange3D(self.im8_1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 255)
        (mi,ma) = computeMaxRange3D(self.im32_1)
        self.assertEqual(mi, 0)
        self.assertEqual(ma, 0xffffffff)
        
