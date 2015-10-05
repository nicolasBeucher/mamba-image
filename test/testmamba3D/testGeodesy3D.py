"""
Test cases for the geodesic operators found in the geodesy3D
module of mamba3D package. 

Python functions:
    upperGeodesicDilate3D
    lowerGeodesicDilate3D
    geodesicDilate3D
    upperGeodesicErode3D
    lowerGeodesicErode3D
    geodesicErode3D
    build3D
    dualBuild3D
    closeHoles3D
    removeEdgeParticles3D
    buildNeighbor3D
    dualbuildNeighbor3D
"""

from mamba import *
from mamba3D import *
import unittest
import random

class TestGeodesy3D(unittest.TestCase):

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
        self.im8_5 = image3DMb(64,64,64,8)
        self.im8_6 = image3DMb(128,128,128,8)
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
        del(self.im32_1)
        del(self.im32_2)
        del(self.im32_3)
        del(self.im32_4)
        del(self.im32_5)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        self.assertRaises(MambaError, build3D, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, build3D, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, build3D, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, build3D, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, build3D, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, build3D, self.im32_1, self.im8_2)
        self.assertRaises(MambaError, dualBuild3D, self.im1_1, self.im8_2)
        self.assertRaises(MambaError, dualBuild3D, self.im1_1, self.im32_2)
        self.assertRaises(MambaError, dualBuild3D, self.im8_1, self.im1_2)
        self.assertRaises(MambaError, dualBuild3D, self.im8_1, self.im32_2)
        self.assertRaises(MambaError, dualBuild3D, self.im32_1, self.im1_2)
        self.assertRaises(MambaError, dualBuild3D, self.im32_1, self.im8_2)
        
    def testGridAcceptation(self):
        """Tests that incorrect grid raises an exception"""
        self.assertRaises(MambaError, build3D, self.im8_1, self.im8_2, grid=CENTER_CUBIC)
        self.assertRaises(MambaError, dualBuild3D, self.im8_1, self.im8_2, grid=CENTER_CUBIC)
        
    def testSizeCheck(self):
        """Verifies that the functions check the size of the image"""
        self.assertRaises(MambaError, build3D, self.im8_6, self.im8_2)
        self.assertRaises(MambaError, build3D, self.im1_5, self.im1_2)
        self.assertRaises(MambaError, build3D, self.im32_5, self.im32_2)
        self.assertRaises(MambaError, dualBuild3D, self.im8_6, self.im8_2)
        self.assertRaises(MambaError, dualBuild3D, self.im1_5, self.im1_2)
        self.assertRaises(MambaError, dualBuild3D, self.im32_5, self.im32_2)    
        self.assertRaises(MambaError, buildNeighbor3D, self.im8_6, self.im8_2, 1)
        self.assertRaises(MambaError, buildNeighbor3D, self.im1_5, self.im1_2, 1)
        self.assertRaises(MambaError, buildNeighbor3D, self.im32_5, self.im32_2, 1)
        self.assertRaises(MambaError, dualbuildNeighbor3D, self.im8_6, self.im8_2, 1)
        self.assertRaises(MambaError, dualbuildNeighbor3D, self.im1_5, self.im1_2, 1)
        self.assertRaises(MambaError, dualbuildNeighbor3D, self.im32_5, self.im32_2, 1)       
        self.assertRaises(MambaError, upperGeodesicDilate3D, self.im8_6, self.im8_2, self.im8_3)
        self.assertRaises(MambaError, lowerGeodesicDilate3D, self.im8_6, self.im8_2, self.im8_3)
        self.assertRaises(MambaError, geodesicDilate3D, self.im8_6, self.im8_2, self.im8_3)
        self.assertRaises(MambaError, upperGeodesicErode3D, self.im8_6, self.im8_2, self.im8_3)
        self.assertRaises(MambaError, lowerGeodesicErode3D, self.im8_6, self.im8_2, self.im8_3)
        self.assertRaises(MambaError, geodesicErode3D, self.im8_6, self.im8_2, self.im8_3)
        
    def testBuild3D_1(self):
        """Tests the reconstruction operator on binary 3D images"""
        for d in getDirections3D():
            self.im1_1.reset()
            self.im1_1.setPixel(1, (32,32,32))
            self.im1_2.reset()
            self.im1_2.setPixel(1, (32,32,32))
            self.im1_2.setPixel(1, (0,0,0))
            self.im1_3.reset()
            self.im1_3.setPixel(1, (32,32,32))
            linearDilate3D(self.im1_1, self.im1_1, d, 4)
            linearDilate3D(self.im1_3, self.im1_3, d, 4)
            build3D(self.im1_1, self.im1_2)
            (x,y,z) = compare3D(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testBuild3D_8(self):
        """Tests the reconstruction operator on 8-bit 3D images"""
        grids = [FACE_CENTER_CUBIC, CUBIC]
        for grid in grids:
            for d in getDirections3D(grid):
                self.im8_1.reset()
                self.im8_1.setPixel(255, (32,32,32))
                self.im8_2.reset()
                self.im8_2.setPixel(128, (32,32,32))
                self.im8_2.setPixel(128, (0,0,0))
                self.im8_3.reset()
                self.im8_3.setPixel(128, (32,32,32))
                linearDilate3D(self.im8_1, self.im8_1, d, 4, grid=grid)
                linearDilate3D(self.im8_3, self.im8_3, d, 4, grid=grid)
                build3D(self.im8_1, self.im8_2, grid=grid)
                (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
                self.assertLess(x, 0, "grid %s, dir %d : diff in (%d,%d,%d)"%(repr(grid),d,x,y,z))
        
    def testBuild3D_32(self):
        """Tests the reconstruction operator on 32-bit 3D images"""
        grids = [FACE_CENTER_CUBIC, CUBIC]
        for grid in grids:
            for d in getDirections3D(grid):
                self.im32_1.reset()
                self.im32_1.setPixel(655, (32,32,32))
                self.im32_2.reset()
                self.im32_2.setPixel(528, (32,32,32))
                self.im32_2.setPixel(528, (0,0,0))
                self.im32_3.reset()
                self.im32_3.setPixel(528, (32,32,32))
                linearDilate3D(self.im32_1, self.im32_1, d, 4, grid=grid)
                linearDilate3D(self.im32_3, self.im32_3, d, 4, grid=grid)
                build3D(self.im32_1, self.im32_2, grid=grid)
                (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
                self.assertLess(x, 0, "%d: diff in (%d,%d,%d)"%(d,x,y,z))
            
    def testDualBuild3D_1(self):
        """Tests the reconstruction (dual) operator on binary 3D images"""
        for d in getDirections3D():
            self.im1_1.fill(1)
            self.im1_1.setPixel(0, (32,32,32))
            self.im1_2.fill(1)
            self.im1_2.setPixel(0, (32,32,32))
            self.im1_2.setPixel(0, (0,0,0))
            self.im1_3.fill(1)
            self.im1_3.setPixel(0, (32,32,32))
            linearErode3D(self.im1_1, self.im1_1, d, 4)
            linearErode3D(self.im1_3, self.im1_3, d, 4)
            dualBuild3D(self.im1_1, self.im1_2)
            (x,y,z) = compare3D(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
        
    def testDualBuild3D_8(self):
        """Tests the reconstruction (dual) operator on 8-bit 3D images"""
        grids = [FACE_CENTER_CUBIC, CUBIC]
        for grid in grids:
            for d in getDirections3D(grid):
                self.im8_1.fill(255)
                self.im8_1.setPixel(0, (32,32,32))
                self.im8_2.fill(255)
                self.im8_2.setPixel(128, (32,32,32))
                self.im8_2.setPixel(128, (0,0,0))
                self.im8_3.fill(255)
                self.im8_3.setPixel(128, (32,32,32))
                linearErode3D(self.im8_1, self.im8_1, d, 4, grid=grid)
                linearErode3D(self.im8_3, self.im8_3, d, 4, grid=grid)
                dualBuild3D(self.im8_1, self.im8_2, grid=grid)
                (x,y,z) = compare3D(self.im8_3, self.im8_2, self.im8_3)
                self.assertLess(x, 0, "grid %s, dir %d : diff in (%d,%d,%d)"%(repr(grid),d,x,y,z))
        
    def testDualBuild3D_32(self):
        """Tests the reconstruction (dual) operator on 32-bit 3D images"""
        grids = [FACE_CENTER_CUBIC, CUBIC]
        for grid in grids:
            for d in getDirections3D(grid):
                self.im32_1.fill(655)
                self.im32_1.setPixel(0, (32,32,32))
                self.im32_2.fill(655)
                self.im32_2.setPixel(528, (32,32,32))
                self.im32_2.setPixel(528, (0,0,0))
                self.im32_3.fill(655)
                self.im32_3.setPixel(528, (32,32,32))
                linearErode3D(self.im32_1, self.im32_1, d, 4, grid=grid)
                linearErode3D(self.im32_3, self.im32_3, d, 4, grid=grid)
                dualBuild3D(self.im32_1, self.im32_2, grid=grid)
                (x,y,z) = compare3D(self.im32_3, self.im32_2, self.im32_3)
                self.assertLess(x, 0, "diff in (%d,%d,%d)"%(x,y,z))
            
    def testLowerGeodesicDilate3D_1(self):
        """Verifies the lower geodesic dilation operation for binary 3D images"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        
        drawCube(self.im1_2, (w//2-2,h//2-2,l//2-2,w//2+2,h//2+2,l//2+2), 1)
        self.im1_1.setPixel(1, (w//2,h//2-2,l//2))
        self.im1_1.setPixel(1, (w//2,h//2-3,l//2))
        drawCube(self.im1_4, (w//2-1,h//2-2,l//2-1,w//2+1,h//2-1,l//2+1), 1)
        lowerGeodesicDilate3D(self.im1_1, self.im1_2, self.im1_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        geodesicDilate3D(self.im1_1, self.im1_2, self.im1_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicDilate3D_1(self):
        """Verifies the upper geodesic dilation operation for binary 3D images"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        
        drawCube(self.im1_2, (w//2-2,h//2-2,l//2-2,w//2+2,h//2+2,l//2+2), 1)
        self.im1_1.setPixel(1, (w//2,h//2-2,l//2))
        self.im1_1.setPixel(1, (w//2,h//2-3,l//2))
        drawCube(self.im1_4, (w//2-1,h//2-4,l//2-1,w//2+1,h//2-3,l//2+1), 1)
        drawCube(self.im1_4, (w//2-2,h//2-2,l//2-2,w//2+2,h//2+2,l//2+2), 1)
        upperGeodesicDilate3D(self.im1_1, self.im1_2, self.im1_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicDilate3D_8(self):
        """Verifies the upper geodesic dilation operation for greyscale 3D images"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(l,64)):
            self.im8_1[i].fill(63-i)
        self.im8_2.fill(32)
        self.im8_4.fill(32)
        for i in range(33):
            self.im8_4[i].fill(min(64-i,63))
        upperGeodesicDilate3D(self.im8_1, self.im8_2, self.im8_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testLowerGeodesicDilate3D_8(self):
        """Verifies the lower geodesic dilation operation for greyscale 3D images"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(l,64)):
            self.im8_1[i].fill(63-i)
        self.im8_2.fill(32)
        
        self.im8_4.reset()
        for i in range(33):
            self.im8_4[i].fill(32)
        for i in range(33,min(w,64)):
            self.im8_4[i].fill(64-i)
        lowerGeodesicDilate3D(self.im8_1, self.im8_2, self.im8_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        geodesicDilate3D(self.im8_1, self.im8_2, self.im8_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testLowerGeodesicErode3D_1(self):
        """Verifies the lower geodesic erosion operation for binary images"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        drawCube(self.im1_2, (w//2-2,h//2-2,l//2-2,w//2+2,h//2+2,l//2+2), 1)
        self.im1_4.setPixel(1, (w//2,h//2-2,l//2))
        drawCube(self.im1_1, (w//2-1,h//2-3,l//2-1,w//2+1,h//2-1,l//2+1), 1)
        lowerGeodesicErode3D(self.im1_1, self.im1_2, self.im1_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
        geodesicErode3D(self.im1_1, self.im1_2, self.im1_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicErode3D_1(self):
        """Verifies the upper geodesic erosion operation for binary images"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        self.im1_3.reset()
        self.im1_4.reset()
        drawCube(self.im1_2, (w//2-2,h//2-2,l//2-2,w//2+2,h//2+2,l//2+2), 1)
        self.im1_4.setPixel(1, (w//2,h//2-3,l//2))
        drawCube(self.im1_4, (w//2-2,h//2-2,l//2-2,w//2+2,h//2+2,l//2+2), 1)
        drawCube(self.im1_1, (w//2-1,h//2-4,l//2-1,w//2+1,h//2-1,l//2+1), 1)
        upperGeodesicErode3D(self.im1_1, self.im1_2, self.im1_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im1_4, self.im1_3, self.im1_3)
        self.assertLess(x, 0)
            
    def testUpperGeodesicErode3D_8(self):
        """Verifies the upper geodesic erosion operation for greyscale images"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(l,64)):
            self.im8_1[i].fill(63-i)
        self.im8_2.fill(32)
        self.im8_4.fill(32)
        for i in range(31):
            self.im8_4[i].fill(62-i)
        upperGeodesicErode3D(self.im8_1, self.im8_2, self.im8_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
        geodesicErode3D(self.im8_1, self.im8_2, self.im8_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testLowerGeodesicErode3D_8(self):
        """Verifies the lower geodesic erosion operation for greyscale images"""
        (w,h,l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        for i in range(min(l,64)):
            self.im8_1[i].fill(63-i)
        self.im8_2.fill(32)
        
        self.im8_4.reset()
        for i in range(31):
            self.im8_4[i].fill(32)
        for i in range(31,min(l,64)-1):
            self.im8_4[i].fill(62-i)
        lowerGeodesicErode3D(self.im8_1, self.im8_2, self.im8_3, 1, se=CUBE3X3X3)
        (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_3)
        self.assertLess(x, 0)
            
    def testCloseHoles3D(self):
        """Verifies the closing holes 3D operator"""
        (w,h,l) = self.im1_1.getSize()
        
        for i in range(3,5):
            self.im1_1.reset()
            drawCube(self.im1_1, (w//2-i,h//2-i,l//2-i,w//2+i,h//2+i,l//2+i), 1)
            drawCube(self.im1_1, (w//2-(i-1),h//2-(i-1),l//2-(i-1),w//2+(i-1),h//2+(i-1),l//2+(i-1)), 0)
            self.im1_2.reset()
            drawCube(self.im1_2, (w//2-i,h//2-i,l//2-i,w//2+i,h//2+i,l//2+i), 1)
            closeHoles3D(self.im1_1, self.im1_3)
            (x,y,z) = compare3D(self.im1_3, self.im1_2, self.im1_3)
            self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))
            
    def testRemoveEdgeParticles3D(self):
        """Tests the 3D operator removing the particles connected to the edge"""
        (w,h,l) = self.im1_1.getSize()
        
        self.im1_1.reset()
        self.im1_2.reset()
        y=1
        z=1
        i=0
        while (y+i)<h and (z+i)<l:
            drawCube(self.im1_1, (0,y,z,i,y+i,z+i), 1)
            drawCube(self.im1_1, (w//2,y,z,w//2+i,y+i,z+i), 1)
            drawCube(self.im1_2, (w//2,y,z,w//2+i,y+i,z+i), 1)
            y += i+2
            z += i+2
            i += 1
        removeEdgeParticles3D(self.im1_1, self.im1_3)
        (x,y,z) = compare3D(self.im1_3, self.im1_2, self.im1_3)
        self.assertLess(x, 0, "%d : %d,%d,%d" %(i,x,y,z))

    def testBuildNeighbor3D(self):
        """Tests the buildNeighbor3D (directional build) operator"""   
        (w, h, l) = self.im8_1.getSize()
        
        self.im8_1.reset()
        self.im8_2.reset()
        cube = (w//2 - 25, h//2 -25, l//2 + 25, w//2 + 25, h//2 + 25, l//2 - 25)
        drawCube(self.im8_1, cube, 255)
        self.im8_2.setPixel(200, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                copy3D(self.im8_2, self.im8_3)
                dt = transposeDirection3D(d, grid3D)
                linearDilate3D(self.im8_3, self.im8_4, dt, 30, grid3D)
                logic3D(self.im8_1, self.im8_4, self.im8_4, "inf")
                buildNeighbor3D(self.im8_1, self.im8_3, d, grid3D)
                (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_5)
                self.assertLess(x, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
    
    def testDualbuildNeighbor3D(self):
        """Tests the dualbuildNeighbor3D (directional dual build) operator"""   
        (w, h, l) = self.im8_1.getSize()
        
        self.im8_1.fill(255)
        self.im8_2.fill(255)
        cube = (w//2 - 25, h//2 -25, l//2 + 25, w//2 + 25, h//2 + 25, l//2 - 25)
        drawCube(self.im8_1, cube, 0)
        self.im8_2.setPixel(0, (w//2, h//2, l//2))
        for grid3D in (FACE_CENTER_CUBIC, CENTER_CUBIC, CUBIC):
            for d in getDirections3D(grid3D, withoutZero=True):
                copy3D(self.im8_2, self.im8_3)
                dt = transposeDirection3D(d, grid3D)
                linearErode3D(self.im8_3, self.im8_4, dt, 30, grid3D)
                logic3D(self.im8_1, self.im8_4, self.im8_4, "sup")
                dt = transposeDirection3D(d, grid3D)
                dualbuildNeighbor3D(self.im8_1, self.im8_3, d, grid3D)
                (x,y,z) = compare3D(self.im8_4, self.im8_3, self.im8_5)    
                self.assertLess(x, 0, "grid3D %s, dir %d : diff in (%d,%d,%d)"%(repr(grid3D),d,x,y,z))
