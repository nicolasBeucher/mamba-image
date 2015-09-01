"""
Test cases for the image dual build function.

The function builds an image using the first input image as a mask. It works
with all depths. The function result depends on choice over grid.
    
Python function:
    dualbuildNeighbor
    
C function:
    MB_DualBldNbb
    MB_DualBldNb8
    MB_DualBldNb32
"""

from mamba import *
import unittest
import random

class TestDualBldNb(unittest.TestCase):

    def setUp(self):
        # Creating three images for each possible depth
        self.im1_1 = imageMb(1)
        self.im1_2 = imageMb(1)
        self.im1_3 = imageMb(1)
        self.im8_1 = imageMb(8)
        self.im8_2 = imageMb(8)
        self.im8_3 = imageMb(8)
        self.im32_1 = imageMb(32)
        self.im32_2 = imageMb(32)
        self.im32_3 = imageMb(32)
        self.im8s2_1 = imageMb(128,128,8)
        self.im8s2_2 = imageMb(128,128,8)
        
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
        del(self.im8s2_1)
        del(self.im8s2_2)

    def testDepthAcceptation(self):
        """Tests that incorrect depth raises an exception"""
        #self.assertRaises(MambaError, dualbuildNeighbor, self.im1_1, self.im1_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im1_1, self.im8_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im1_1, self.im32_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im8_1, self.im1_2,0)
        #self.assertRaises(MambaError, dualbuildNeighbor, self.im8_1, self.im8_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im8_1, self.im32_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im32_1, self.im1_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im32_1, self.im8_2,0)
        #self.assertRaises(MambaError, dualbuildNeighbor, self.im32_1, self.im32_2,0)

    def testSizeCheck(self):
        """Tests that different sizes raise an exception"""
        self.assertRaises(MambaError, dualbuildNeighbor, self.im8s2_1, self.im8_2,0)
        self.assertRaises(MambaError, dualbuildNeighbor, self.im8_1, self.im8s2_2,0)
        
    def testParameterAcceptation(self):
        """Tests that incoherent parameters produce an exception"""
        for i in range(7,50):
            self.assertRaises(MambaError, dualbuildNeighbor, self.im1_1, self.im1_2,i, grid=HEXAGONAL)
            self.assertRaises(MambaError, dualbuildNeighbor, self.im8_1, self.im8_2,i, grid=HEXAGONAL)
        for i in range(9,50):
            self.assertRaises(MambaError, dualbuildNeighbor, self.im1_1, self.im1_2,i, grid=SQUARE)
            self.assertRaises(MambaError, dualbuildNeighbor, self.im8_1, self.im8_2,i, grid=SQUARE)

    def _drawExpectedS(self, im, x, y, d, v=1):
        # draws an expected result centered in x,y
        if d==0:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==1:
            mat = [[1,1,0,1,1],[1,1,0,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==2:
            mat = [[1,1,1,1,0],[1,1,1,0,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==3:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,0,0],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==4:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]]
        elif d==5:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,0,1,1],[1,1,0,1,1]]
        elif d==6:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,0,1,1,1],[0,1,1,1,1]]
        elif d==7:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[0,0,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==8:
            mat = [[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        else:
            self.assertTrue(False, "Invalid directions in Square grid")
        for i in range(5):
            for j in range(5):
                im.setPixel(mat[j][i]*v, ((x-2)+i, (y-2)+j))
        return computeVolume(im)
            
    def _drawContainement(self, im, x, y, v):
        # draws a containment barrier
        (w,h) = im.getSize()
        j = y-3
        for i in range(x-3,x+4):
            if j<h and j>=0 and i<w and i>=0:
                im.setPixel(v, (i,j))
        j = y+3
        for i in range(x-3,x+4):
            if j<h and j>=0 and i<w and i>=0:
                im.setPixel(v, (i,j))
                
        i = x-3
        for j in range(y-2,y+3):
            if j<h and j>=0 and i<w and i>=0:
                im.setPixel(v, (i,j))
        i = x+3
        for j in range(y-2,y+3):
            if j<h and j>=0 and i<w and i>=0:
                im.setPixel(v, (i,j))
                

    def testComputationSquare_1(self):
        """Tests build (dual) by neighbor computations in square grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        for wi in range(2,w-2):
            self.im1_2.reset()
            self._drawContainement(self.im1_2, wi, 20, 1)
            for d in getDirections():
                self.im1_1.fill(1)
                self.im1_1.setPixel(0, (wi,20))
                self.im1_3.fill(1)
                exp_vol = self._drawExpectedS(self.im1_3, wi, 20, d)
                vol = dualbuildNeighbor(self.im1_2, self.im1_1, d, grid=SQUARE)
                (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
                self.assertLess(x, 0, "at (%d,20) in dir %d (%d,%d)" % (wi,d,x,y))
                self.assertEqual(vol, exp_vol, "%d/%d" %(vol,exp_vol))
        for wi in range(2,w-2):
            self.im1_2.reset()
            self._drawContainement(self.im1_2, wi, 27, 1)
            for d in getDirections():
                self.im1_1.fill(1)
                self.im1_1.setPixel(0, (wi,27))
                self.im1_3.fill(1)
                exp_vol = self._drawExpectedS(self.im1_3, wi, 27, d)
                vol = dualbuildNeighbor(self.im1_2, self.im1_1, d, grid=SQUARE)
                (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
                self.assertEqual(vol, exp_vol)
                
    def testComputationSquare_8(self):
        """Tests build (dual) by neighbor computations in square grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        for wi in range(2,w-2):
            vi = random.randint(2,255)
            self.im8_2.reset()
            self._drawContainement(self.im8_2, wi, 20, vi)
            for d in getDirections():
                self.im8_1.fill(vi)
                self.im8_1.setPixel(0, (wi,20))
                self.im8_3.fill(vi)
                exp_vol = self._drawExpectedS(self.im8_3, wi, 20, d, vi)
                vol = dualbuildNeighbor(self.im8_2, self.im8_1, d, grid=SQUARE)
                (x,y) = compare(self.im8_3, self.im8_1, self.im8_3)
                self.assertLess(x, 0)
                self.assertEqual(vol, exp_vol, "in dir %d : %d/%d" %(d,vol,exp_vol))
        for wi in range(2,w-2):
            vi = random.randint(2,255)
            self.im8_2.reset()
            self._drawContainement(self.im8_2, wi, 27, vi)
            for d in getDirections():
                self.im8_1.fill(vi)
                self.im8_1.setPixel(0, (wi,27))
                self.im8_3.fill(vi)
                exp_vol = self._drawExpectedS(self.im8_3, wi, 27, d, vi)
                vol = dualbuildNeighbor(self.im8_2, self.im8_1, d, grid=SQUARE)
                (x,y) = compare(self.im8_3, self.im8_1, self.im8_3)
                self.assertLess(x, 0, "at (%d,27) in dir %d (%d,%d)" % (wi,d,x,y))
                self.assertEqual(vol, exp_vol)
                
    def testComputationSquare_32(self):
        """Tests build (dual) by neighbor computations in square grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        for wi in range(2,w-2):
            vi = random.randint(2,0xffffffff)
            self.im32_2.reset()
            self._drawContainement(self.im32_2, wi, 20, vi)
            for d in getDirections():
                self.im32_1.fill(vi)
                self.im32_1.setPixel(0, (wi,20))
                self.im32_3.fill(vi)
                exp_vol = self._drawExpectedS(self.im32_3, wi, 20, d, vi)
                vol = dualbuildNeighbor(self.im32_2, self.im32_1, d, grid=SQUARE)
                (x,y) = compare(self.im32_3, self.im32_1, self.im32_3)
                self.assertLess(x, 0)
                self.assertEqual(vol, exp_vol, "in dir %d : %d/%d" %(d,vol,exp_vol))
        for wi in range(2,w-2):
            vi = random.randint(2,0xffffffff)
            self.im32_2.reset()
            self._drawContainement(self.im32_2, wi, 27, vi)
            for d in getDirections():
                self.im32_1.fill(vi)
                self.im32_1.setPixel(0, (wi,27))
                self.im32_3.fill(vi)
                exp_vol = self._drawExpectedS(self.im32_3, wi, 27, d, vi)
                vol = dualbuildNeighbor(self.im32_2, self.im32_1, d, grid=SQUARE)
                (x,y) = compare(self.im32_3, self.im32_1, self.im32_3)
                self.assertLess(x, 0, "at (%d,27) in dir %d (%d,%d)" % (wi,d,x,y))
                self.assertEqual(vol, exp_vol)

    def _drawExpectedHO(self, im, x, y, d, v=1):
        # draws an expected result centered in x,y
        if d==0:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==1:
            mat = [[1,1,1,0,1],[1,1,1,0,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==2:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,0,0],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==3:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,0,1]]
        elif d==4:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,0,1,1],[1,0,1,1,1]]
        elif d==5:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[0,0,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==6:
            mat = [[1,0,1,1,1],[1,1,0,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        else:
            self.assertTrue(False, "Invalid directions in Hexagonal grid")
        for i in range(5):
            for j in range(5):
                im.setPixel(mat[j][i]*v, ((x-2)+i, (y-2)+j))
        return computeVolume(im)

    def _drawExpectedHE(self, im, x, y, d, v=1):
        # draws an expected result centered in x,y
        if d==0:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==1:
            mat = [[1,1,1,0,1],[1,1,0,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==2:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,0,0],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==3:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,0,1,1],[1,1,1,0,1]]
        elif d==4:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,0,1,1,1],[1,0,1,1,1]]
        elif d==5:
            mat = [[1,1,1,1,1],[1,1,1,1,1],[0,0,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        elif d==6:
            mat = [[1,0,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,1,1],[1,1,1,1,1]]
        else:
            self.assertTrue(False, "Invalid directions in Hexagonal grid")
        for i in range(5):
            for j in range(5):
                im.setPixel(mat[j][i]*v, ((x-2)+i, (y-2)+j))
        return computeVolume(im)

    def testComputationHexagonal_1(self):
        """Tests build (dual) by neighbor computations in hexagonal grid on binary images"""
        (w,h) = self.im1_1.getSize()
        
        for wi in range(2,w-2):
            self.im1_2.reset()
            self._drawContainement(self.im1_2, wi, 20, 1)
            for d in getDirections():
                self.im1_1.fill(1)
                self.im1_1.setPixel(0, (wi,20))
                self.im1_3.fill(1)
                exp_vol = self._drawExpectedHE(self.im1_3, wi, 20, d)
                vol = dualbuildNeighbor(self.im1_2, self.im1_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
                self.assertLess(x, 0, "at (%d,20) in dir %d (%d,%d)" % (wi,d,x,y))
                self.assertEqual(vol, exp_vol, "%d/%d" %(vol,exp_vol))
        for wi in range(2,w-2):
            self.im1_2.reset()
            self._drawContainement(self.im1_2, wi, 27, 1)
            for d in getDirections():
                self.im1_1.fill(1)
                self.im1_1.setPixel(0, (wi,27))
                self.im1_3.fill(1)
                exp_vol = self._drawExpectedHO(self.im1_3, wi, 27, d)
                vol = dualbuildNeighbor(self.im1_2, self.im1_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im1_3, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
                self.assertEqual(vol, exp_vol)
                
    def testComputationHexagonal_8(self):
        """Tests dualbuild by neighbor computations in hexagonal grid on 8-bit images"""
        (w,h) = self.im8_1.getSize()
        
        for wi in range(2,w-2):
            vi = random.randint(2,255)
            self.im8_2.reset()
            self._drawContainement(self.im8_2, wi, 20, vi)
            for d in getDirections():
                self.im8_1.fill(vi)
                self.im8_1.setPixel(0, (wi,20))
                self.im8_3.fill(vi)
                exp_vol = self._drawExpectedHE(self.im8_3, wi, 20, d, vi)
                vol = dualbuildNeighbor(self.im8_2, self.im8_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im8_3, self.im8_1, self.im8_3)
                self.assertLess(x, 0)
                self.assertEqual(vol, exp_vol, "in dir %d : %d/%d" %(d,vol,exp_vol))
        for wi in range(2,w-2):
            vi = random.randint(2,255)
            self.im8_2.reset()
            self._drawContainement(self.im8_2, wi, 27, vi)
            for d in getDirections():
                self.im8_1.fill(vi)
                self.im8_1.setPixel(0, (wi,27))
                self.im8_3.fill(vi)
                exp_vol = self._drawExpectedHO(self.im8_3, wi, 27, d, vi)
                vol = dualbuildNeighbor(self.im8_2, self.im8_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im8_3, self.im8_1, self.im8_3)
                self.assertLess(x, 0, "at (%d,27) in dir %d (%d,%d)" % (wi,d,x,y))
                self.assertEqual(vol, exp_vol)
                
    def testComputationHexagonal_32(self):
        """Tests dualbuild by neighbor computations in hexagonal grid on 32-bit images"""
        (w,h) = self.im32_1.getSize()
        
        for wi in range(2,w-2):
            vi = random.randint(2,0xffffffff)
            self.im32_2.reset()
            self._drawContainement(self.im32_2, wi, 20, vi)
            for d in getDirections():
                self.im32_1.fill(vi)
                self.im32_1.setPixel(0, (wi,20))
                self.im32_3.fill(vi)
                exp_vol = self._drawExpectedHE(self.im32_3, wi, 20, d, vi)
                vol = dualbuildNeighbor(self.im32_2, self.im32_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im32_3, self.im32_1, self.im32_3)
                self.assertLess(x, 0)
                self.assertEqual(vol, exp_vol, "in dir %d : %d/%d" %(d,vol,exp_vol))
        for wi in range(2,w-2):
            vi = random.randint(2,0xffffffff)
            self.im32_2.reset()
            self._drawContainement(self.im32_2, wi, 27, vi)
            for d in getDirections():
                self.im32_1.fill(vi)
                self.im32_1.setPixel(0, (wi,27))
                self.im32_3.fill(vi)
                exp_vol = self._drawExpectedHO(self.im32_3, wi, 27, d, vi)
                vol = dualbuildNeighbor(self.im32_2, self.im32_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im32_3, self.im32_1, self.im32_3)
                self.assertLess(x, 0, "at (%d,27) in dir %d (%d,%d)" % (wi,d,x,y))
                self.assertEqual(vol, exp_vol)
            
    def testInoutComputation_1(self):
        """Verifies computation when a binary image is used as both mask and output"""
        (w,h) = self.im1_1.getSize()
        for wi in range(2,w-2):
            for d in getDirections():
                self.im1_1.fill(1)
                self.im1_1.setPixel(0, (wi,20))
                self.im1_2.fill(1)
                self.im1_2.setPixel(0, (wi,20))
                vol = dualbuildNeighbor(self.im1_1, self.im1_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
                vol = dualbuildNeighbor(self.im1_1, self.im1_1, d, grid=SQUARE)
                (x,y) = compare(self.im1_2, self.im1_1, self.im1_3)
                self.assertLess(x, 0)
                
    def testInoutComputation_8(self):
        """Verifies computation when a 8-bit image is used as both mask and output"""
        (w,h) = self.im8_1.getSize()
        for wi in range(2,w-2):
            vi = random.randint(2,255)
            for d in getDirections():
                self.im8_1.fill(vi)
                self.im8_1.setPixel(0, (wi,20))
                self.im8_2.fill(vi)
                self.im8_2.setPixel(0, (wi,20))
                vol = dualbuildNeighbor(self.im8_1, self.im8_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)
                vol = dualbuildNeighbor(self.im8_1, self.im8_1, d, grid=SQUARE)
                (x,y) = compare(self.im8_2, self.im8_1, self.im8_3)
                self.assertLess(x, 0)
                
    def testInoutComputation_32(self):
        """Verifies computation when a 32-bit image is used as both mask and output"""
        (w,h) = self.im32_1.getSize()
        for wi in range(2,w-2):
            vi = random.randint(2,0xffffffff)
            for d in getDirections():
                self.im32_1.fill(vi)
                self.im32_1.setPixel(0, (wi,20))
                self.im32_2.fill(vi)
                self.im32_2.setPixel(0, (wi,20))
                vol = dualbuildNeighbor(self.im32_1, self.im32_1, d, grid=HEXAGONAL)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0)
                vol = dualbuildNeighbor(self.im32_1, self.im32_1, d, grid=SQUARE)
                (x,y) = compare(self.im32_2, self.im32_1, self.im32_3)
                self.assertLess(x, 0)

