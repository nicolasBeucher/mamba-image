"""
Test cases for the image copy function.

The function works on all images depths.
The input image is copied into the output image. Thus the images must have the
same depth.

When working with line copy, the line is extracted in the input image at the 
given position and put into the output image at another given position.

Here is the list of legal operations :
     1 -> 1
     8 -> 8
    32 ->32
     1[line] -> 1[line]
     8[line] -> 8[line]
    32[line] ->32[line]
    
Python functions:
    copy
    copyLine
    cropCopy
    
C functions:
    MB_Copy
    MB_CopyLine
    MB_CropCopy
"""

from mamba import *
import unittest
import random

class TestCopy(unittest.TestCase):

    def setUp(self):
        # Creating two images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im1s2_1 = imageMb(128,128,1)
        self.im1s2_2 = imageMb(128,128,1)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        self.im32s2_1 = imageMb(128,128,32)
        self.im32s2_2 = imageMb(128,128,32)
        
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
        del(self.im1s2_1)
        del(self.im1s2_2)
        del(self.im8s2_1)
        del(self.im8s2_2)
        del(self.im32s2_1)
        del(self.im32s2_2)

    def testDepthAcceptationCopy(self):
        """Tests that incorrect depth raises an exception on copy function"""
        #self.assertRaises(MambaError, copy, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, copy, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, copy, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, copy, self.im8_1, self.im1_2)
        #self.assertRaises(MambaError, copy, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, copy, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, copy, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, copy, self.im32_1, self.im8_2)
        #self.assertRaises(MambaError, copy, self.im32_1, self.im32_2)

    def testDepthAcceptationCopyLine(self):
        """Tests that incorrect depth raises an exception on copyline function"""
        #self.assertRaises(MambaError, copyLine, self.im1_1, 0, self.im1_2, 0)
        self.assertRaises(MambaError, copyLine, self.im1_1, 0, self.im8_2, 0)
        self.assertRaises(MambaError, copyLine, self.im1_1, 0, self.im32_2, 0)
        self.assertRaises(MambaError, copyLine, self.im8_1, 0, self.im1_2, 0)
        #self.assertRaises(MambaError, copyLine, self.im8_1, 0, self.im8_2, 0)
        self.assertRaises(MambaError, copyLine, self.im8_1, 0, self.im32_2, 0)
        self.assertRaises(MambaError, copyLine, self.im32_1, 0, self.im1_2, 0)
        self.assertRaises(MambaError, copyLine, self.im32_1, 0, self.im8_2, 0)
        #self.assertRaises(MambaError, copyLine, self.im32_1, 0, self.im32_2, 0)

    def testDepthAcceptationCropCopy(self):
        """Tests that incorrect depth raises an exception on cropCopy function"""
        self.assertRaises(MambaError, cropCopy, self.im1_1, (0,0), self.im1_2, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im1_1, (0,0), self.im8_2, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im1_1, (0,0), self.im32_2, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im8_1, (0,0), self.im1_2, (0,0), (10,10))
        #self.assertRaises(MambaError, cropCopy, self.im8_1, (0,0), self.im8_2, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im8_1, (0,0), self.im32_2, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im32_1, (0,0), self.im1_2, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im32_1, (0,0), self.im8_2, (0,0), (10,10))
        #self.assertRaises(MambaError, cropCopy, self.im32_1, (0,0), self.im32_2, (0,0), (10,10))

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, copy, self.im8s2_1, self.im8_1)
        self.assertRaises(MambaError, copy, self.im8_1, self.im8s2_1)
        self.assertRaises(MambaError, copyLine, self.im8s2_1, 0, self.im8_1, 0)
        self.assertRaises(MambaError, copyLine, self.im8_1, 0, self.im8s2_1, 0)

    def testParameterRangeCopyLine(self):
        """Tests that out of range parameter raises an exception in copyline"""
        (w,h) = self.im1_1.getSize()
        
        for i in range(h,h+10):
            self.assertRaises(MambaError, copyLine, self.im1_1, i, self.im1_2, 0)
            self.assertRaises(MambaError, copyLine, self.im8_1, i, self.im8_2, 0)
            self.assertRaises(MambaError, copyLine, self.im32_1, i, self.im32_2, 0)
            self.assertRaises(MambaError, copyLine, self.im1_1, 0, self.im1_2, i)
            self.assertRaises(MambaError, copyLine, self.im8_1, 0, self.im8_2, i)
            self.assertRaises(MambaError, copyLine, self.im32_1, 0, self.im32_2, i)

    def testParameterRangeCropCopy(self):
        """Tests that out of range parameter raises an exception in cropCopy"""
        (w_dest,h_dest) = self.im8_1.getSize()
        (w_src,h_src) = self.im8s2_1.getSize()
        
        self.assertRaises(MambaError, cropCopy, self.im8s2_1, (w_src,0), self.im8_1, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im8s2_1, (0,h_src), self.im8_1, (0,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im8s2_1, (0,0), self.im8_1, (w_dest,0), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im8s2_1, (0,0), self.im8_1, (0,h_dest), (10,10))
        self.assertRaises(MambaError, cropCopy, self.im8s2_1, (0,0), self.im8_1, (0,0), (0,10))
        self.assertRaises(MambaError, cropCopy, self.im8s2_1, (0,0), self.im8_1, (0,0), (10,0))
            
    def testCopy_1(self):
        """Verifies that image copy works with binary image"""
        self.im1_2.reset()
        self.im1_1.fill(1)
        self.im1_3.fill(1)
        copy(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
        self.assertLess(x, 0)
        self.im1_2.fill(1)
        self.im1_1.reset()
        self.im1_3.reset()
        copy(self.im1_1, self.im1_2)
        (x,y) = compare(self.im1_2, self.im1_3, self.im1_1)
        self.assertLess(x, 0)

    def testCopy_8(self):
        """Verifies that image copy works with 8-bit image"""
        for i in range(100):
            self.im8_2.reset()
            vi = random.randint(1,255)
            self.im8_1.fill(vi)
            self.im8_3.fill(vi)
            copy(self.im8_1, self.im8_2)
            (x,y) = compare(self.im8_2, self.im8_3, self.im8_1)
            self.assertLess(x, 0)

    def testCopy_32(self):
        """Verifies that image copy works with 32-bit image"""
        for i in range(100):
            self.im32_2.reset()
            vi = random.randint(1,0x7fffffff)
            self.im32_1.fill(vi)
            self.im32_3.fill(vi)
            copy(self.im32_1, self.im32_2)
            (x,y) = compare(self.im32_2, self.im32_3, self.im32_1)
            self.assertLess(x, 0)
        
    def testCopyLine_1(self):
        """Verifies that image copy line by line works with binary image"""
        (w,h) = self.im1_1.getSize()
        self.im1_2.reset()
        self.im1_1.fill(1)
        for i in range(h):
            copyLine(self.im1_1, i, self.im1_2, i)
            vol = computeVolume(self.im1_2)
            self.assertEqual(vol, ((i+1)*w))
        
    def testCopyLine_8(self):
        """Verifies that image copy line by line works with 8-bit image"""
        (w,h) = self.im8_1.getSize()
        for i in range(100):
            self.im8_2.reset()
            vi = random.randint(1,255)
            self.im8_1.fill(vi)
            for i in range(h):
                copyLine(self.im8_1, i, self.im8_2, i)
                vol = computeVolume(self.im8_2)
                self.assertEqual(vol, ((i+1)*w*vi))
        
    def testCopyLine_32(self):
        """Verifies that image copy line by line works with 32-bit image"""
        (w,h) = self.im32_1.getSize()
        for i in range(100):
            self.im32_2.reset()
            vi = random.randint(1,500)
            self.im32_1.fill(vi)
            for i in range(h):
                copyLine(self.im32_1, i, self.im32_2, i)
                vol = computeVolume(self.im32_2)
                self.assertEqual(vol, ((i+1)*w*vi), "%d : %d/%d" %(i,vol,(i+1)*w*vi))
            
    def testCropCopy_8(self):
        """Verifies that image crop copy works with 8-bit image"""
        (w,h) = self.im8s2_1.getSize()
        for i in range(100):
            vi = random.randint(0,255)
            self.im8s2_1.fill(vi)
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            self.im8_2.reset()
            drawSquare(self.im8_2,[xi,yi,xi+w-1,yi+h-1],vi)
            self.im8_1.reset()
            cropCopy(self.im8s2_1, (0,0), self.im8_1, (xi,yi), (w,h))
            (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
            self.assertLess(x, 0)
            
    def testCropCopy_32(self):
        """Verifies that image crop copy works with 32-bit image"""
        (w,h) = self.im32s2_1.getSize()
        for i in range(100):
            vi = random.randint(0,0xffffffff)
            self.im32s2_1.fill(vi)
            xi = random.randint(0,w-1)
            yi = random.randint(0,h-1)
            self.im32_2.reset()
            drawSquare(self.im32_2,[xi,yi,xi+w-1,yi+h-1],vi)
            self.im32_1.reset()
            cropCopy(self.im32s2_1, (0,0), self.im32_1, (xi,yi), (w,h))
            (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
            self.assertLess(x, 0)

