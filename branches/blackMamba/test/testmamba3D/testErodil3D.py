"""
Test cases for the erosion and dilation functions found in the erodil3D
module of mamba3D package. Also performs verifications on the structuring
element class.

Python functions and classes:
    structuringElement3D
    erode3D
    dilate3D
    linearErode3D
    linearDilate3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestErodil3D(unittest.TestCase):

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
        self.assertRaises(MambaError, erode3D, self.im8_3, self.im8_4)
        self.assertRaises(MambaError, dilate3D, self.im8_3, self.im8_4)
        self.assertRaises(MambaError, linearErode3D, self.im8_3, self.im8_4, 1)
        self.assertRaises(MambaError, linearDilate3D, self.im8_3, self.im8_4, 1)
        
    def _drawMat(self, im, value, x, y, z):
        # draws a matrix centered in x,y,z
        for i in range(3):
            for j in range(3):
                for h in range(3):
                    im.setPixel(value, ((x-1)+i, (y-1)+j, (z-1)+h))
        
    def testErode3D(self):
        """Verifies the default erosion in 3D"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2,l//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, 0, w//2,h//2,l//2)
        erode3D(self.im8_1, self.im8_3, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testDilate3D(self):
        """Verifies the default dilation in 3D"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(0)
        self.im8_1.setPixel(255, (w//2,h//2,l//2))
        self.im8_2.fill(0)
        self._drawMat(self.im8_2, 255, w//2,h//2,l//2)
        dilate3D(self.im8_1, self.im8_3, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def _drawEdge(self, im, value):
        # draws the edge
        (w,h) = im.getSize()
        l = im.getLength()
        im[0].fill(value)
        im[l-1].fill(value)
        for i in range(1,l-1):
            drawBox(im[i], (0,0,w-1,h-1), value)
        
    def testEdgeErode3D(self):
        """Verifies the erosion correct behavior with edge"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        self._drawEdge(self.im8_2, 0)
        erode3D(self.im8_1, self.im8_3, se=CUBE3X3X3, edge=EMPTY)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testEdgeDilate3D(self):
        """Verifies the dilation correct behavior with edge"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(0)
        self.im8_2.fill(0)
        self._drawEdge(self.im8_2, 255)
        dilate3D(self.im8_1, self.im8_3, se=CUBE3X3X3, edge=FILLED)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testNoZeroErode3D(self):
        """Verifies the erosion correct behavior when direction 0 is missing"""
        se = structuringElement3D(range(1,27), CUBIC)
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2,l//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, 0, w//2,h//2,l//2)
        self.im8_2.setPixel(255, (w//2,h//2,l//2))
        erode3D(self.im8_1, self.im8_3, se=se)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testNoZeroDilate3D(self):
        """Verifies the dilation correct behavior when direction 0 is missing"""
        se = structuringElement3D(range(1,27), CUBIC)
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(0)
        self.im8_1.setPixel(255, (w//2,h//2,l//2))
        self.im8_2.fill(0)
        self._drawMat(self.im8_2, 255, w//2,h//2,l//2)
        self.im8_2.setPixel(0, (w//2,h//2,l//2))
        dilate3D(self.im8_1, self.im8_3, se=se)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testLinearErode3D(self):
        """Verifies the linear erosion"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2,l//2))
        self.im8_2.fill(255)
        self.im8_2.setPixel(0, (w//2,h//2,l//2))
        self.im8_2.setPixel(0, (w//2,h//2,l//2-1))
        self.im8_2.setPixel(0, (w//2,h//2,l//2-2))
        linearErode3D(self.im8_1, self.im8_3, 18, 2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testLinearDilate3D(self):
        """Verifies the linear dilation"""
        (w,h) = self.im8_1.getSize()
        l = self.im8_1.getLength()
        self.im8_1.fill(0)
        self.im8_1.setPixel(255, (w//2,h//2,l//2))
        self.im8_2.fill(0)
        self.im8_2.setPixel(255, (w//2,h//2,l//2))
        self.im8_2.setPixel(255, (w//2,h//2,l//2-1))
        self.im8_2.setPixel(255, (w//2,h//2,l//2-2))
        linearDilate3D(self.im8_1, self.im8_3, 18, 2, CUBIC)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testStructuringElement3D(self):
        """Tests the structuring Element 3D class"""
        testse = structuringElement3D([0,4,5,6,9,12] , FACE_CENTER_CUBIC)
        testse2 = structuringElement3D([4,5,6,9,12] , CENTER_CUBIC)
        testse3 = structuringElement3D([0,4,5,6,9,12] , FACE_CENTER_CUBIC)
        self.assertEqual(testse.getDirections(), [0,4,5,6,9,12])
        self.assertEqual(testse.getGrid(), FACE_CENTER_CUBIC)
        self.assertTrue(testse.hasZero())
        self.assertEqual(testse2.getDirections(), [4,5,6,9,12])
        self.assertEqual(testse2.getGrid(), CENTER_CUBIC)
        self.assertTrue(not testse2.hasZero())
        transse=testse.transpose()
        self.assertEqual(transse.getDirections(), [0,1,2,3,9,12])
        self.assertEqual(transse.getGrid(), FACE_CENTER_CUBIC)
        self.assertTrue(transse.hasZero())
        self.assertEqual(testse3, testse)
        self.assertNotEqual(testse3, testse2)
        s = repr(testse)
        self.assertEqual(s, "structuringElement3D([0, 4, 5, 6, 9, 12], mamba3D.FACE_CENTER_CUBIC)",s)

