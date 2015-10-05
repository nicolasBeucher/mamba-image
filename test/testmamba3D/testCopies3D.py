"""
Test cases for the copy operators found in the copies3D module of mamba3D
package.

Python functions:
    copy3D
    copyBitPlane3D
    copyBytePlane3D
    cropCopy3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestConversion3D(unittest.TestCase):

    def setUp(self):
        self.im1_1 = image3DMb(64,64,64,1)
        self.im1_2 = image3DMb(64,64,64,1)
        self.im1_3 = image3DMb(64,64,64,1)
        self.im1_4 = image3DMb(64,64,64,1)
        self.im1_5 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(64,64,64,8)
        self.im8_2 = image3DMb(64,64,64,8)
        self.im8_3 = image3DMb(64,64,64,8)
        self.im8_4 = image3DMb(64,64,64,8)
        self.im8_5 = image3DMb(128,128,128,8)
        self.im8_6 = image3DMb(128,128,128,8)
        self.im8_7 = image3DMb(128,128,128,8)
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
        del(self.im8_6)
        del(self.im8_7)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        del(self.im32_5)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError,copyBitPlane3D, self.im1_3, 0, self.im8_5)
        self.assertRaises(MambaError,copyBytePlane3D, self.im8_5, 0, self.im32_3)
        self.assertRaises(MambaError,cropCopy3D, self.im8_1,(0,0,64), self.im8_5, (0,0,0),(64,64,64))
        
    def _drawValueByPlane(self, im):
        im.reset()
        for i,im2D in enumerate(im):
            im2D.fill(i)
        
    def testCopy3D(self):
        """Tests the copy of 3D images"""
        l = len(self.im8_1)
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
        (w,h,l) = self.im8_1.getSize()
        self.im1_1.fill(1)
        self.im8_1.reset()
        self.im8_2.fill(0x4)
        copyBitPlane3D(self.im1_1, 2, self.im8_1)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testCopyBytePlane3D(self):
        """Byte plane copy verification on 3D images"""
        (w,h,l) = self.im8_1.getSize()
        self.im8_1.fill(0x25)
        self.im32_1.reset()
        self.im32_2.fill(0x250000)
        copyBytePlane3D(self.im8_1, 2, self.im32_1)
        (x,y,z) = compare3D(self.im32_1, self.im32_2, self.im32_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testCropCopy3D(self):
        """Test the crop copy operator on 3D images"""
        (w,h, l) = self.im8_1.getSize()
        for i in range(10):
            vi = random.randint(0,255)
            self.im8_1.fill(vi)
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            z1 = random.randint(0,l-1)
            self.im8_5.reset()
            drawCube(self.im8_5,[xi,yi,z1,xi+w-1,yi+h-1,z1+l-1],vi)
            self.im8_6.reset()
            cropCopy3D(self.im8_1,(0,0,0), self.im8_6, (xi,yi,z1), (w,h,l))
            (x,y,z) = compare3D(self.im8_6, self.im8_5, self.im8_7)
            self.assertLess(x, 0)
            
            
