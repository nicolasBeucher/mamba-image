"""
Test cases for the various functions found in the miscellaneous3D
module of mamba3D package.

Python functions:
    checkEmptiness3D
    compare3D
    shift3D
    drawEdge3D
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
        self.im8_4 = image3DMb(8)
        self.im8_5 = image3DMb(128, 128,128,8)
        self.im8_6 = image3DMb(64,64,64,8)
        self.im8_7 = image3DMb(64,64,64,8)
        self.im8_8 = image3DMb(64,64,64,8)
        self.im8_9 = image3DMb(64,64,64,8)
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
        del(self.im8_6)
        del(self.im8_7)
        del(self.im8_8)
        del(self.im8_9)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError,compare3D, self.im8_5, self.im8_2, self.im8_3)
        self.assertRaises(MambaError,shift3D, self.im8_5, self.im8_2, 1,1,1)
        
    def testCheckEmptiness3D(self):
        """Tests the emptiness verification on 3D images"""
        self.im8_1.reset()
        self.im8_1.setPixel(23, (128,128,0))
        empty = checkEmptiness3D(self.im8_1)
        self.assertTrue(not empty)
        self.im8_1.reset()
        self.im8_1.setPixel(198, (128,128,255))
        empty = checkEmptiness3D(self.im8_1)
        self.assertTrue(not empty)
        self.im8_1.reset()
        empty = checkEmptiness3D(self.im8_1)
        self.assertTrue(empty)
    
    def testCompare3D(self):
        """Verifies the comparison between 3D images"""
        self.im8_1.fill(128)
        self.im8_1.setPixel(198, (128,45,255))
        self.im8_2.fill(128)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertEqual(z, 255, "diff in (%d,%d,%d)"%(x,y,z))
        self.assertEqual(x, 128, "diff in (%d,%d,%d)"%(x,y,z))
        self.assertEqual(y, 45, "diff in (%d,%d,%d)"%(x,y,z))
        self.im8_1.fill(128)
        self.im8_1.setPixel(198, (255,45,0))
        self.im8_2.fill(128)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertEqual(z, 0, "diff in (%d,%d,%d)"%(x,y,z))
        self.assertEqual(x, 255, "diff in (%d,%d,%d)"%(x,y,z))
        self.assertEqual(y, 45, "diff in (%d,%d,%d)"%(x,y,z))
        self.im8_1.fill(128)
        self.im8_2.fill(128)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(z, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testShift3D(self):
        """Tests the shifting inside 3D images"""
        (w,h,l) = self.im8_6.getSize()
        self.im8_6.reset()
        self.im8_6.setPixel(200, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                dt = transposeDirection3D(d, grid3D)
                for amp in [1, 17, 29]:
                    linearDilate3D(self.im8_6, self.im8_7, dt, amp-1, grid3D)
                    linearDilate3D(self.im8_7, self.im8_8, dt, 1, grid3D)
                    diff3D(self.im8_8, self.im8_7, self.im8_8)
                    shift3D(self.im8_6, self.im8_7, d, amp, 0, grid3D)
                    (x,y,z) = compare3D(self.im8_7, self.im8_8, self.im8_9)
                    self.assertLess(z, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
        
    def _drawEdge(self, im, value):
        # draws the edge
        (w,h,l) = im.getSize()
        im[0].fill(value)
        im[l-1].fill(value)
        for i in range(1,l-1):
            drawBox(im[i], (0,0,w-1,h-1), value)
        
    def testDrawEdge3D(self):
        """Verifies the edge drawing operator"""
        self.im8_2.fill(0)
        self._drawEdge(self.im8_2, 255)
        drawEdge3D(self.im8_1)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))

