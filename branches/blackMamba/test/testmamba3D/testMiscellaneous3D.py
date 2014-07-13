"""
Test cases for the various functions found in the miscellaneous3D
module of mamba3D package.

Python functions:
    copy3D
    copyBitPlane3D
    copyBytePlane3D
    getHistogram3D
    computeVolume3D
    computeRange3D
    computeMaxRange3D
    checkEmptiness3D
    compare3D
    shift3D
    drawEdge3D
    downscale3D
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
        self.im32_1 = image3DMb(32)
        self.im32_2 = image3DMb(32)
        self.im32_3 = image3DMb(32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError,copyBitPlane3D, self.im1_3, 0, self.im8_4)
        self.assertRaises(MambaError,copyBytePlane3D, self.im8_4, 0, self.im32_3)
        self.assertRaises(MambaError,compare3D, self.im8_4, self.im8_2, self.im8_3)
        self.assertRaises(MambaError,shift3D, self.im8_4, self.im8_2, 1,1,1)
        
    def _drawValueByPlane(self, im):
        l = im.getLength()
        im.reset()
        for i in range(l):
            im[i].fill(i)
        
    def testCopy3D(self):
        """Tests the copy of 3D images"""
        l = self.im8_1.getLength()
        self._drawValueByPlane(self.im8_1)
        self.im8_3.reset()
        self._drawValueByPlane(self.im8_2)
        copy3D(self.im8_1, self.im8_3)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        self.im8_3.reset()
        self.im8_2.reset()
        for i in range(l//2):
            self.im8_2[i].fill(i+l//2)
        copy3D(self.im8_1, self.im8_3, l//2, 0)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))

    def testCopyBitPlane3D(self):
        """Bit plane copy verification on 3D images"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im1_1.fill(1)
        self.im8_1.reset()
        self.im8_2.fill(0x4)
        copyBitPlane3D(self.im1_1, 2, self.im8_1)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testCopyBytePlane3D(self):
        """Byte plane copy verification on 3D images"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(0x25)
        self.im32_1.reset()
        self.im32_2.fill(0x250000)
        copyBytePlane3D(self.im8_1, 2, self.im32_1)
        (x,y,z) = compare3D(self.im32_1, self.im32_2, self.im32_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testGetHistogram3D(self):
        """Verifies the computation of the histogram on 3D images"""
        (w,h) = self.im8_1.getSize()
        self._drawValueByPlane(self.im8_1)
        histo = getHistogram3D(self.im8_1)
        for i in range(256):
            self.assertEqual(histo[i], w*h,"%d : %d!=%d" %(i,histo[i],w*h))
        
    def testComputeVolume3D(self):
        """Verifies the computation of the volume on 3D images"""
        (w,h) = self.im8_1.getSize()
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
        
    def testCheckEmptiness3D(self):
        """Tests the emptyness verification on 3D images"""
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
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(128)
        self.im8_1.setPixel(255, (w//2,h//2,l//2))
        self.im8_2.fill(128)
        self.im8_2[0].reset()
        self.im8_2.setPixel(255, (w//2,h//2,l//2+1))
        shift3D(self.im8_1, self.im8_3, d=18, amp=1, fill=0, grid=CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(z, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def _drawEdge(self, im, value):
        # draws the edge
        (w,h) = im.getSize()
        l = im.getLength()
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
        
    def testDownscale3D(self):
        """Verifies the downscale operator"""
        (w,h) = self.im32_1.getSize()
        l = self.im32_1.getLength()
        
        drawCube(self.im32_1, (0, 0, 0, w/3-1, h-1, l-1), 0)
        drawCube(self.im32_1, (w/3, 0, 0, 2*w/3-1, h-1, l-1), 0x80000000)
        drawCube(self.im32_1, (2*w/3, 0, 0, w-1, h-1, l-1), 0xffffffff)
        
        drawCube(self.im8_2, (0, 0, 0, w/3-1, h-1, l-1), 0)
        drawCube(self.im8_2, (w/3, 0, 0, 2*w/3-1, h-1, l-1), 0x7f)
        drawCube(self.im8_2, (2*w/3, 0, 0, w-1, h-1, l-1), 0xff)
        
        downscale3D(self.im32_1, self.im8_1)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0)

