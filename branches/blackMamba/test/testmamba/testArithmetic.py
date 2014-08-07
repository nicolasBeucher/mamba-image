"""
Test cases for the functions implementing arithmetic operators found in the 
arithmetic module of mamba package.

Python function:
    ceilingAddConst
    ceilingAdd
    floorSubConst
    floorSub
    mulRealConst
"""

from mamba import *
import unittest
import random

class TestArithmetic(unittest.TestCase):

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
        
    def testCeilingAdd(self):
        """Verifies the saturated (ceiling) addition for 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.fill(0xffffff80)
        for i in range(256):
            self.im32_3.fill(i)
            ceilingAdd(self.im32_1, self.im32_3, self.im32_2)
            vol = computeVolume(self.im32_2)//(w*h)
            value = min(0xffffff80+i, 0xffffffff)
            self.assertEqual(vol, value)
        
    def testCeilingAddConst(self):
        """Verifies the saturated (ceiling) constant addition for 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.fill(0xffffff80)
        for i in range(256):
            ceilingAddConst(self.im32_1, i, self.im32_2)
            vol = computeVolume(self.im32_2)//(w*h)
            value = min(0xffffff80+i, 0xffffffff)
            self.assertEqual(vol, value)
        
    def testFloorSub(self):
        """Verifies the saturated (floor) subtraction for 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.fill(0x80)
        for i in range(256):
            self.im32_3.fill(i)
            floorSub(self.im32_1, self.im32_3, self.im32_2)
            vol = computeVolume(self.im32_2)//(w*h)
            value = max(0x80-i, 0)
            self.assertEqual(vol, value, "%d: %d %d" % (i,vol, value))
        
    def testFloorSubConst(self):
        """Verifies the saturated (floor) constant subtraction for 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        self.im32_1.fill(0x80)
        for i in range(256):
            floorSubConst(self.im32_1, i, self.im32_2)
            vol = computeVolume(self.im32_2)//(w*h)
            value = max(0x80-i, 0)
            self.assertEqual(vol, value)
        
    def testMulRealConstDepthAcceptance(self):
        """Verifies that mulRealConst refuses binary input images"""
        self.assertRaises(MambaError, mulRealConst, self.im1_1, 1.0, self.im8_2)
        self.assertRaises(MambaError, mulRealConst, self.im32_1, 1.0, self.im1_2)
        
    def testMulRealConst(self):
        """Tests the real value multiplication"""
        self.im8_1.fill(1)
        
        self.im8_3.fill(1)
        mulRealConst(self.im8_1, 1.6, self.im8_2, nearest=False)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im8_3.fill(2)
        mulRealConst(self.im8_1, 1.6, self.im8_2, nearest=True)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im8_1.fill(10)
        self.im8_3.fill(15)
        mulRealConst(self.im8_1, 1.5, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        
        self.im32_1.fill(1000)
        self.im32_3.fill(1500)
        mulRealConst(self.im32_1, 1.5, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)
        
        self.im8_1.fill(200)
        self.im8_3.fill(255)
        self.im32_3.fill(260)
        mulRealConst(self.im8_1, 1.3, self.im8_2)
        (x,y) = compare(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0)
        mulRealConst(self.im8_1, 1.3, self.im32_2)
        (x,y) = compare(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0)
