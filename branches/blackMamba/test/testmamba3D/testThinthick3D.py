"""
Test cases for the class and functions found in the thinthick3D module of
mamba3D package.

Python classes and functions:
    doubleStructuringElement3D
    HitOrMiss3D
    thin3D
    thick3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestThinthick3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(64,64,64,1)
        self.im1_2 = image3DMb(64,64,64,1)
        self.im1_3 = image3DMb(64,64,64,1)
        self.im1_4 = image3DMb(64,64,64,1)
        self.im1_5 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(64,64,32,8)
        self.im8_2 = image3DMb(64,64,32,8)
        self.im8_3 = image3DMb(64,64,32,8)
        self.im8_4 = image3DMb(64,64,32,8)
        self.im8_5 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(64,64,64,32)
        self.im32_2 = image3DMb(64,64,64,32)
        self.im32_3 = image3DMb(64,64,64,32)
        self.im32_4 = image3DMb(64,64,64,32)
        self.im32_5 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im1_5)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im8_5)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        del(self.im32_5)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        dse = doubleStructuringElement3D([5],[2],CUBIC)
        self.assertRaises(MambaError,hitOrMiss3D,self.im8_1,self.im1_2,dse)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        dse = doubleStructuringElement3D([5],[2],CUBIC)
        self.assertRaises(MambaError,hitOrMiss3D,self.im1_5,self.im1_2,dse)
        
    def testDoubleStructuringElement3D(self):
        """Checks the 3D double structuring element class"""
        se1 = structuringElement3D([5], CUBIC)
        se2 = structuringElement3D([2], CUBIC)
        se3 = structuringElement3D([10], FACE_CENTER_CUBIC)
        
        self.assertRaises(ValueError,doubleStructuringElement3D,1,2,3,4)
        self.assertRaises(ValueError,doubleStructuringElement3D,se1,se3)
        
        dse1 = doubleStructuringElement3D(se1,se2)
        dse2 = doubleStructuringElement3D([5],[2],CUBIC)
        dse3 = doubleStructuringElement3D([5],[2],CENTER_CUBIC)
        dse4 = dse2.flip()
        
        self.assertEqual(dse1.getStructuringElement3D(0), se1)
        self.assertEqual(dse2.getStructuringElement3D(0), se1)
        self.assertEqual(dse4.getStructuringElement3D(0), se2)
        self.assertEqual(dse1.getStructuringElement3D(1), se2)
        self.assertEqual(dse2.getStructuringElement3D(1), se2)
        self.assertEqual(dse4.getStructuringElement3D(1), se1)
        self.assertEqual(dse1.getGrid(), CUBIC)
        self.assertEqual(dse2.getGrid(), CUBIC)
        self.assertEqual(dse3.getGrid(), CENTER_CUBIC)
        self.assertEqual(dse4.getGrid(), CUBIC)
        
        self.assertEqual(repr(dse2), "doubleStructuringElement(structuringElement3D([5], mamba3D.CUBIC), structuringElement3D([2], mamba3D.CUBIC))")
        
    def testHitOrMiss3D(self):
        """Verifies the binary hit or miss 3D operator"""
        (w,h,l) = self.im1_1.getSize()
        
        dse1 = doubleStructuringElement3D([1,5,9], [0,10,14,18,19,23], CUBIC)
        dse2 = doubleStructuringElement3D([0,1,5,9], [10,14,18,19,23], CUBIC)
        self.im1_1.reset()
        self.im1_1.setPixel(1, (w//2,h//2,l//2))
        self.im1_1.setPixel(1, (w//2,h//2+1,l//2-1))
        self.im1_1.setPixel(1, (w//2,h//2-1,l//2-1))
        self.im1_1.setPixel(1, (w//2,h//2+1,l//2+1))
        self.im1_1.setPixel(1, (w//2,h//2  ,l//2+1))
        self.im1_1.setPixel(1, (w//2,h//2-1,l//2+1))
        
        self.im1_1.setPixel(1, (w//2,h//2,l-1))
        self.im1_1.setPixel(1, (w//2,h//2+1,l-2))
        self.im1_1.setPixel(1, (w//2,h//2-1,l-2))
        
        self.im1_3.reset()
        self.im1_2.reset()
        self.im1_3.setPixel(1, (w//2,h//2,l//2))
        hitOrMiss3D(self.im1_1, self.im1_2, dse1, EMPTY)
        (x,y,z) = compare3D(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0, "%d,%d,%d" % (x,y,z))
        
        self.im1_3.reset()
        self.im1_2.reset()
        hitOrMiss3D(self.im1_1, self.im1_2, dse2, EMPTY)
        (x,y,z) = compare3D(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0, "%d,%d,%d" % (x,y,z))
        
        self.im1_3.reset()
        self.im1_2.reset()
        self.im1_3.setPixel(1, (w//2,h//2,l//2))
        self.im1_3.setPixel(1, (w//2,h//2,l-1))
        hitOrMiss3D(self.im1_1, self.im1_2, dse1, FILLED)
        (x,y,z) = compare3D(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0, "%d,%d,%d" % (x,y,z))
        
    def testThin3D(self):
        """Tests the thinning 3D operator"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawCube(self.im1_1, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 1)
        self.im1_3.reset()
        drawCube(self.im1_3, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 1)
        self.im1_3.setPixel(0, (w//2,h//2-1,l//2))
        
        dse = doubleStructuringElement3D([1,2,8,10,11,17,19,20,26],[4,5,6,13,14,15,22,24], CUBIC)
        thin3D(self.im1_1, self.im1_2, dse)
        (x,y,z) = compare3D(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0, "%d,%d,%d" % (x,y,z))
        
    def testThick3D(self):
        """Verifies the thickening 3D operator"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawCube(self.im1_1, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 1)
        self.im1_3.reset()
        drawCube(self.im1_3, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 1)
        self.im1_3.setPixel(1, (w//2,h//2-2,l//2))
        
        dse = doubleStructuringElement3D([1,2,8,10,11,17,19,20,26],[4,5,6,13,14,15,22,24], CUBIC)
        thick3D(self.im1_1, self.im1_2, dse)
        (x,y,z) = compare3D(self.im1_2, self.im1_3, self.im1_2)
        self.assertLess(x, 0, "%d,%d,%d" % (x,y,z))

