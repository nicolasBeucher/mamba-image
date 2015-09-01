"""
Test cases for the open and close family of operators found in the
openclose3D module of mamba3D package.

Python functions:
    opening3D
    closing3D
    buildOpen3D
    buildClose3D
    linearOpen3D
    linearClose3D
    supOpen3D
    infClose3D
    openByCylinder3D
    closeByCylinder3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestOpenclose3D(unittest.TestCase):

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
        
    def testGridAcceptation(self):
        """Tests that incorrect grid raises an exception"""
        self.assertRaises(MambaError, supOpen3D, self.im8_1, self.im8_2, 1, grid=CENTER_CUBIC)
        self.assertRaises(MambaError, infClose3D, self.im8_1, self.im8_2, 1, grid=CENTER_CUBIC)
        
    def testOpening3D(self):
        """Verifies the correct behavior of the 3D open operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_1.setPixel(255, (w//2,h//2,l//2))
        dilate3D(self.im8_1, self.im8_1, 5)
        
        for i in range(3,8):
            self.im8_3.reset()
            if i<=5:
                self.im8_3.setPixel(255, (w//2,h//2,l//2))
                dilate3D(self.im8_3, self.im8_3, 5)
            
            opening3D(self.im8_1, self.im8_2, i)
            (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
            self.assertLess(x, 0, "%d" %(i))
        
    def testClose3D(self):
        """Verifies the correct behavior of the 3D close operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.fill(255)
        self.im8_1.setPixel(0, (w//2,h//2,l//2))
        erode3D(self.im8_1, self.im8_1, 5)
        
        for i in range(3,8):
            self.im8_3.fill(255)
            if i<=5:
                self.im8_3.setPixel(0, (w//2,h//2,l//2))
                erode3D(self.im8_3, self.im8_3, 5)
            
            closing3D(self.im8_1, self.im8_2, i)
            (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
            self.assertLess(x, 0, "%d" %(i))
            
        
        self.im8_1.reset()
        drawCube(self.im8_1, (1,1,1,w-2,h-2,l-2), 255)
        drawCube(self.im8_1, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 0)
        
        self.im8_3.reset()
        drawCube(self.im8_3, (1,1,1,w-2,h-2,l-2), 255)
            
        closing3D(self.im8_1, self.im8_2, 3, se=CUBE3X3X3, edge=EMPTY)
        (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
        self.assertLess(x, 0, "%d" %(i))
        
    def testBuildOpen3D(self):
        """Verifies the open by reconstruction 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_4.reset()
        self.im8_4.setPixel(128, (w//2,h//2,l//2-10))
        dilate3D(self.im8_4, self.im8_4, 7)
        logic3D(self.im8_1, self.im8_4, self.im8_1, "sup")
        self.im8_4.reset()
        self.im8_4.setPixel(255, (w//2,h//2,l//2+10))
        dilate3D(self.im8_4, self.im8_4, 4)
        logic3D(self.im8_1, self.im8_4, self.im8_1, "sup")
        drawLine3D(self.im8_1, (w//2,h//2,l//2-10,w//2,h//2,l//2+10), 128)
        
        self.im8_3.reset()
        self.im8_4.reset()
        self.im8_4.setPixel(128, (w//2,h//2,l//2-10))
        dilate3D(self.im8_4, self.im8_4, 7)
        logic3D(self.im8_3, self.im8_4, self.im8_3, "sup")
        self.im8_4.reset()
        self.im8_4.setPixel(128, (w//2,h//2,l//2+10))
        dilate3D(self.im8_4, self.im8_4, 4)
        logic3D(self.im8_3, self.im8_4, self.im8_3, "sup")
        drawLine3D(self.im8_3, (w//2,h//2,l//2-10,w//2,h//2,l//2+10), 128)
        
        self.im8_4.reset()
        
        for i in range(5,10):
            buildOpen3D(self.im8_1, self.im8_2, i)
            if i<=7:
                (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
            else:
                (x,y,z) = compare3D(self.im8_2, self.im8_4, self.im8_2)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testBuildClose3D(self):
        """Verifies the close by reconstruction 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.fill(255)
        self.im8_4.fill(255)
        self.im8_4.setPixel(128, (w//2,h//2,l//2-10))
        erode3D(self.im8_4, self.im8_4, 7)
        logic3D(self.im8_1, self.im8_4, self.im8_1, "inf")
        self.im8_4.fill(255)
        self.im8_4.setPixel(0, (w//2,h//2,l//2+10))
        erode3D(self.im8_4, self.im8_4, 4)
        logic3D(self.im8_1, self.im8_4, self.im8_1, "inf")
        drawLine3D(self.im8_1, (w//2,h//2,l//2-10,w//2,h//2,l//2+10), 128)
        
        self.im8_3.fill(255)
        self.im8_4.fill(255)
        self.im8_4.setPixel(128, (w//2,h//2,l//2-10))
        erode3D(self.im8_4, self.im8_4, 7)
        logic3D(self.im8_3, self.im8_4, self.im8_3, "inf")
        self.im8_4.fill(255)
        self.im8_4.setPixel(128, (w//2,h//2,l//2+10))
        erode3D(self.im8_4, self.im8_4, 4)
        logic3D(self.im8_3, self.im8_4, self.im8_3, "inf")
        drawLine3D(self.im8_3, (w//2,h//2,l//2-10,w//2,h//2,l//2+10), 128)
        
        self.im8_4.fill(255)
        
        for i in range(5,10):
            buildClose3D(self.im8_1, self.im8_2, i)
            if i<=7:
                (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
            else:
                (x,y,z) = compare3D(self.im8_2, self.im8_4, self.im8_2)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
        
    def testLinearOpen3D(self):
        """Verifies the correct behavior of the directional open 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        for d in getDirections3D():
            self.im8_1.reset()
            self.im8_1.setPixel(255, (w//2,h//2,l//2))
            linearDilate3D(self.im8_1, self.im8_1, d, 5)
            
            for i in range(4,7):
                self.im8_3.reset()
                if i<=5 or d==0:
                    self.im8_3.setPixel(255, (w//2,h//2,l//2))
                    linearDilate3D(self.im8_3, self.im8_3, d, 5)
                
                linearOpen3D(self.im8_1, self.im8_2, d, i)
                (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
                self.assertLess(x, 0, "%d-%d" %(d,i))
        
    def testLinearClose3D(self):
        """Verifies the correct behavior of the directional close 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        for d in getDirections3D():
            self.im8_1.fill(255)
            self.im8_1.setPixel(0, (w//2,h//2,l//2))
            linearErode3D(self.im8_1, self.im8_1, d, 5)
            
            for i in range(4,7):
                self.im8_3.fill(255)
                if i<=5 or d==0:
                    self.im8_3.setPixel(0, (w//2,h//2,l//2))
                    linearErode3D(self.im8_3, self.im8_3, d, 5)
                
                linearClose3D(self.im8_1, self.im8_2, d, i)
                (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
                self.assertLess(x, 0, "%d-%d" %(d,i))
            
        self.im8_1.reset()
        drawCube(self.im8_1, (1,1,1,w-2,h-2,l-2), 255)
        drawCube(self.im8_1, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 0)
        self.im8_3.reset()
        drawCube(self.im8_3, (1,1,1,w-2,h-2,l-2), 255)
        for d in getDirections3D(CUBIC):
            if d==0:
                drawCube(self.im8_3, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 0)
            linearClose3D(self.im8_1, self.im8_2, d, 3, grid=CUBIC, edge=EMPTY)
            (x,y,z) = compare3D(self.im8_2, self.im8_3, self.im8_2)
            self.assertLess(x, 0, "%d-%d" %(d,i))
            if d==0:
                drawCube(self.im8_3, (w//2-1,h//2-1,l//2-1,w//2+1,h//2+1,l//2+1), 255)
                
    def testSupOpen3D(self):
        """Tests the superior open 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        dirs = getDirections3D(FACE_CENTER_CUBIC)[1:]
        do = random.choice(dirs)
        for d in dirs:
            self.im8_4.reset()
            self.im8_4.setPixel(255, (w//2,h//2,l//2))
            linearDilate3D(self.im8_4, self.im8_4, d, d==do and 3 or 2, FACE_CENTER_CUBIC)
            logic3D(self.im8_1, self.im8_4, self.im8_1, "sup")
            
        supOpen3D(self.im8_1, self.im8_2, 5, FACE_CENTER_CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertGreater(vol, 0)
        supOpen3D(self.im8_1, self.im8_2, 5)
        vol = computeVolume3D(self.im8_2)
        self.assertGreater(vol, 0)
        supOpen3D(self.im8_1, self.im8_2, 6, FACE_CENTER_CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertEqual(vol, 0)
        supOpen3D(self.im8_1, self.im8_2, 6)
        vol = computeVolume3D(self.im8_2)
        self.assertEqual(vol, 0)
        
        self.im8_1.reset()
        dirs = [(1,10),(3,10),(5,10),(7,10),(9,10),(18,10),
                (2,7),(4,7),(6,7),(8,7),(10,7),(12,7),(14,7),(16,7),
                (19,7),(21,7),(23,7),(25,7),
                (17,6),(11,6),(13,6),(15,6),(20,6),(22,6),(24,6),(26,7)
                ]
        for d,amp in dirs:
            self.im8_4.reset()
            self.im8_4.setPixel(255, (w//2,h//2,l//2))
            linearDilate3D(self.im8_4, self.im8_4, d, amp, CUBIC)
            logic3D(self.im8_1, self.im8_4, self.im8_1, "sup")
            
        supOpen3D(self.im8_1, self.im8_2, 20, CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertGreater(vol, 0)
        supOpen3D(self.im8_1, self.im8_2, 21, CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertEqual(vol, 0)
        
    def testInfClose3D(self):
        """Tests the inferior close 3D operator"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.fill(255)
        dirs = getDirections3D(FACE_CENTER_CUBIC)[1:]
        do = random.choice(dirs)
        for d in dirs:
            self.im8_4.fill(255)
            self.im8_4.setPixel(0, (w//2,h//2,l//2))
            linearErode3D(self.im8_4, self.im8_4, d, d==do and 3 or 2, FACE_CENTER_CUBIC)
            logic3D(self.im8_1, self.im8_4, self.im8_1, "inf")
            
        infClose3D(self.im8_1, self.im8_2, 5, FACE_CENTER_CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertLess(vol, w*h*l*255)
        infClose3D(self.im8_1, self.im8_2, 5)
        vol = computeVolume3D(self.im8_2)
        self.assertLess(vol, w*h*l*255)
        infClose3D(self.im8_1, self.im8_2, 6, FACE_CENTER_CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertEqual(vol, w*h*l*255)
        infClose3D(self.im8_1, self.im8_2, 6)
        vol = computeVolume3D(self.im8_2)
        self.assertEqual(vol, w*h*l*255)
        
        self.im8_1.fill(255)
        dirs = [(1,10),(3,10),(5,10),(7,10),(9,10),(18,10),
                (2,7),(4,7),(6,7),(8,7),(10,7),(12,7),(14,7),(16,7),
                (19,7),(21,7),(23,7),(25,7),
                (17,6),(11,6),(13,6),(15,6),(20,6),(22,6),(24,6),(26,7)
                ]
        for d,amp in dirs:
            self.im8_4.fill(255)
            self.im8_4.setPixel(0, (w//2,h//2,l//2))
            linearErode3D(self.im8_4, self.im8_4, d, amp, CUBIC)
            logic3D(self.im8_1, self.im8_4, self.im8_1, "inf")
            
        infClose3D(self.im8_1, self.im8_2, 20, CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertLess(vol, w*h*l*255)
        infClose3D(self.im8_1, self.im8_2, 21, CUBIC)
        vol = computeVolume3D(self.im8_2)
        self.assertEqual(vol, w*h*l*255)
        
    def testOpenByCylinder3D(self):
        """Verifies the opening by cylinder of a sequence"""
        seq1 = sequenceMb(128,128,5)
        seq2 = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        seq1.fill(0)
        seq1[2].setPixel(255, (64,64))
        seq2.fill(0)
        seq2[2].setPixel(255, (64,64))
        dilateByCylinder3D(seq1, 1, 1)
        dilateByCylinder3D(seq2, 1, 1)
        openByCylinder3D(seq1, 1, 1)
        for i in range(5):
            (x,y) = compare(seq1[i], seq2[i], im)
            self.assertLess(x, 0)
        copy3D(seq2, seq1)
        openByCylinder3D(seq1, 2, 2)
        for i in range(5):
            vol = computeVolume(seq1[i])
            self.assertEqual(vol, 0)
        
    def testCloseByCylinder3D(self):
        """Verifies the opening by cylinder of a sequence"""
        seq1 = sequenceMb(128,128,5)
        seq2 = sequenceMb(128,128,5)
        im = imageMb(128, 128)
        seq1.fill(255)
        seq1[2].setPixel(0, (64,64))
        seq2.fill(255)
        seq2[2].setPixel(0, (64,64))
        erodeByCylinder3D(seq1, 1, 1)
        erodeByCylinder3D(seq2, 1, 1)
        closeByCylinder3D(seq1, 1, 1)
        for i in range(5):
            (x,y) = compare(seq1[i], seq2[i], im)
            self.assertLess(x, 0)
        copy3D(seq2, seq1)
        closeByCylinder3D(seq1, 2, 2)
        for i in range(5):
            vol = computeVolume(seq1[i])
            self.assertEqual(vol, 255*128*128)

