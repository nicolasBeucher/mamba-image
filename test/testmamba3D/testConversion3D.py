"""
Test cases for the depth conversion family of operators found in the
conversion3D module of mamba3D package.

Python functions:
    convert3D
    convertByMask3D
    threshold3D
    generateSupMask3D
    lookup3D
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
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError,convert3D,self.im8_5,self.im1_2)
        self.assertRaises(MambaError,convertByMask3D,self.im1_5,self.im8_2,0,255)
        self.assertRaises(MambaError,threshold3D,self.im8_5,self.im1_2,0,255)
        self.assertRaises(MambaError,generateSupMask3D,self.im8_5,self.im8_2,self.im1_3,False)
        self.assertRaises(MambaError,generateSupMask3D,self.im8_1,self.im8_5,self.im1_3,False)
        self.assertRaises(MambaError,generateSupMask3D,self.im8_1,self.im8_2,self.im1_5,False)
        self.assertRaises(MambaError,lookup3D,self.im8_1,self.im1_5,256*[0])
        
    def testConvert3D_8_1(self):
        """Tests the 3D image greyscale/binary conversion function"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1[l-1].fill(255)
        self.im8_1[l-2].fill(155)
        
        self.im1_2.reset()
        self.im1_2[l-1].fill(1)
        self.im8_2.reset()
        self.im8_2[l-1].fill(255)
        
        convert3D(self.im8_1, self.im1_1)
        (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
        convert3D(self.im1_1, self.im8_1)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testConvert3D_32_1(self):
        """Tests the 3D image 32-bit/binary conversion function"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im32_1.reset()
        self.im32_1[l-1].fill(0xffffffff)
        self.im32_1[l-2].fill(0x8f8f8f8f)
        
        self.im1_2.reset()
        self.im1_2[l-1].fill(1)
        self.im32_2.reset()
        self.im32_2[l-1].fill(0xffffffff)
        
        convert3D(self.im32_1, self.im1_1)
        (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
        convert3D(self.im1_1, self.im32_1)
        (x,y,z) = compare3D(self.im32_1, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testConvert3D_32_8(self):
        """Tests the 3D image 32-bit downscaling conversion function"""
        (w,h,l) = self.im32_1.getSize()
        
        self.im32_1.reset()
        self.im32_1[l-1].fill(0xffffffff)
        self.im32_1[l-2].fill(0x80000000)
        self.im8_2.reset()
        self.im8_2[l-1].fill(255)
        self.im8_2[l-2].fill(127)
        
        convert3D(self.im32_1, self.im8_1)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testConvertByMask3D(self):
        """Tests the 3D image binary 2 greyscale mask conversion function"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_2.fill(27)
        self.im8_2[l-1].fill(155)
        self.im1_1.reset()
        self.im1_1[l-1].fill(1)
        
        convertByMask3D(self.im1_1, self.im8_1, 27, 155)
        (x,y,z) = compare3D(self.im8_1, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testThreshold3D(self):
        """Tests the 3D image threshold function"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(l):
            self.im8_1[i].fill(i)
        
        self.im1_2.fill(1)
        for i in range(l):
        
            threshold3D(self.im8_1, self.im1_1, i, 255)
            (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : diff in (%d,%d,%d)"%(i,x,y,z))
            
            self.im1_2[i].fill(0)
            
    def testGenerateSupMask3D(self):
        """Verifies the superior mask generation on 3D images"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(l):
            self.im8_1[i].fill(i)
            
        self.im8_2.fill(l//2)
        
        self.im1_2.reset()
        drawCube(self.im1_2, (0,0,l//2,w-1,h-1,l-1), 1)
        generateSupMask3D(self.im8_1, self.im8_2, self.im1_1, False)
        (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
        self.im1_2.reset()
        drawCube(self.im1_2, (0,0,l//2+1,w-1,h-1,l-1), 1)
        generateSupMask3D(self.im8_1, self.im8_2, self.im1_1, True)
        (x,y,z) = compare3D(self.im1_1, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testLookup3D(self):
        """Tests the look-up table conversion on 3D images"""
        (w,h,l) = self.im8_1.getSize()
        
        for i in range(l):
            self.im8_1[i].fill(i)
            
        self.im8_3.reset()
        lookup3D(self.im8_1, self.im8_2, 256*[0])
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
            
        self.im8_3.reset()
        for i in range(l):
            self.im8_3[i].fill(255-i)
        lookup3D(self.im8_1, self.im8_2, list(range(255,-1,-1)))
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))

