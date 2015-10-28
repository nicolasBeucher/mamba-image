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
    erodeByCylinder3D
    dilateByCylinder3D
    computeDistance3D
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
        self.im1_4 = image3DMb(128,128,128,1)
        self.im8_1 = image3DMb(8)
        self.im8_2 = image3DMb(8)
        self.im8_3 = image3DMb(8)
        self.im8_4 = image3DMb(128,128,128,8)
        self.im32_1 = image3DMb(32)
        self.im32_2 = image3DMb(32)
        self.im32_3 = image3DMb(32)
        self.im32_4 = image3DMb(128,128,128,32)
        
    def tearDown(self):
        del(self.im1_1)
        del(self.im1_2)
        del(self.im1_3)
        del(self.im1_4)
        del(self.im8_1)
        del(self.im8_2)
        del(self.im8_3)
        del(self.im8_4)
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, computeDistance3D, self.im1_1, self.im1_2)
        self.assertRaises(MambaError, computeDistance3D, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, computeDistance3D, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, computeDistance3D, self.im8_1, self.im8_2)
        self.assertRaises(MambaError, computeDistance3D, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, computeDistance3D, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, computeDistance3D, self.im32_1, self.im8_2)
        self.assertRaises(MambaError, computeDistance3D, self.im32_1, self.im32_2)

    def testGridAcceptation(self):
        """Tests that incorrect grid raises an exception"""
        self.assertRaises(MambaError, computeDistance3D, self.im1_1, self.im32_2, grid=CENTER_CUBIC)
        
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError, erode3D, self.im8_3, self.im8_4)
        self.assertRaises(MambaError, dilate3D, self.im8_3, self.im8_4)
        self.assertRaises(MambaError, linearErode3D, self.im8_3, self.im8_4, 1)
        self.assertRaises(MambaError, linearDilate3D, self.im8_3, self.im8_4, 1)
        self.assertRaises(MambaError, computeDistance3D, self.im1_4, self.im32_2)
        self.assertRaises(MambaError, computeDistance3D, self.im1_1, self.im32_4)
        
    def _drawMat(self, im, value, x, y, z):
        # draws a matrix centered in x,y,z
        for i in range(3):
            for j in range(3):
                for h in range(3):
                    im.setPixel(value, ((x-1)+i, (y-1)+j, (z-1)+h))
        
    def testErode3D(self):
        """Verifies the default erosion in 3D"""
        (w,h,l) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2,l//2))
        self.im8_2.fill(255)
        self._drawMat(self.im8_2, 0, w//2,h//2,l//2)
        erode3D(self.im8_1, self.im8_3, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testDilate3D(self):
        """Verifies the default dilation in 3D"""
        (w,h,l) = self.im8_1.getSize()
        self.im8_1.fill(0)
        self.im8_1.setPixel(255, (w//2,h//2,l//2))
        self.im8_2.fill(0)
        self._drawMat(self.im8_2, 255, w//2,h//2,l//2)
        dilate3D(self.im8_1, self.im8_3, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def _drawEdge(self, im, value):
        # draws the edge
        (w,h,l) = im.getSize()
        im[0].fill(value)
        im[l-1].fill(value)
        for i in range(1,l-1):
            drawBox(im[i], (0,0,w-1,h-1), value)
        
    def testEdgeErode3D(self):
        """Verifies the erosion correct behavior with edge"""
        (w,h,l) = self.im8_1.getSize()
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        self._drawEdge(self.im8_2, 0)
        erode3D(self.im8_1, self.im8_3, se=CUBE3X3X3, edge=EMPTY)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testEdgeDilate3D(self):
        """Verifies the dilation correct behavior with edge"""
        (w,h,l) = self.im8_1.getSize()
        self.im8_1.fill(0)
        self.im8_2.fill(0)
        self._drawEdge(self.im8_2, 255)
        dilate3D(self.im8_1, self.im8_3, se=CUBE3X3X3, edge=FILLED)
        (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_1)
        self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testNoZeroErode3D(self):
        """Verifies the erosion correct behavior when direction 0 is missing"""
        se = structuringElement3D(range(1,27), CUBIC)
        (w,h,l) = self.im8_1.getSize()
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
        (w,h,l) = self.im8_1.getSize()
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
        (w,h,l) = self.im8_1.getSize()
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
        (w,h,l) = self.im8_1.getSize()
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
        
                    
    def testDilateByCylinder3D(self):
        """Verifies the dilation by a cylinder of a sequence"""
        seq = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        im2 = imageMb(128, 128)
        
        seq.reset()
        seq[2].setPixel(255, (64,64))
        dilateByCylinder3D(seq, 1, 0)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 0)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 255, "%d" %(vol))
        self.assertEqual(seq[1].getPixel((64,64)), 255)
        vol = computeVolume(seq[2])
        self.assertEqual(vol, 255)
        self.assertEqual(seq[2].getPixel((64,64)), 255)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 255)
        self.assertEqual(seq[3].getPixel((64,64)), 255)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 0)
        
        seq.reset()
        seq[2].setPixel(255, (64,64))
        im.reset()
        im.setPixel(255, (64,64))
        im.setPixel(255, (65,64))
        im.setPixel(255, (63,64))
        im.setPixel(255, (63,63))
        im.setPixel(255, (63,65))
        im.setPixel(255, (64,63))
        im.setPixel(255, (64,65))
        dilateByCylinder3D(seq, 0, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 0)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 0)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 0)
        
        seq.reset()
        seq[2].setPixel(255, (64,64))
        dilateByCylinder3D(seq, 1, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 0)
        (x,y) = compare(seq[1], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[3], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 0)
            
    def testErodeByCylinder3D(self):
        """Verifies the erosion by a cylinder of a sequence"""
        seq = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        im2 = imageMb(128, 128)
        
        seq.fill(255)
        seq[2].setPixel(0, (64,64))
        erodeByCylinder3D(seq, 1, 0)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 255*128*128)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 255*128*128-255, "%d" %(vol))
        self.assertEqual(seq[1].getPixel((64,64)), 0)
        vol = computeVolume(seq[2])
        self.assertEqual(vol, 255*128*128-255)
        self.assertEqual(seq[2].getPixel((64,64)), 0)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 255*128*128-255)
        self.assertEqual(seq[3].getPixel((64,64)), 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 255*128*128)
        
        seq.fill(255)
        seq[2].setPixel(0, (64,64))
        im.fill(255)
        im.setPixel(0, (64,64))
        im.setPixel(0, (65,64))
        im.setPixel(0, (63,64))
        im.setPixel(0, (63,63))
        im.setPixel(0, (63,65))
        im.setPixel(0, (64,63))
        im.setPixel(0, (64,65))
        erodeByCylinder3D(seq, 0, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 255*128*128)
        vol = computeVolume(seq[1])
        self.assertEqual(vol, 255*128*128)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[3])
        self.assertEqual(vol, 255*128*128)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 255*128*128)
        
        seq.fill(255)
        seq[2].setPixel(0, (64,64))
        erodeByCylinder3D(seq, 1, 1)
        vol = computeVolume(seq[0])
        self.assertEqual(vol, 255*128*128)
        (x,y) = compare(seq[1], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[2], im, im2)
        self.assertLess(x, 0)
        (x,y) = compare(seq[3], im, im2)
        self.assertLess(x, 0)
        vol = computeVolume(seq[4])
        self.assertEqual(vol, 255*128*128)
        
    def testComputeDistance3D(self):
        """Verifies the distance computation on a 3D binary set"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im32_3.reset()
        self.im1_1.setPixel(1, (w//2,h//2,l//2))
        self.im32_3.setPixel(1, (w//2,h//2,l//2))
        for i in range(4):
            dilate3D(self.im1_1, self.im1_1)
            add3D(self.im32_3, self.im1_1, self.im32_3)
            
        computeDistance3D(self.im1_1, self.im32_2)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
    def testComputeDistance3DEdge(self):
        """Verifies edge effect on the distance computation on a 3D binary set"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        drawCube(self.im1_1,(0,0,0,6,6,6), 1)
        
        self.im32_3.reset
        drawCube(self.im32_3,(0,0,0,6,6,6), 1)
        drawCube(self.im32_3,(1,1,1,5,5,5), 2)
        drawCube(self.im32_3,(2,2,2,4,4,4), 3)
        self.im32_3.setPixel(4, (3,3,3))
            
        computeDistance3D(self.im1_1, self.im32_2, CUBIC, mamba.EMPTY)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))
        
        self.im32_3.reset
        drawCube(self.im32_3,(0,0,0,6,6,6), 1)
        drawCube(self.im32_3,(0,0,0,5,5,5), 2)
        drawCube(self.im32_3,(0,0,0,4,4,4), 3)
        drawCube(self.im32_3,(0,0,0,3,3,3), 4)
        drawCube(self.im32_3,(0,0,0,2,2,2), 5)
        drawCube(self.im32_3,(0,0,0,1,1,1), 6)
        self.im32_3.setPixel(7, (0,0,0))
            
        computeDistance3D(self.im1_1, self.im32_2, CUBIC, mamba.FILLED)
        (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
        self.assertLess(x, 0, "%d,%d,%d" %(x,y,z))

